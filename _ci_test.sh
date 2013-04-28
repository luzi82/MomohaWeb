#!/bin/bash

cp src/MomohaWeb/secret.py.example src/MomohaWeb/secret.py || exit 1
./dev_test.sh || exit 1
