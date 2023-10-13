#!/bin/bash

FUZZER_NAME='Recfuzz'
. $(dirname $0)/common-setup.sh

if [ -z "$2" ] #fuzzing part
then ./recfuzz -qS -i seed -o output -s random-only -f "./$1 $2" -t "$4" > recfuzz.log #for stdin
else ./recfuzz -q -i seed -o output -s random-only -f "./$1 $2" -t "$4" > recfuzz.log
fi
wait

if [ -z "$2" ] #dryrun part
then ./recfuzz -qS -i output/crashes/ -f "./$1 $2"
else ./recfuzz -q -i output/crashes/ -f "./$1 $2"
fi

wait

cp ./dryrun-out.log ./output/dryrun-out.log

. $(dirname $0)/common-postproc.sh
