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

    readsystemid - simple MegaCD header reader
'''

import io
import argparse

PARSER = argparse.ArgumentParser(description='Simple MegaCd header reader')
PARSER.add_argument('filename', metavar='filename', type=str,
                   help='cd image to read')

ARGS = PARSER.parse_args()

DATAFILE = io.FileIO(ARGS.filename,'r')

# System ID
DISCIDENTIFIER = DATAFILE.read(0x10)
SEGASYSTEMDISC = DATAFILE.read(0xB)
DATADISC = DATAFILE.read(16)

DATAFILE.seek(0x030)

IP_ADDRESS = DATAFILE.read(4)
IP_LOAD_SIZE = DATAFILE.read(4)
IP_ENTRY = DATAFILE.read(4)
IP_WORK_SIZE = DATAFILE.read(4)
SP_ADDRESS = DATAFILE.read(4)
SP_LOAD_SIZE = DATAFILE.read(4)
SP_ENTRY = DATAFILE.read(4)
SP_WORK_SIZE = DATAFILE.read(4)

DATAFILE.seek(0x100)

# Disc ID
SYSTEMNAME = DATAFILE.read(0x10)
COPYRIGHT = DATAFILE.read(0x10)
DOMESTICNAME = DATAFILE.read(0x30)
OVERSEASNAME = DATAFILE.read(0x30)
GAMETYPE = DATAFILE.read(0x3)
GAMEREFERENCE = DATAFILE.read(0x7)
GAMEVERSION = DATAFILE.read(0x2)
GAMEVERSIONNUMBER = DATAFILE.read(0x2)

DATAFILE.seek(0x190)

IODATA = DATAFILE.read(0x10)

DATAFILE.seek(0x1BC)

MODEM = DATAFILE.read(10)

DATAFILE.seek(0x1F0)

COUNTRY = DATAFILE.read(0x10)

print '==== System ID ===='
print 'Disc identifier: ' + DISCIDENTIFIER
print 'System type: ' + SEGASYSTEMDISC
print 'Data disc: ' + DATADISC

print 'IP_Address: ' + SP_ADDRESS.encode('hex')
print 'IP_Load_Size: ' + SP_LOAD_SIZE.encode('hex')
print 'IP_Entry: ' + SP_ENTRY.encode('hex')
print 'IP_Work_Size: ' + SP_WORK_SIZE.encode('hex')
print 'SP_Address: ' + SP_ADDRESS.encode('hex')
print 'SP_Load_Size: ' + SP_LOAD_SIZE.encode('hex')
print 'SP_Entry: ' + SP_ENTRY.encode('hex')
print 'SP_Work_Size: ' + SP_WORK_SIZE.encode('hex')


print ''
print '==== Disc ID ===='
print 'System name: ' + SYSTEMNAME
print 'Copyright: ' + COPYRIGHT
print 'Domestic name: ' + DOMESTICNAME.decode('shift-jis')
print 'Overseas name: ' + OVERSEASNAME
print 'Game type: ' + GAMETYPE
print 'Game reference: ' + GAMEREFERENCE
print 'Game version: ' + GAMEVERSION
print 'Game version number: ' + GAMEVERSIONNUMBER
print 'IODATA: ' + IODATA
print 'Modem: ' + MODEM
print 'Country: ' + COUNTRY

DATAFILE.close()
