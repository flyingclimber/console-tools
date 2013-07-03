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

def _findemptyregions():
    '''_findemptyregions - scans an ISO for LENGTH byte to find zeros or
        spaces
    '''
    zero = '\x00\x00\x00\x00\x00\x00\x00\x00'
    space = '\x20\x20\x20\x20\x20\x20\x20\x20'
    length = 8
    found = False

    DATAFILE.seek(0)
    byte = DATAFILE.read(length)

    while byte:
        if byte == zero or byte == space:
            if found != True:
                start = DATAFILE.tell() - length
                found = True
        elif found == True:
            end = DATAFILE.tell() - length
            print start, "-", end, "|", end - start
            found = False

        byte = DATAFILE.read(8)

DATAFILE.seek(0x200)

STRIP = DATAFILE.read(13)

if STRIP.encode('hex') == USA:
    print 'USA'
if STRIP.encode('hex') == JAP:
    print 'JAP'
if STRIP.encode('hex') == EUR:
    print 'EUR'

_findemptyregions()
