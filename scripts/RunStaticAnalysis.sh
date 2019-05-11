#!/bin/sh

# Static analysis checker'

# Disable the following checks.
# see https://docs.pylint.org/en/1.6.0/features.html
DISABLES="--disable=C0326,R0205,R1705,R1710,R0911,R0912,R0903,C0103,C0111,R0801,W0201,R0913,W0401"\
",W0201,R0902,R0915,W1401,R0914,W0235,C0411,R1716"
#DISABLES=""

# Run the command
pylint $DISABLES ../lemminflect
