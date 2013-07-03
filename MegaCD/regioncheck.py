#!/usr/bin/python

'''
    console-tools - Tools for various consoles

    Copyright (C) 2013, Tomasz Finc <tomasz@gmail.com>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

    regionchecker - detect which region this iso is currently set for
'''

import io, os
import argparse

PARSER = argparse.ArgumentParser(description='MegaCd region checker')
PARSER.add_argument('filename', metavar='filename', type=str,
                   help='cd image to read')

ARGS = PARSER.parse_args()

USA = '43fa000a4eb803646000057a60'
JAP = '21fc00000280fd024bf900a120'
EUR = '43fa000a4eb803646000056460'

DATAFILE = io.FileIO(ARGS.filename,'r')

def _findemptyregions(filebegin=0, fileend=os.stat(ARGS.filename).st_size):
    '''_findemptyregions - scans an ISO for LENGTH byte to find zeros or
        spaces
    '''

    zero = '\x00\x00\x00\x00\x00\x00\x00\x00'
    space = '\x20\x20\x20\x20\x20\x20\x20\x20'
    length = 8
    found = False

    DATAFILE.seek(filebegin)
    byte = DATAFILE.read(length)

    while DATAFILE.tell() != fileend:
        if byte == zero or byte == space:
            if found != True:
                start = DATAFILE.tell() - length
                found = True
        elif found == True:
            end = DATAFILE.tell() - length
            print start, "-", end, "|", end - start
            found = False

        byte = DATAFILE.read(8)

def _findregion():
    '''_findregion - find the region of a megacd game'''

    DATAFILE.seek(0x200)
    strip = DATAFILE.read(13)

    if strip.encode('hex') == USA:
        print 'USA'
    if strip.encode('hex') == JAP:
        print 'JAP'
    if strip.encode('hex') == EUR:
        print 'EUR'

def _main():
    _findregion()
    _findemptyregions()

_main()
