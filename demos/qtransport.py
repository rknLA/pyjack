#!/usr/bin/python
# -*- coding: utf-8 -*-

import jack, os, sys
from PyQt4.QtGui import QApplication, QDialog
from PyQt4.QtCore import QTimer, SIGNAL, SLOT
from PyQt4.uic import loadUi

jack.attach("qtransport")

class MainW(QDialog):
    def __init__(self, *args):
        QDialog.__init__(self, *args)
        loadUi(sys.path[0]+"/qtransport_gui.ui", self)
        
        self.timer = QTimer()
        self.timer.start(100)
        
        self.connect(self.b_back, SIGNAL("clicked()"), self.goBack)
        self.connect(self.b_play, SIGNAL("clicked()"), self.play)
        self.connect(self.b_stop, SIGNAL("clicked()"), self.stop)
        self.connect(self.b_forward, SIGNAL("clicked()"), self.goForward)
        self.connect(self.timer, SIGNAL("timeout()"), self.refreshUi)
        
    def goBack(self):
	pos = int(jack.get_current_transport_frame()) - 100000
	if pos < 0:
	  jack.transport_locate(0)
	else:
	  jack.transport_locate(pos)

    def goForward(self):
	jack.transport_locate(jack.get_current_transport_frame()+100000)

    def play(self):
	if (self.b_play.isChecked()):
	  jack.transport_start()
	else:
	  jack.transport_stop()

    def stop(self):
	jack.transport_stop()
	jack.transport_locate(0)
	self.b_play.setChecked(False)

    def refreshUi(self):
	state = jack.get_transport_state()
	frame = jack.get_current_transport_frame()
	rate  = jack.get_sample_rate()
	
	# Jack State
	if (state == 0):
	  self.l_state.setText("Stopped")
	  self.b_play.setChecked(False)
	elif (state == 1):
	  self.l_state.setText("Rolling")
	  self.b_play.setChecked(True)
	elif (state == 3): self.l_state.setText("Starting")
	else: self.l_state.setText("Unknown (%i)" % state)

	# Current Time
	time = frame / rate
	secs = time % 60
	mins = (time / 60) % 60
	hrs  = (time / 3600) % 60
	secH = minH = hrsH = ""
	if secs < 10: secH = "0"
	if mins < 10: minH = "0"
	if hrs  < 10: hrsH = "0"
	self.l_time.setText(hrsH+str(hrs)+":"+minH+str(mins)+":"+secH+str(secs))
	
	# Current Frame
	self.l_frame.setText(str(frame))

#--------------- main ------------------
if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = MainW()
    gui.show()
    app.exec_()
    jack.detach()
