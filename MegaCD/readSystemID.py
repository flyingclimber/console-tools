#!/usr/bin/python

sectorSize = 2048;
sectorsToRead = 1;

sectorData = file("test.iso",'rb').read(sectorsToRead*sectorSize);
dataFile = open("header",'w');

dataFile.write(sectorData);
dataFile.close();
