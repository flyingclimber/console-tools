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

    regiontool - multi purpose MegaCD region tool
'''

import io, os, sys
import argparse

PARSER = argparse.ArgumentParser(description='MegaCd region tool')
PARSER.add_argument('filename', metavar='filename', type=str,
                    help='cd image to read')
PARSER.add_argument('-c', '--convert', action="store_true",
                    help='convert to a new region')
PARSER.add_argument('-n', choices=['USA', 'JAP', 'EUR'],
                    help='name of new region')

ARGS = PARSER.parse_args()

USA = '43fa000a4eb803646000057a60'
JAP = '21fc00000280fd024bf900a120'
EUR = '43fa000a4eb803646000056460'

DATAFILE = io.FileIO(ARGS.filename,'r')
CONVERTEDISO = io.FileIO('converted.iso','w')

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
    '''_findregion - find the region of a MegaCD game'''

    DATAFILE.seek(0x200)
    strip = DATAFILE.read(13)

    if strip.encode('hex') == USA:
        return 'USA'
    if strip.encode('hex') == JAP:
        return 'JAP'
    if strip.encode('hex') == EUR:
        return 'EUR'

def _convertregion(newregion=str, oldregion=str):
    '''_convertregions - convert from one region to another'''

    if newregion == 'USA':
        if oldregion == 'EUR':
            _copybase(DATAFILE, CONVERTEDISO, 'EUR', 'USA')
        elif oldregion == 'JAP':
            _copybase(DATAFILE, CONVERTEDISO, 'JAP', 'USA')
    elif newregion == 'JAP':
        if oldregion == 'USA':
            _copybase(DATAFILE, CONVERTEDISO, 'USA', 'JAP')
        if oldregion == 'EUR':
            _copybase(DATAFILE, CONVERTEDISO, 'EUR', 'JAP')
    elif newregion == 'EUR':
        if oldregion == 'USA':
            _copybase(DATAFILE, CONVERTEDISO, 'USA', 'EUR')
        if oldregion == 'JAP':
            _copybase(DATAFILE, CONVERTEDISO, 'JAP', 'EUR')
    else:
        print "Invalid region"

def _findnextgap(start):
    '''_findnextgap - given a location find the next 8byte gap'''
    
    DATAFILE.seek(start)
    count = 0;
    zero = '\x00\x00'
    space = '\x20\x20'

    while count < 4:
        buffer = DATAFILE.read(2)

        if buffer == zero or buffer == space:
            count += 1
        else: 
            count = 0

    if count == 4:
        pos = DATAFILE.tell() - 8
        return pos
    else:
        return None


def _copybase(sourceiso=io.FileIO, newiso=io.FileIO, oldregion=str, 
        newregion=str):
    '''_copybase - build the base image'''

    baselength = 512

    if newregion == 'USA':
        propbin = 'us_prop.bin'
    elif newregion == 'JAP':
        propbin = 'jp_prop.bin'
    elif newregion == 'EUR':
        propbin = 'eu_prop.bin'
    else:
        print "Unknown region. Aborting"
        sys.exit()

    if oldregion == 'USA':
        oldpropbin = 'us_prop.bin'
    elif oldregion == 'JAP':
        oldpropbin = 'jp_prop.bin'
    elif oldregion == 'EUR':
        oldpropbin = 'eu_prop.bin'
    else:
        print "Unknown region. Aborting"
        sys.exit()


    # prep work #
    print "Converting from " + oldregion + " to " + newregion
    prop = io.FileIO(propbin, 'r')
    sourceiso.seek(0x40)
    gameentry = int((sourceiso.read(4)).encode('hex'))

    # write header # 
    sourceiso.seek(0) # rewind for copy
    newiso.write(sourceiso.read(baselength)) # everything up to region code

    # write new region code #
    newiso.write(prop.read()) # new region code

    # write post region code #
    loaderstart = baselength + os.stat(oldpropbin).st_size
    sourceiso.seek(loaderstart) # wind source to just past region code
    loaderend = _findnextgap(sourceiso.tell()) # get length of post region code
    sourceiso.seek(loaderstart) # re-wind source to just past region code
    newiso.write(sourceiso.read(loaderend - loaderstart))

    # write rest of iso #
    gameentry = 4096 # BUG: this should be dynamic
    sourceiso.seek(gameentry) # wind to the game code
    newiso.seek(gameentry)
    newiso.write(sourceiso.read()) # write the rest

    # cleanup #
    newiso.close()

def _main():
    '''_main - master of all'''

    if ARGS.convert:
        newregion = ARGS.n
        oldregion = _findregion()

        if oldregion != newregion:
            _convertregion(newregion, oldregion)
        else:
            print "No point in converting to the same region"
    else:
        print _findregion()

_main()
