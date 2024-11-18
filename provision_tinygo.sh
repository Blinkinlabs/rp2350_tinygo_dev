#!/usr/bin/bash
#
# Note: Run this from within the container!

cd /build
#git clone git@github.com:Blinkinlabs/tinygo.git
git clone --branch rp2350-experiments https://github.com/Blinkinlabs/tinygo.git
cd tinygo
git submodule update --init --recursive
cd /build/tinygo
go install
make llvm-source
make gen-device
