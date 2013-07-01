#!/usr/bin/python

"""regionchecker - detect which region this iso is currently set for"""

import io
import argparse

PARSER = argparse.ArgumentParser(description='MegaCd region checker')
PARSER.add_argument('filename', metavar='filename', type=str,
                   help='cd image to read')

ARGS = PARSER.parse_args()

USA = '43fa000a4eb803646000057a60'
JAP = '21fc00000280fd024bf900a120'
EUR = '43fa000a4eb803646000056460'

DATAFILE = io.FileIO(ARGS.filename,'r')

DATAFILE.seek(0x200)

STRIP = DATAFILE.read(13)

if STRIP.encode('hex') == USA:
    print 'USA'
if STRIP.encode('hex') == JAP:
    print 'JAP'
if STRIP.encode('hex') == EUR:
    print 'EUR'
