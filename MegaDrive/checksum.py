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

    checksum - calculate the checksum for a Genesis ROM
'''

import io
import argparse

PARSER = argparse.ArgumentParser(
    description='Simple MegaDrive checksum reader/writter')

PARSER.add_argument('filename', metavar='filename', type=str,
                        help='rom image to read')

ARGS = PARSER.parse_args()

DATAFILE = io.FileIO(ARGS.filename,'r')

def _findchecksum():
    '''Calculate checksum and return high 16bits'''
    DATAFILE.seek(0x200)
    checksum = 0
    
    while True:
        snip = DATAFILE.read(1)
        if not snip: 
            break
        
        checksum += ord(snip) * 256
        checksum += ord(DATAFILE.read(1))
        
    return checksum & 0xFFFF

def _main():
    '''MAIN'''
    
    checksum = _findchecksum()
    
    print "Checksum: " + hex(checksum)
    DATAFILE.close()
    
_main()