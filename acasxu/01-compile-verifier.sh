#!/usr/bin/env bash

SCRIPTDIR="${BASH_SOURCE[0]}"
SCRIPTDIR="$(dirname "${SCRIPTDIR}")"

VOTE_DIR=$SCRIPTDIR/../VoTE

pushd ${VOTE_DIR}; ./bootstrap.sh && ./configure && make; popd
cc -static -L $VOTE_DIR/lib/.libs \
   -I $VOTE_DIR/inc \
   $SCRIPTDIR/verifier.c \
   -lvote -lm \
   -o $SCRIPTDIR/verifier || exit 1

