#!BPY
# -*- coding: utf-8 -*-
"""
Name: 'Jack Transport'
Blender: 249
Group: 'Misc'
Tooltip: 'Makes jack and blender synced'
"""
__script__ = "Jack Transport"
__author__ = "falkTX"
__version__ = "0.1"
__url__ = ["Communicate problems and errors, BlenderArtists.org, Python forum"]
__email__= ["falktx@gmail.com", "blender-pyjack script"]
__bpydoc__ = """\
blender-jacktransport.py v0.1

Version History:
 0.1: Initial release
"""

# Depends from PyJack-0.2
# Uses code from bpyjack.py by IL'dar AKHmetgaleev (aka AkhIL)

# Tried to get this as fast (and simple) as possible

import bpy
import jack, time, sys
import Blender
from Blender import *

play_button = Draw.Create(False)
BEV_PLAY = 1
BEV_EXIT = 2
BEV_PREV = 3
BEV_NEXT = 4
BEV_START = 5
ret_blender_curr = 0
ret_blender_next = 0
ret_jack_current = 0
prev_blen = 0
prev_jack = 0

try:
    jack.attach("/var/run/jack-blender")
except jack.UsageError:
    pass # continue using exist jack if script crashed but jack still online 

def getFrames():
    global ret_blender_curr
    global ret_blender_next
    global ret_jack_current

    currblenframe = Get("curframe")
    currjackframe = jack.get_current_transport_frame()

    rate = jack.get_sample_rate()

    fps = Scene.GetCurrent().getRenderingContext().fps
    fpsBase = Scene.GetCurrent().getRenderingContext().fpsBase
    factor = int(rate/(fps/fpsBase))

    ret_blender_curr = currblenframe*factor
    ret_blender_next = currjackframe/factor
    ret_jack_current = currjackframe


def refresh():
    global ret_blender_curr
    global ret_blender_next
    global ret_jack_current
    global prev_blen
    global prev_jack

    getFrames()

    #print "blender old", prev_blen
    #print "blender frame is", ret_blender_curr
    #print "jack old", prev_jack
    #print "jack frame is", ret_jack_current

    if (prev_jack != ret_jack_current): #Jack changed, externally
        Set("curframe", ret_blender_next)
        #Window.Redraw(Window.Types.ACTION)
        Window.Redraw(Window.Types.BUTS)
        #Window.Redraw(Window.Types.IMAGE)
        #Window.Redraw(Window.Types.IMASEL)
        #Window.Redraw(Window.Types.INFO)
        Window.Redraw(Window.Types.SEQ)
        #Window.Redraw(Window.Types.TEXT)
        Window.Redraw(Window.Types.VIEW3D)
    elif (prev_blen != ret_blender_curr): #Blender changed, internally
        jack.transport_locate(ret_blender_curr)
        while jack.get_current_transport_frame() != ret_blender_curr:
            time.sleep(0.01) # waiting till pyjack applyed transport

    id = Window.GetAreaID()
    Window.QAdd(id, Draw.TIMER3, 0, 1)

    prev_blen = ret_blender_curr
    prev_jack = ret_jack_current

def event (evt, dummy):
    if evt == Draw.TIMER3:
        refresh()
        time.sleep(0.001)

def button_event (evt):
    global play_button

    currentJackFrame = jack.get_current_transport_frame()

    if evt == BEV_PLAY: #play/pause
        if play_button.val == 1:
            jack.transport_start()
        else:
            jack.transport_stop()

    elif evt == BEV_START: #back to 0
        jack.transport_locate(0)

    elif evt == BEV_PREV: #go back
        nextJackFrame = currentJackFrame - 200000
        if (nextJackFrame < 0): nextJackFrame = 0
        jack.transport_locate(nextJackFrame)

    elif evt == BEV_NEXT: #go forward
        nextJackFrame = currentJackFrame + 200000
        jack.transport_locate(nextJackFrame)

    elif evt == BEV_EXIT: #quit script
        jack.detach()
        Draw.Exit()

def gui ():
    global play_button
    BGL.glClearColor(*map(lambda x: x/255.0, Window.Theme.Get()[0].get('buts').back))
    BGL.glClear(BGL.GL_COLOR_BUFFER_BIT)
    Draw.BeginAlign()

    if jack.get_transport_state() == jack.TransportStopped:
        play_button.val = 0
        button_text = "play"
    else:
        play_button.val = 1
        button_text = "pause"

    Draw.PushButton("s", BEV_START, 1, 1, 20, 20, "Go to 0")
    Draw.PushButton("<", BEV_PREV, 20, 1, 20, 20, "Go back")
    Draw.PushButton(">", BEV_NEXT, 40, 1, 20, 20, "Go forward")
    play_button = Draw.Toggle(button_text, BEV_PLAY, 60, 1, 75, 20, play_button.val, "Play / Pause")
    Draw.PushButton("x", BEV_EXIT, 135, 1, 25, 20, "Exit from script")
    Draw.EndAlign()


Draw.Register(gui, event, button_event)

refresh()
