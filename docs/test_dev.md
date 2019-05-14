
# Testing and Development
A large portion of the repository is dedicated to corpus extraction and model creation.  Scripts that facilitate these tasks are located in the `test` and `scripts` directories.

## Testing
Testing files are in the `tests` directory

The `auto` subdirectory, contains a set of unit-tests to exercise and verify system operation.  The script `RunAllUnitTests.py`, executes all tests in the `auto` directory and prints out a final summary.  Note that it is setup to run from the `test` directory.  If you try to run it from elsewhere, likely it won't find the individual test files without some modification.

The `manual` directory contains various scripts used to exercise system functionality and facilitate debugging.

The `accuracy` directory contains scripts and modules used to create the [accuracy](accuracy.md) data.

## Development
Files in the `scripts` directory are predominantly used to build the resources needed to drive the run-time system.  Directories are numbered to indicate the order they need to be run.  Likewise, scripts in the directories have a numerical prefix to indicate order.  Additional libraries are required to run these including, `nltk`, `keras` and a Keras backend such as `tensorflow`.

There is a README.txt file in the `01_BuildLexicon` directory with information on how to get started.  Generally you will need to..

* Create a `data_repo` directory or link in the main directory
* Download the various corpora used for building the resource (see the README.txt)
* Review the `lemmatizer\config.py` file.  This contains the location of data read and written.  You will likely need to change the source locations for things like the Gutenberg and Billion Word Corpora.

There is no formal documentation for these scripts but there is a lot of comments inside the code.  If you wish to dig into these files, plan to spend some time learning how the code operates as they are not intended for use by a casual end-user.
