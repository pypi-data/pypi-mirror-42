#!/usr/bin/python
# -*- coding: utf-8 -*-

# FoFiX
# Copyright (C) 2018 FoFiX team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import unittest

import pygame

from fretwork.mixstream import VorbisFileMixStream


class VorbisFileMixStreamTest(unittest.TestCase):

    def setUp(self):
        freq = 22050    # audio CD quality
        bitsize = -16   # unsigned 16 bit
        channels = 2    # 1 is mono, 2 is stereo
        buffer_ = 1024  # number of samples (experiment to get right sound)
        pygame.mixer.init(freq, bitsize, channels, buffer_)

    def test_play(self):
        filename = "tests/guitar.ogg"
        channel = pygame.mixer.Channel(0)
        #mx = VorbisFileMixStream(filename)
        #mx.play(channel)

    def test_is_playing(self):
        pass

    def test_stop(self):
        pass

    def test_seek(self):
        pass

    def test_get_position(self):
        pass

    def test_get_length(self):
        pass

    def test_set_pitch_semitones(self):
        pass

    def test_set_speed(self):
        pass
