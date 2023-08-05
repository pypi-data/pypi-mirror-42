#!/bin/bash

PYV="3.5"
FAUCETHOME=`dirname $0`"/../.."
TMPDIR=`mktemp -d -p /var/tmp`
CONFIG="$FAUCETHOME/setup.cfg"
# TODO: halt flag must be 2014 parallel compatible.
PARARGS="parallel --delay 1 --bar --halt 1 -j 2"
PYTYPE=`which pytype`
PYTYPEARGS="python$PYV $PYTYPE --config $CONFIG -o $TMPDIR/{/} {}"
PYHEADER=`head -1 $PYTYPE`
SRCFILES="$FAUCETHOME/tests/codecheck/src_files.sh $*"
echo "Using $PYTYPE (header $PYHEADER)"

$SRCFILES | shuf | $PARARGS $PYTYPEARGS || exit 1
rm -rf $TMPDIR
