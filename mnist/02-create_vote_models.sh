#!/usr/bin/env bash

SCRIPTDIR="${BASH_SOURCE[0]}"
SCRIPTDIR="$(dirname "${SCRIPTDIR}")"

SILVA2VOTE=$SCRIPTDIR/tools/silva2vote.py

for SILVA_MODEL in $SCRIPTDIR/models/*.silva; do
    VOTE_MODEL=${SILVA_MODEL::-5}vote
    echo "Creating $VOTE_MODEL"
    $SILVA2VOTE < $SILVA_MODEL > $VOTE_MODEL || exit 1
done
