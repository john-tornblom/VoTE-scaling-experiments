#!/usr/bin/env bash

SCRIPTDIR="${BASH_SOURCE[0]}"
SCRIPTDIR="$(dirname "${SCRIPTDIR}")"

for PROP in $(seq 1 10); do
    echo "INFO:verify-acasxu:Analyzing property $PROP"
    /usr/bin/time \
	-f '%es real, %Us user, %Ss kernel, %M mmem' \
	$SCRIPTDIR/verify-property-$PROP.sh \
	> $SCRIPTDIR/logs/property-$PROP.log 2>&1 \
	|| exit 1
done

