#!/bin/bash

if [ "$(uname -m)" = "x86_64" ]; then
    export PATH=$PATH:/reader/jdk-19.0.1+10-jre/bin
elif [ "$(uname -m)" = "aarch64" ]; then
    export PATH=$PATH:/reader/jdk-19.0.2+7-jre/bin
fi

exec python main.py