#!/usr/bin/python

"""regionchecker - detect which region this iso is currently set for"""

import io
import argparse

PARSER = argparse.ArgumentParser(description='MegaCd region checker')
PARSER.add_argument('filename', metavar='filename', type=str,
                   help='cd image to read')

ARGS = PARSER.parse_args()

USA = 0x43
JAP = 0x21
EUR = 0x43

DATAFILE = io.FileIO(ARGS.filename,'r')

DATAFILE.seek(0x20b)

STRIP = DATAFILE.read(1)

if STRIP == chr(0x7a): 
    print 'USA'
if STRIP == chr(0xa1):
    print 'JAP'
if STRIP == chr(0x64):
    print 'EUR'
