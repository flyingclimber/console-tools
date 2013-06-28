#!/usr/bin/python

"""readsystemid - Simple MegaCD system id reader"""

import io

DATAFILE = io.FileIO('test.iso','r')

DISCIDENTIFIER = DATAFILE.read(0x10)
SEGASYSTEMDISC = DATAFILE.read(0xB)
DATADISC = DATAFILE.read(16)

DATAFILE.seek(0x100)

SYSTEMNAME = DATAFILE.read(0x10)
COPYRIGHT = DATAFILE.read(0x10)
DOMESTICNAME = DATAFILE.read(0x30)
OVERSEASNAME = DATAFILE.read(0x30)

DATAFILE.seek(0x1F0)

COUNTRY = DATAFILE.read(0x10)

print 'Disc identifier: ' + DISCIDENTIFIER
print 'System type: ' + SEGASYSTEMDISC
print 'Data disc: ' + DATADISC
print 'System name: ' + SYSTEMNAME
print 'Copyright: ' + COPYRIGHT
print 'Domestic name: ' + DOMESTICNAME
print 'Overseas name: ' + OVERSEASNAME
print 'Country: ' + COUNTRY

DATAFILE.close()
