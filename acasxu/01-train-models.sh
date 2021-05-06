#!/usr/bin/env bash

SCRIPTDIR="${BASH_SOURCE[0]}"
SCRIPTDIR="$(dirname "${SCRIPTDIR}")"

VOTE_DIR=$SCRIPTDIR/../VoTE
export PYTHONPATH=$VOTE_DIR/bindings/python

make -C $SCRIPTDIR/nnet || exit 1

for aprev in {1,2,3,4,5}; do
    for tau in {1,2,3,4,5,6,7,8,9}; do
	$SCRIPTDIR/train.py \
	    -v \
	    -n 1000000 \
	    -B 200 \
	    -d 10 \
	    -a $aprev \
	    -t $tau \
	    -o $SCRIPTDIR/models/ACASXU_${aprev}_${tau}.json || exit 1
    done
done
