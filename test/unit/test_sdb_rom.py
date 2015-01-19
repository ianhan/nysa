#!/usr/bin/python

import unittest
import json
import sys
import os
from array import array as Array

sys.path.append(os.path.join(os.path.dirname(__file__),
                             os.pardir,
                             os.pardir))


from nysa.cbuilder import sdb_rom


class Test (unittest.TestCase):
    """Unit test for arbiter"""

    def setUp(self):
        self.dbg = False
        self.sdbrom = sdb_rom.SDBROM()

    def test_rom_buffer_length(self):
        self.sdbrom.parse_rom(rom_buffer, True)
        self.assertEqual(len(self.sdbrom), 5)

    def test_parse_rom(self):
        self.sdbrom.parse_rom(rom_buffer)

rom_buffer =   \
        "5344422D" \
        "00030100" \
        "00000000" \
        "00000000" \
        "00000002" \
        "00000000" \
        "80000000" \
        "0000C594" \
        "01000001" \
        "00000001" \
        "140F0105" \
        "6E797361" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000207" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000050" \
        "80000000" \
        "0000C594" \
        "01000001" \
        "00000001" \
        "140F0105" \
        "53444200" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000001" \
        "00000101" \
        "00000207" \
        "00000000" \
        "01000000" \
        "00000000" \
        "01000008" \
        "80000000" \
        "0000C594" \
        "00000000" \
        "00000001" \
        "140F0107" \
        "77625F67" \
        "70696F00" \
        "00000000" \
        "00000000" \
        "00000001" \
        "00000502" \
        "00000207" \
        "00000001" \
        "00000000" \
        "00000001" \
        "00800000" \
        "80000000" \
        "0000C594" \
        "00000000" \
        "00000001" \
        "140F0107" \
        "77625F73" \
        "6472616D" \
        "00000000" \
        "00000000" \
        "00000001" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000"

