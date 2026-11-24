#!/bin/bash

export PINI="NO"
if [ "$#" -gt 0 ]; then
    export PINI=$1
fi

export RVAL="VAL"
if [ "$#" -gt 1 ]; then
    export RVAL=$2
fi

# HASH defaults to # if PINI is NO.
export HASH="#"
if [ ${PINI} = "YES" ]; then
    # It defaults to nothing if PINI is YES.
    # The empty string cannot be used as it creates an empty macro.
    export HASH=" "
fi

if [ "$#" -gt 2 ]; then
    export HASH=$3
fi

# Launch the IOC
./st.cmd
