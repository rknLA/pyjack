#!/usr/bin/python
# -*- coding: utf-8 -*-
# Capture 3 seconds of stereo audio from alsa_pcm:capture_1/2; then play it back.
#
# Copyright 2003, Andrew W. Schmeder
# This source code is released under the terms of the GNU Public License.
# See LICENSE for the full text of these terms.

import numpy
import jack
import time

jack.attach("captest")

print jack.get_ports()

jack.register_port("in_1", jack.IsInput)
jack.register_port("in_2", jack.IsInput)
jack.register_port("out_1", jack.IsOutput)
jack.register_port("out_2", jack.IsOutput)

jack.activate()

print jack.get_ports()

jack.connect("system:capture_1", "captest:in_1")
jack.connect("system:capture_2", "captest:in_2")
jack.connect("captest:out_1", "system:playback_1")
jack.connect("captest:out_2", "system:playback_2")

print jack.get_connections("captest:in_1")

N = jack.get_buffer_size()
Sr = float(jack.get_sample_rate())
print "Buffer Size:", N, "Sample Rate:", Sr
sec = 3.0

capture = numpy.zeros((2,int(Sr*sec)), 'f')
input = numpy.zeros((2,N), 'f')
output = numpy.zeros((2,N), 'f')

#time.sleep(1)

print "Capturing audio..."

i = 0
while i < capture.shape[1] - N:
    try:
        jack.process(output, capture[:,i:i+N])
        i += N
    except jack.InputSyncError:
        print "Input Sync"
        pass
    except jack.OutputSyncError:
        print "Output Sync"
        pass
    print ".",

print "\nPlaying back..."

i = 0
iS = 0
oS = 0
while i < capture.shape[1] - N:
    try:
        jack.process(capture[:,i:i+N], input)
        i += N
    except jack.InputSyncError:
        iS += 1
        pass
    except jack.OutputSyncError:
        iO += 1
        pass
print "Finished with", iS, "input-off-sync &", oS, "output-off-sync"

jack.deactivate()
jack.detach()

import numpy, scipy.io.wavfile
toSave = numpy.array((2**15-1)*capture.transpose(),dtype="int16")
scipy.io.wavfile.write("output.wav", int(Sr), toSave)
