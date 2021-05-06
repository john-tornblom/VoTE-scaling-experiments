#!/usr/bin/env bash

SCRIPTDIR="${BASH_SOURCE[0]}"
SCRIPTDIR="$(dirname "${SCRIPTDIR}")"

$SCRIPTDIR/extract_results.py > $SCRIPTDIR/results.csv

