import os
import sys
from lxml import etree
import textwrap
import wave
import mad
import operator

AUDIO_EXT = [".mp3", ".wav"]
DOCTYPE = '<!DOCTYPE sonic-visualiser>'
ENCODING = 'UTF-8'

COMMONERRS = ['b6', 'b7', '#7', 'b9', '#9', 'b11', '#11', 'b13', '#13']
TRIADS = ['maj','min','aug','dim']
SEVENTH = ['maj7','min7','7','hdim7', 'dim7']
SIXTH = ['maj6','min6']
EXTENDED = ['9', 'maj9', 'min9']
EXTENDED2 = ['maj11', 'min11', 'maj13', 'min13']
SUSPENDED = ['sus4', 'sus2']
DOMINANTS = ['7', '9', '11', '13']
ALLTYPES = TRIADS+SEVENTH+SIXTH+EXTENDED+SUSPENDED+DOMINANTS+EXTENDED2


#curdir = os.path.abspath(os.path.expanduser("~/Dropbox/RWC_Pop_Chords"))
curdir = os.path.abspath(os.path.expanduser("~/Dropbox/uspopLabels"))
#curdir = os.path.expanduser(sys.argv[1])
#destdir = os.path.abspath(os.path.expanduser("~/MacHDD/Volumes/Audio/Data/RWC-MDB-P-2001"))
destdir = os.path.abspath(os.path.expanduser("~/MacHDD/Users/taemin/mp3s"))
#destdir = os.path.expanduser(sys.argv[2])

Labfiles = [os.path.join(dirname, filename) \
         for dirname, dirnames, filenames in os.walk(curdir) \
            for filename in filenames \
                if os.path.splitext(filename)[1].lower() == '.svl']
Labfiles.sort()


def accsort(acc):
    """sort tensions

    Arguments:
    - `acc`:
    """
    symbols = ['b', '#']
    accnum = []
    for x in acc:
        if x[0] == '*':
            if not symbols.count(x[1]):
                v = int(x[1:])
            else:
                v = symbols.index(x[1]) - 0.5 + int(x[2:])
        elif not symbols.count(x[0]):
            v = int(x)
        else:
            v = symbols.index(x[0]) - 0.5 + int(x[1:])
        accnum.append(v)

    # accnum = [int(x) if not symbols.count(x[0]) else symbols.index(x[0]) - 0.5 + int(x[1:]) \
    #           for x in acc];

    idx = [x[0] for x in sorted(enumerate(accnum), key=operator.itemgetter(1))]

    return [acc[x] for x in idx]

def checkGrammar(frame, label):
    """Check grammer

    Arguments:
    - `label`:
    """

    error = []
    change = []
    root = []
    bass = ''
    quality = ''
    acc = []
    suggestionNeeded = False

    # parsing
    if label.count(':'):
        root, temp = label.split(':')
        if temp.count('/'):
            temp, bass = temp.split('/')
        if temp.count('('):
            quality, acc = temp.split('(')
            acc = acc.split(')')[0]
            acc = acc.split(',')
        else:
            quality = temp
    else:
        if label.count('/'):
            root, bass = label.split('/')
        else:
            root = label


    root = root.strip()
    quality = quality.strip().lower().replace(' ','')
    acc = [x.strip() for x in acc]
    bass = bass.strip().lower()

    if root != 'end' and len(root) > 2:
        error.append('%-10d %-15s labeling error' %(frame, label))

    if root != 'end':
        root = root.capitalize()


    if quality != '':
        if quality == 'maj':
            if acc.count('#5'):
                acc.remove('#5')
                quality = 'aug'
                suggestionNeeded = True
        if quality == '7':
            if acc.count('#5'):
                acc.remove('#5')
                acc.append('b7')
                quality = 'aug'
                suggestionNeeded = True
        if quality == 'maj7':
            if acc.count('#5'):
                acc.remove('#5')
                acc.append('7')
                quality = 'aug'
                suggestionNeeded = True

        if quality == 'hdim':
            error.append('%-10d %-15s labeling error' %(frame, label))
        elif quality == '6':
            quality = 'maj6'
            suggestionNeeded = True
        elif COMMONERRS.count(quality):
            if acc.count('2') or acc.count('4'):
                error.append('%-10d %-15s labeling error' %(frame, label))
            else:
                acc.append(quality)
                quality = '7'
                suggestionNeeded = True
        elif EXTENDED2.count(quality):
            error.append('%-10d %-15s are you sure ?' %(frame, label))
        elif not ALLTYPES.count(quality):
            error.append("%-10d %-15s don't understand" %(frame, label))
        else:
            for x in COMMONERRS:
                if quality.find(x) > -1:
                    error.append('%-10d %-15s labeling error' %(frame, label))
                    break

    if bass:
        if not bass.isdigit():
            if not ['b', '#'].count(bass[0]) or not bass[1:].isdigit():
                error.append('%-10d %-15s bass error' %(frame, label))

        if ['maj', 'maj7'].count(quality) and ['b3', 'b5', '#5', 'b7'].count(bass):
            error.append('%-10d %-15s bass confliction' %(frame, label))
        elif quality.find('maj') > -1 and ['b3', 'b5', '#5', 'b7'].count(bass):
            error.append('%-10d %-15s bass confliction' %(frame, label))

        if quality == 'maj' and bass == '7':
            quality = 'maj7'
            if acc:
                acc.remove('7')
            suggestionNeeded = True

        if quality.find('aug') > -1:
            if ['b3', 'b5', '5'].count(bass) or (['b7', '7'].count(bass) and not acc.count(bass)):
                error.append('%-10d %-15s bass confliction' %(frame, label))

        if quality == 'min7' and ['3', 'b5', '#5', '7'].count(bass):
            error.append('%-10d %-15s bass confliction' %(frame, label))

        if quality == 'min':
            if ['3', 'b5', '#5'].count(bass) or (bass == '7' and not acc.count(bass)):
                error.append('%-10d %-15s bass confliction' %(frame, label))

            if bass == 'b7':
                quality = 'min7'
                if acc:
                    acc.remove('b7')
                suggestionNeeded = True

        if quality == 'dim':
            if ['3', '5', '#5'].count(bass) or (bass == '7' and not acc.count(bass)):
                error.append('%-10d %-15s labeling error' %(frame, label))

            if bass == 'b7':
                quality = 'hdim7'
                if acc:
                    acc.remove('b7')
                suggestionNeeded = True
            if bass == 'bb7' or bass == '6':
                quality = 'dim7'
                if acc:
                    acc.remove('bb7')
                    acc.remove('6')
                suggestionNeeded = True

        if quality == 'hdim7':
            if ['3', '5', '#5', '7', 'bb7'].count(bass):
                error.append('%-10d %-15s labeling error' %(frame, label))

        if DOMINANTS.count(quality):
            if ['b3', '7'].count(bass):
                error.append('%-10d %-15s bass confliction' %(frame, label))

        if (acc.count('*3') and bass == '3') \
           or (acc.count('*b3') and bass == 'b3') \
           or (acc.count('*5') and bass == '5') \
           or (acc.count('*7') and bass == '7') \
           or (acc.count('*b7') and bass == 'b7'):
            error.append('%-10d %-15s bass confliction' %(frame, label))

        if not error \
               and ((acc and not acc.count(bass) or not acc)\
                    and ['2', '4', 'b9', '9', '#9', '11','#11','13','b13'].count(bass)):
            if not quality.count(bass): # for sus4 and sus2
                error.append('%-10d %-15s pedal bass ?' %(frame, label))


    acc = accsort(list(set(acc))) # remove duplicates

    # compose
    newlabel = root
    if quality != '' or acc:
        newlabel += ':'
        if quality != '':
            newlabel += quality
        if acc:
            newlabel += '('+','.join(acc)+')'

    if bass != '':
        newlabel += '/'+bass

    if not label == newlabel:
        change.append(label + ' -> ' + newlabel)

    else:
        newlabel = []

    if suggestionNeeded:
        error.append('%-10d %-15s maybe %-15s' %(frame, label, newlabel))

    return newlabel, error, change

def checkSVL(labelFile, samples):

    """Check errors of labels and fix them if available

    Arguments:
    - `labelFile`: a xml formatted file that have labels
    - `samples`  : the length of audio file in samples
    """

    errors = []
    changes = []

    needUpdate = False
    elements = etree.iterparse(labelFile, tag='point', remove_blank_text=True)

    prevframe = -10000
    for i, [event, element] in enumerate(elements):
        curframe = int(element.get('frame'))
        curLabel = element.get('label')
        if curLabel.count('[') and curLabel.count(']'):
            p = element.getparent()
            p.remove(element)
            changes.append('remove %d %s' %(curframe, curLabel))
            needUpdate = True
            continue

        # Starting Point add 'N' for starting silence
        if i == 0 and curframe != 0:
            if curLabel.strip() == 'N':
                element.set('frame', '0')
                changes.append('%d %s -> 0 N' %(curframe, curLabel))
            else:
                startpoint = etree.Element('point', frame='0', label = 'N')
                element.addprevious(startpoint)
                changes.append('0 N Added at the begining')
            needUpdate = True

        if curframe - prevframe < 1000:
            errors.append('%-10d %-15s is duplicated' %(curframe, curLabel))

        # Grammer Check
        newLabel, err, change = checkGrammar(curframe, curLabel)

        changes.extend(change)

        if err:
            errors.extend(err)

        if newLabel:
            element.set('label', newLabel)
            needUpdate = True

        prevframe = curframe

    # End Point - add end mark
    if int(element.get('frame')) < samples:
        if not element.get('label') == 'end':
            endpoint = etree.Element('point', frame=str(samples), label = 'end')
            element.addnext(endpoint)
            changes.append('%d end Added' %(samples))
            needUpdate = True
    else:
        element.set('label', 'end')
        needUpdate = True

    if needUpdate:
        # Generate new xml file
        newXML = etree.tostring(elements.root,
                                xml_declaration=True,
                                pretty_print=True,
                                doctype=DOCTYPE,
                                encoding='UTF-8')
    else:
        newXML = []

    return newXML, errors, changes

def svl2lab(labelFile):

    """Convert svl file to text format lab file

    Arguments:
    - `labelFile`: a xml formatted file that have labels
    """

    model = etree.iterparse(labelFile, tag='model').next()
    sampleRate = float(model[-1].get('sampleRate'))
    elements = etree.iterparse(labelFile, tag='point', remove_blank_text=True)

    lines = []
    for i, [event, element] in enumerate(elements):
        curframe = int(element.get('frame'))
        endTime=curframe/sampleRate
        if i:
            line = '%.3f\t%.3f\t%s\n' %(startTime, endTime, curLabel)
            lines.append(line)

        curLabel = element.get('label')
        startTime = endTime

    labFileName = labelFile[:-3] + 'lab'
    f = open(labFileName, 'w')
    f.writelines(lines)
    f.close()


# Check File Existence
count = 0
for labfile in Labfiles:
    audiofilename = destdir + labfile[len(curdir):-4]
    samples = 0
    error = []
    changes = []

    for ext in AUDIO_EXT:
        if os.path.exists(audiofilename + ext):
            if ext == '.mp3':
                mp3 = mad.MadFile(audiofilename + ext)
                samples = mp3.total_time()*mp3.samplerate()/1000

            if ext == '.wav':
                wav = wave.open(audiofilename + ext, 'r')
                samples = wav.getnframes()
                wav.close()

            if not samples == 0:
                # print labfile, samples
                try:
                    newXML, errors, changes = checkSVL(labfile, samples)
                except:
                    print labfile + " Error !!!"

                if errors:
                    error.extend(errors)
                # make backup file.

                break
            else:
                error.append('Audio file has problem')
    else:
        error.append('No corresponding audio file')
        # try:
        #     newXML, errors, changes = checkSVL(labfile, 9999999999)
        # except:
        #     print labfile + " Error !!!"

        if errors:
            error.extend(errors)


    if newXML:
        cmd = 'mv %s %s' %(labfile, labfile+'.bak')
        os.system(cmd)
        f = open(labfile, 'w')
        f.writelines(newXML)
        f.close()

    if error or changes:
        print labfile
        if error:
            for err in error:
                print err
            print ''
        if changes:
            for chg in changes:
                print chg
            print ''


    svl2lab(labfile)
