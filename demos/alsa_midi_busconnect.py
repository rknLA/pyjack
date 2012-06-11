#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os

def _getClients(typeOfClient):
	lines=[line.strip() for line in os.popen("LANG=C aconnect -%s" % typeOfClient).readlines()]
	listOfClients=[]
	temporalList=[]
	for line in lines:
		if line.find("client ")==0:
			listOfClients.append(dict())
			listOfClients[-1]["clientName"]=re.search("'(.*)'",line).group(1)
			listOfClients[-1]["clientNumber"]=int(re.search("client (.*):",line).group(1))
			if len(temporalList)>0:
				listOfClients[-2]["ports"]=temporalList
			temporalList=[]
		else:
			line=re.search("'(.*)'",line).group(1)
			temporalList.append(line)
	listOfClients[-1]["ports"]=temporalList
	return listOfClients

def _getClientPorts(name,typeOfClient):
	listOfClients=_getClients(typeOfClient)
	try:
		index=[client['clientName'] for client in listOfClients].index(name)
	except:
		print "WARNING: trying to get ports of client %s, which doesn't exist. Returning an empty list." % name
		return []
	if index == -1:
		return None
	client=listOfClients[index]
	return [ "%s:%i" % (client["clientNumber"],client["ports"].index(port)) for port in client["ports"] ]

def getInputClients():
	return _getClients("o")
	
def getOutputClients():
	return _getClients("i")

def getClientInputPorts(name):
	return _getClientPorts(name,"o")

def getClientOutputPorts(name):
	return _getClientPorts(name,"i")

def connect(source,target):
	os.system("aconnect %s %s" % (source,target))

def bus_connect(source, target):
	"""
	Connects two lists of ports. The arguments can be a list or a string. If the latter, all the available ports of the client will be used.
	"""
	sources = source if type(source) == type([]) else getClientOutputPorts(source)
	targets = target if type(target) == type([]) else getClientInputPorts(target)
	num_connections = min(len(sources), len(targets))
	print 'Doing %i connections. Client has %i out ports and target has %i in ports' % (num_connections, len(sources), len(targets))
	for i in xrange(num_connections) :
		print 'connect', sources[i], targets[i]
		connect(sources[i], targets[i])
	return num_connections != 0

def main():
	print "input clients: "
	print getInputClients()
	print "output ones: "
	print getOutputClients()
	print "Midi Through:"
	print getClientInputPorts("Midi Through")
	print "Midi Through outputs:"
	print getClientOutputPorts("Midi Through")
	bus_connect("Midi Through","Midi Through")

if __name__ == '__main__':
	main()
