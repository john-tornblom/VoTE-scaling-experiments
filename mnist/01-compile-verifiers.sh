#!/usr/bin/env bash

SCRIPTDIR="${BASH_SOURCE[0]}"
SCRIPTDIR="$(dirname "${SCRIPTDIR}")"

VOTE_DIR=$SCRIPTDIR/../VoTE
SILVA_DIR=$SCRIPTDIR/../silva


pushd ${VOTE_DIR}; ./bootstrap.sh && ./configure; popd
make -C ${VOTE_DIR} clean
make -C ${VOTE_DIR}
gcc -static -L $VOTE_DIR/lib/.libs \
    -I $VOTE_DIR/inc \
    $SCRIPTDIR/tools/vote.c \
    -lvote -lpthread -lm \
    -o $SCRIPTDIR/tools/vote || exit 1


make -C ${SILVA_DIR}/src clean
make -C ${SILVA_DIR}/src
cp $SILVA_DIR/src/silva $SCRIPTDIR/tools/silva || exit 1


