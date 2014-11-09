#!/usr/bin/python

'''
    console-tools - Tools for various consoles

    Copyright (C) 2014, Tomasz Finc <tomasz@gmail.com>

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

    checksum - multi function MegaDrive rom checksum tool
'''

import io, os, binascii
import argparse

PARSER = argparse.ArgumentParser(
    description='Simple MegaDrive checksum reader/writter')
PARSER.add_argument('filename', metavar='filename', type=str,
                        help='rom image to read')
PARSER.add_argument('-f', '--fix', action="store_true",
                    help='fix checksum')
PARSER.add_argument('-o', help='output filename')

ARGS = PARSER.parse_args()

ROMBEGIN = 0x0
CHECKSUMLOCATION = 0x18E
GAMECODEBEGIN = 0x200

DATAFILE = io.FileIO(ARGS.filename,'r')

def _calculatechecksum():
    '''_calculatechecksum - calculate checksum and return high 16 bits'''

    DATAFILE.seek(GAMECODEBEGIN)
    checksum = 0
    
    while True:
        snip = DATAFILE.read(1)
        if not snip: 
            break
        
        checksum += ord(snip) * 256
        checksum += ord(DATAFILE.read(1))
        
    return int(checksum & 0xFFFF)

def _readheaderchecksum():
    '''_readheaderchecksum - read header checksum value'''

    DATAFILE.seek(CHECKSUMLOCATION)
    checksum = DATAFILE.read(2)

    return int(binascii.hexlify(checksum), 16)

def _fixheaderchecksum(calculatedchecksum):
    '''_fixheaderchecksum - create a copy rom with new calculatedchecksum'''

    if ARGS.o:
        outputfile = ARGS.o
    else:
        filename, fileextension = os.path.splitext(os.path.basename(DATAFILE.name))
        outputfile = filename + " fixed" + fileextension

    DATAFILE.seek(ROMBEGIN)

    copy = io.FileIO(outputfile, 'wb')
    copy.write(DATAFILE.read(CHECKSUMLOCATION))
    copy.write(binascii.unhexlify(format(calculatedchecksum,'x')))
    DATAFILE.read(2)
    copy.write(DATAFILE.read())
    copy.close()

def _main():
    '''_main - master of all'''

    headerchecksum = _readheaderchecksum()
    calculatedchecksum = _calculatechecksum()
    
    print "Header: " + hex(headerchecksum)
    print "Calculated: " + hex(calculatedchecksum)
    
    if ARGS.fix:
        if headerchecksum == calculatedchecksum:
            print ("Checksums match. Nothing to do")
        else:
            _fixheaderchecksum(calculatedchecksum)

    DATAFILE.close()
    
_main()