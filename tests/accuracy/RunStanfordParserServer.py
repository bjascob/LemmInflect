#!/usr/bin/python3
import os
import sys
import time
import signal
import subprocess
from   types import SimpleNamespace

# Config info
config = SimpleNamespace()
config.log_dir      = '/tmp/'
config.snlp_log_fn  = '/tmp/snlp_server.log'
config.snlp_dir     = '/home/bjascob/Libraries/StanfordNLP/stanford-corenlp-full-2018-10-05'
config.snlp_port    = 5001


# Note stanford-corenlp-full-2018-02-27 (and 2017) does not work with openjdk,
# these only work with Oracle java8 or later.
# stanford-corenlp-full-2018-10-05 works with Java 11, but 2018-02-27 doesn't.

# Terminate the java process
def signal_handler(signum, frame):
    global gProc, gRun, gLogfile
    if gProc:
        gProc.terminate()
        st = time.time()
        while time.time()-st < 1.0:
            ret = gProc.poll()
            if ret is not None:
                break
            time.sleep(0.1)
        gRun = False
        gLogfile.close()


# Note running server takes about 3GB of RAM
if __name__ == '__main__':
    # Catch sigint
    signal.signal(signal.SIGINT, signal_handler)

    # Open the logfile
    gLogfile = sys.stdout   # default
    try:
        if not os.path.exists(config.log_dir):
            os.mkdir(config.log_dir)
        gLogfile = open(config.snlp_log_fn, 'w')
    except IOError as e:
        print(e)
        print('Unable to open logfile. Does the directory exist?')
        print('Logging to stdout')

    # Start the server
    # See https://github.com/stanfordnlp/CoreNLP/blob/master/src/edu/stanford/
    #     nlp/pipeline/StanfordCoreNLPServer.java
    working_dir = '.'
    cmd = 'java -mx4g -cp %s/* edu.stanford.nlp.pipeline.' \
          'StanfordCoreNLPServer ' % (config.snlp_dir)
    cmd += '--port %d --preload tokenize,ssplit,pos,lemma,ner,parse ' % (config.snlp_port)
    cmd += '--ner.applyFineGrained 0 '
    cmd += '--ner.buildEntityMentions 0 '
    cmd += '--quiet '    # prevents printing text.  Works for version 3.6.1 onward
    cmd = cmd.split()
    if 0:  # Redirect stderr to the log file
        gProc = subprocess.Popen(cmd, cwd=working_dir, stdout=gLogfile, stderr=gLogfile)
    else:  # Redirect stderr to /dev/null
        devnull = open(os.devnull, 'w')
        gProc = subprocess.Popen(cmd, cwd=working_dir, stdout=gLogfile, stderr=devnull)
    gLogfile.write('java process started with pid = %d\n\n' % (gProc.pid))
    gLogfile.flush()
    print('Started SNLP server. pid=', gProc.pid)

    # Run until signal handler sets this to false
    gRun = True
    while gRun:
        time.sleep(0.1)
