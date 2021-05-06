#!/usr/bin/env bash

SCRIPTDIR="${BASH_SOURCE[0]}"
SCRIPTDIR="$(dirname "${SCRIPTDIR}")"

VOTE2SILVA=$SCRIPTDIR/tools/vote2silva.py
SILVA2VOTE=$SCRIPTDIR/tools/silva2vote.py

for FILE in $SCRIPTDIR/models/*.vote; do
    echo "Validating VoTE2Silva for $FILE"
    $VOTE2SILVA < $FILE | $SILVA2VOTE | diff $FILE -
    RC=$?
    if [ $RC -ne 0 ]; then
	echo "Error: discrepancy detected in the translation of $FILE"
	exit $RC
    fi
done

for FILE in $SCRIPTDIR/models/*.silva; do
    echo "Validating Silva2VoTE for $FILE"
    $SILVA2VOTE < $FILE | $VOTE2SILVA | diff $FILE -
    RC=$?
    if [ $RC -ne 0 ]; then
	echo "Error: discrepancy detected in the translation of $FILE"
	exit $RC
    fi
done
