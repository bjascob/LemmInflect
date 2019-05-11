#!/bin/sh

echo 'Removing setup files in main directory'
cd ..
sudo rm -rf build/
sudo rm -rf dist/
sudo rm -rf lemminflect.egg-info/
