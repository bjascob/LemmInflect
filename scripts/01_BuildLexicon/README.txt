
Setup prior to running scripts
------------------------------
The file lemminflect/config.py contains the definition of the locations used by these scripts to
store temporary and project related data files.  The temporary files all reside in the directory
"data_repo" which is defined relative to the config.py file (one up from it).  You will need to
create that directory prior to running any of the setup scripts here.

It's assumed that you're running the scripts using a local download of lemminflect, not an
installed instance.  The line `sys.path.insert(0, '../..')` at the top of each file is intended
to force the use of the lemminflect library that's part of the local download, and not use
the installed instance.  If you're doing something different you may need to modify paths in
lemminflect.config.py so the scripts can find the data files.


Obtaining source data used in the scripts
-----------------------------------------
All data here is free-open-source and can be downloaded from the web.

CreateEnglishWordSet.py
The English word lists used here are standard installs in Ubuntu 18.04.  They're from package
wamerican and wbritish.  There are also larger list like wamerican-large, -huge and -insane
that are not installed.
The Debian English word lists are built from SCOWL (Spell-Checker Oriented Word Lists)
If you're not on a Debian distribution you should still be able to search and download the
raw packages and extract the needed text files.

GutenbergToUnigrams.py
This script uses a portion of the Gutenberg corpus downloadable from
https://web.eecs.umich.edu/~lahiri/gutenberg_dataset.html
The corpus used is 3,036 English books and is 1.2GB in size
This is not the full Gutenberg corpus but it's a "cleaned" subset of the 58,000 some
books available from https://www.gutenberg.org/
You'll need to modify lemminflect.config.gutenberg_dir to specify the corpus location

BWCorpToUnigrams.py
This script uses the Billion word corpus.
See https://code.google.com/archive/p/1-billion-word-language-modeling-benchmark
for a description of the data
To download do `wget http://statmt.org/wmt11/training-monolingual.tgz` or use a browser
The download is 9.9GB and contains multiple languages.  To extract the English portions do..
tar --extract -v --file training-monolingual.tgz --wildcards training-monolingual/news.20??.en.shuffled
This portion of the extracted data is 14GB.  If you extract the entire file, it's about 25GB.
You'll need to modify lemminflect.config.bwcorp_dir to specify the corpus location

ExtractFormsTableFromLexicon
This script uses the NIH's SPECIALIST Lexicon available from..
https://lsg3.nlm.nih.gov/LexSysGroup/Projects/lexicon/current/web/index.html
Follow the links to the latest release (2019 as of this README file) and download "Lexicon (text)"
There is also an excellent PDF explaining the data format and inflection rules. Download at..
https://lexsrv3.nlm.nih.gov/Specialist/Docs/Papers/00_NLM_Lexicon.pdf
