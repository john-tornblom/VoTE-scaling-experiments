#!/usr/bin/env bash

SCRIPTDIR="${BASH_SOURCE[0]}"
SCRIPTDIR="$(dirname "${SCRIPTDIR}")"

VERIFIER=$SCRIPTDIR/verifier

PASS=0
FAIL=0

aprev=4
tau=5

$VERIFIER -p10 $SCRIPTDIR/models/ACASXU_${aprev}_${tau}.json
RES=$?

if [ $RES -eq 1 ]; then
    PASS=$((PASS+1))
fi

if [ $RES -eq 0 ]; then
    FAIL=$((FAIL+1))
fi

echo "property:10"
echo "PASS:$PASS"
echo "FAIL:$FAIL"
