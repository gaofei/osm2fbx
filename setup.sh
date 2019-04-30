#!/bin/env bash
PYTHONPATH=$(which python)
PYTHONBIN="$(dirname "$PYTHONPATH")"
PYTHONHOME="$(dirname "$PYTHONBIN")"
PYTHONLIB=$PYTHONHOME"/lib"

echo "==========================================================================="
echo "PYTHONPATH: "$PYTHONPATH
echo "PYTHONBIN: "$PYTHONBIN
echo "PYTHONHOME: "$PYTHONHOME
echo "PYTHONLIB: "$PYTHONLIB
echo "==========================================================================="

mkdir .tmp
cd .tmp
wget http://download.autodesk.com/us/fbx/2019/2019.0/fbx20190_fbxpythonsdk_linux.tar.gz
tar -xvzf fbx20190_fbxpythonsdk_linux.tar.gz
yes yes | ./fbx20190_fbxpythonsdk_linux
cp ./lib/Python27_ucs4_x64/* $PYTHONLIB"/python2.7"
cd .. && rm -rf .tmp


echo "==========================================================================="
echo " INSTALL FINISHED"
echo "==========================================================================="
