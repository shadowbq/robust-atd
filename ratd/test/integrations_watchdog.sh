#!/usr/bin/env bash

if [[ $PWD =~ robust-atd$ ]]; then

    # Cleanup
    rm -rf tmp/preprocess
    rm -rf tmp/errors
    rm -rf tmp/clean
    rm -rf tmp/dirty
    rm -rf tmp/reports

    # Holding & Queue
    mkdir -p tmp/wait
    mkdir -p tmp/preprocess

    # Bin drops
    mkdir -p tmp/errors
    mkdir -p tmp/clean
    mkdir -p tmp/dirty

    # Report drops
    mkdir -p tmp/reports

    #
    cp tmp/wait/*.exe tmp/preprocess/.
    robust-convict.py -n -a 26 -c ./tmp/clean/ -x ./tmp/dirty/ -r ./tmp/reports/ -z ./tmp/errors/ -d ./tmp/preprocess -j 10 -t zip -v -e

fi
