#!/bin/bash

set -e
set -x

BASE_DIR=/home/pymor/src

# Using
#   export PYTHONPATH=${BUILD_DIR}/lib:${BASE_DIR}/src:${PYTHONPATH}
# will fail with empty PYTHONPATH as the empty string
# after ':' will be treated as the current directory
# in which the operator module is imported instead of
# the operator module from stdlib.
cd ${BASE_DIR}

pip install pytest
pip install .

cd ${BASE_DIR}/src/
xvfb-run -a pytest test/demo.py
