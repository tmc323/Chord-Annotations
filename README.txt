MARL (Music and Audio Research Lab) at NYU Music Technology program
is happy to release hundreds of human annotated chord labels to MIR researchers.

You can download the latest version of label files from our project repository.

   git://github.com/tmc323/Chord-Annotations.git

to download the files, you will need to install git, then type below in your terminal:
   git clone git://github.com/tmc323/Chord-Annotations.git

All chord transcriptions are manually annotated by NYU undergraduate music students,
and each song has been double checked by two different annotators.

Our dataset provides the chord transcriptions for all 100 songs of RWC Popular Music database ( http://staff.aist.go.jp/m.goto/RWC-MDB/rwc-mdb-p.html ).
In addition, up to now, we provide 195 songs out of 8752 songs from the uspop2002 Pop Music data set ( http://labrosa.ee.columbia.edu/projects/musicsim/uspop2002.html ).
The number of transcriptions will be gradually increased.

So, please check the repository regularly.


* Format
  Chord labels are annotated following Christopher Harte's chord notation rules that used in his famous Beatle dataset.

  The annotations are provided in two different file formats.

  - .lab files contain text format chord annotations in this form:

     start_time end_time chord_label

  - .svl files are for sonic-visualiser.


* Lists of chord annotated songs:
  You can check the list of annotated song titles in these files.

  RWC_Pop_Chords.txt
  uspopLabels.txt


* Audio files

  We provide only chord annotations, no audio files.
  You can get the audio files or CD information from:

  - RWC_Pop audios (wavs)
    Please contact Dr. Masataka Goto at
    http://staff.aist.go.jp/m.goto/RWC-MDB

  - uspop audio (mp3s)
    Please contact LabROSA
    http://labrosa.ee.columbia.edu/projects/musicsim/uspop2002.html

* Please help us
  The chord labels may have errors.
  If you found any error, inaccuracy of any kind, please let us know to fix it.
  Any comments and feedback is also very helpful to improve the quality of the database.

  You can also participate this project. Please contact us, and get your permission to access the repository.

* Contact

  Taemin Cho <tmc323@nyu.edu>

  MARL (Music and Audio Research Lab)
  Music Technology, New York University
  http://marl.smusic.nyu.edu

* Special Thanks to these Annotators:

  - RWC-pop
    Joshua H Chang <jhc418@nyu.edu>
    Daniel Cicourel Hanley <dcicourelh@gmail.com>
    Daniel Lipsitz <lipsitz@nyu.edu>
    Aled I Roberts <air226@nyu.edu>

  - uspopLabels
    Nocolas Dooley <nsd250@nyu.edu>
    Travis Kaufman <tmk272@nyu.edu>
