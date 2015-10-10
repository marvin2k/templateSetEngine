#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

O=./testbf/
T=$DIR/../templates/
# use "conversion" feature in template
DB="$T"bla.yaml
# for testing: directly giving some yaml
#DB="$O"to.yaml
# the tool...
PYRATOOL=$DIR/pyratemp-0.3.2/pyratemp_tool.py

# need "XML_DB" switch because of automatic conversion... using "DB" as switch without conversion visible would be better
make O=$O XML_DB=$DB B=$B T=$T PYRATOOL=$PYRATOOL \
    -f "$DIR/Makefile" "$@"
