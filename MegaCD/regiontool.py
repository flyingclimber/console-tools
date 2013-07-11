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
PARSER.add_argument('-o',
                    help='name of new region')

ARGS = PARSER.parse_args()

# Regions we support converting to/from
USAREGION = 'USA'
JAPREGION = 'JAP'
EURREGION = 'EUR'

# Property files. Currently not bundled
USAPROPBIN = 'us_prop.bin'
JAPPROPBIN = 'jp_prop.bin'
EURPROPBIN = 'eu_prop.bin'

# File handles
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

def _findregion(sourceiso=io.FileIO):
    '''_findregion - find the region of a MegaCD game'''

    sourceiso.seek(0x200)
    striplength = 13
    strip = sourceiso.read(striplength)

    usap = io.FileIO(USAPROPBIN, 'r')
    japp = io.FileIO(JAPPROPBIN, 'r')
    eurp = io.FileIO(EURPROPBIN, 'r')

    if strip == usap.read(striplength):
        region = USAREGION
    elif strip == japp.read(striplength):
        region = JAPREGION
    elif strip == eurp.read(striplength):
        region = EURREGION
    else:
        region = None

    usap.close()
    japp.close()
    eurp.close()

    return region

def _convertregion(newregion=str, oldregion=str):
    '''_convertregions - convert from one region to another'''

    if ARGS.o:
        outputfile = ARGS.o
    else:
        filename, fileextension = os.path.splitext(DATAFILE.name)
        outputfile = filename + newregion + fileextension

    CONVERTEDISO = io.FileIO(outputfile, 'w')

    if newregion == USAREGION:
        if oldregion == EURREGION:
            _copybase(DATAFILE, CONVERTEDISO, EURREGION, USAREGION)
        elif oldregion == JAPREGION:
            _copybase(DATAFILE, CONVERTEDISO, JAPREGION, USAREGION)
    elif newregion == JAPREGION:
        if oldregion == USAREGION:
            _copybase(DATAFILE, CONVERTEDISO, USAREGION, JAPREGION)
        if oldregion == EURREGION:
            _copybase(DATAFILE, CONVERTEDISO, EURREGION, JAPREGION)
    elif newregion == EURREGION:
        if oldregion == USAREGION:
            _copybase(DATAFILE, CONVERTEDISO, USAREGION, EURREGION)
        if oldregion == JAPREGION:
            _copybase(DATAFILE, CONVERTEDISO, JAPREGION, EURREGION)
    else:
        print "Invalid region"

def _findnextgap(start):
    '''_findnextgap - given a location find the next 8byte gap'''
    
    DATAFILE.seek(start)
    count = 0
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

def _getpropbin(region):
    '''_getpropbin - given a region return the corresponding propbin'''

    if region == USAREGION:
        return USAPROPBIN
    elif region == JAPREGION:
        return JAPPROPBIN
    elif region == EURREGION:
        return EURPROPBIN
    else:
        print "Unknown region. Aborting"
        sys.exit()

def _copybase(sourceiso=io.FileIO, newiso=io.FileIO, oldregion=str,
        newregion=str):
    '''_copybase - build the base image'''

    baselength = 512

    propbin = _getpropbin(newregion)
    oldpropbin = _getpropbin(oldregion)

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
        oldregion = _findregion(DATAFILE)

        if oldregion != newregion:
            _convertregion(newregion, oldregion)
        else:
            print "No point in converting to the same region"
    else:
        print _findregion(DATAFILE)

_main()
