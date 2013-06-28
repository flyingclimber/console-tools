#!/usr/bin/python

"""readsystemid - Simple MegaCD system id reader"""

SECTORSIZE = 2048
SECTORSTOREAD = 1

SECTORDATA = file("test.iso",'rb').read(SECTORSTOREAD*SECTORSIZE)
DATAFILE = open("header",'w')

DATAFILE.write(SECTORDATA)
DATAFILE.close()
