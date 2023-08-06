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

from fretwork.audio import Audio
#from fretwork.audio import Channel
#from fretwork.audio import MicrophonePassthroughStream
#from fretwork.audio import Music
#from fretwork.audio import StreamingSound
#from fretwork.audio import Sound


class AudioTest(unittest.TestCase):

    def test_open(self):
        audio = Audio()
        nb_channels = 10
        # init the pygame mixer and set channels
        audio_open = audio.open()
        self.assertTrue(audio_open)  # check return
        self.assertIsNotNone(pygame.mixer.get_init())  # check the mixer
        self.assertEqual(pygame.mixer.get_num_channels(), nb_channels)  # check channels
        # quit the mixer
        audio.close()

    def test_close(self):
        audio = Audio()
        # init the pygame mixer
        audio.open()
        # close the pygame mixer
        audio.close()
        self.assertIsNone(pygame.mixer.get_init())  # check the mixer

    def test_findChannel(self):
        pass

    def test_getChannelCount(self):
        pass

    def test_pause(self):
        pass

    def test_unpause(self):
        pass


class MusicTest(unittest.TestCase):

    def test_setEndEvent(self):
        pass

    def test_play(self):
        pass

    def test_setVolume(self):
        pass

    def test_fadeout(self):
        pass

    def test_isPlaying(self):
        pass


class ChannelTest(unittest.TestCase):
    pass


class SoundTest(unittest.TestCase):
    pass


class MicrophonePassthroughStreamTest(unittest.TestCase):

    def test_play(self):
        pass

    def test_stop(self):
        pass

    def test_setVolume(self):
        pass


class StreamingSoundTest(unittest.TestCase):

    def test_play(self):
        pass

    def test_stop(self):
        pass

    def test_setVolume(self):
        pass

    def test_fadeout(self):
        pass

    def test_setPitchBendSemitones(self):
        pass

    def test_setSpeed(self):
        pass
