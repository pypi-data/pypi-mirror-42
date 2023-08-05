#!/usr/bin/env bash
set -e -v  # exit immediately on error, and print each line as it executes

# This script runs the test suite on the emulator

NAME=$0
COMMAND=$1

if [[ "$COMMAND" == "install" ]]; then
    conda install --quiet matplotlib mkl numpy scipy tensorflow
    pip install "git+https://github.com/nengo/nengo-dl.git@conv_transform"
    pip install -e .[tests]
elif [[ "$COMMAND" == "script" ]]; then
    coverage run -m pytest nengo_loihi -v --duration 20 --plots --color=yes
    coverage run -a -m pytest --pyargs nengo -v --duration 20 --color=yes
    coverage report -m
elif [[ "$COMMAND" == "after_success" ]]; then
    eval "bash <(curl -s https://codecov.io/bash)"
else
    echo "$NAME does not define $COMMAND"
fi
