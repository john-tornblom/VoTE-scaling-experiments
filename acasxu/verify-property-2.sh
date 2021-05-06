#!/usr/bin/env bash

SCRIPTDIR="${BASH_SOURCE[0]}"
SCRIPTDIR="$(dirname "${SCRIPTDIR}")"

VERIFIER=$SCRIPTDIR/verifier

PASS=0
FAIL=0

for aprev in {2,3,4,5}; do
    for tau in {1,2,3,4,5,6,7,8,9}; do
	$VERIFIER -p2 $SCRIPTDIR/models/ACASXU_${aprev}_${tau}.json
	RES=$?

	if [ $RES -eq 1 ]; then
	    PASS=$((PASS+1))
	fi

	if [ $RES -eq 0 ]; then
	    FAIL=$((FAIL+1))
	fi
    done
done

echo "property:2"
echo "PASS:$PASS"
echo "FAIL:$FAIL"