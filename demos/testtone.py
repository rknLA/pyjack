#!/usr/bin/python
# -*- coding: utf-8 -*-
# Plays a 440.0 Hz test tone for 3 seconds to alsa_pcm:playback_1.
#
# Copyright 2003, Andrew W. Schmeder
# This source code is released under the terms of the GNU Public License.
# See LICENSE for the full text of these terms.

import numpy
import jack

jack.attach("testtone")
jack.register_port("in_1", jack.IsInput)
jack.register_port("out_1", jack.IsOutput)
jack.activate()
jack.connect("testtone:out_1", "alsa_pcm:playback_1")

N = jack.get_buffer_size()
Sr = float(jack.get_sample_rate())
print "Buffer Size:", N, "Sample Rate:", Sr
sec = 3.0

input = numpy.zeros((1,N), 'f')
output = numpy.reshape(
    numpy.sin(
        2*numpy.pi*440.0 * (numpy.arange(0, sec, 1.0/(Sr), 'f')[0:int(Sr*sec)])
    ), (1, Sr*sec)).astype('f')

i = 0
while i < output.shape[1] - N:
    try:
        jack.process(output[:,i:i+N], input)
        i += N
    except jack.InputSyncError:
        pass
    except jack.OutputSyncError:
        pass
        
jack.deactivate()

jack.detach()
