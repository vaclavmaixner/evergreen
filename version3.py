#!/usr/bin/python

import os
import xml.sax
from xml.sax.saxutils import quoteattr,escape
import sys
import codecs
import argparse
import re

class Id():
	def __init__(self, egId, nkId):
		self.egId=egId
		self.nkId=nkId

class egExportParser(xml.sax.handler.ContentHandler):
	def startDocument(self):
		self.datafield=None
		self.subfield=None
		self.egSubfield=None        
		self.nkSubfield=None        
		self.counter=0

	def startElement(self,tag,attrs):
		if tag=="datafield":
			self.datafield=attrs.get('tag')
			self.subfield=None
		elif tag=="subfield":
			self.subfield=attrs.get('code')
		elif tag=="record": 
			self.datafield=None
			self.subfield=None
			self.counter+=1
			if not self.counter%1000:
				print ".",
				sys.stdout.flush()

		#if self.datafield=="100" and self.subfield=="7":
		#	print("yay")

	def characters(self,data):
		if self.datafield=="035" and self.subfield=="a":
			if "(CZ PrNK)" in data:
				data = data.replace("(CZ PrNK)", "")
			data = data.strip()

			if data!="":
				self.nkSubfield = data
				#idData=Id(egId, data)

				#if not nkIdsFromEg:
				#	nkIdsFromEg.append(idData)
				#elif idData!=nkIdsFromEg[-1]:
				#	nkIdsFromEg.append(idData)

			if data!="" and len(data)<=4:
				#print data + "chyba vole"
				pass


		if self.datafield=="901" and self.subfield=="c":
			if data!="":
				self.egSubfield=data
				#print self.egSubfield + "laaa"
				#if self.counter<=100:
				#	print self.egSubfield

		if self.egSubfield!="" and self.nkSubfield!="":
			idData=Id(self.egSubfield,self.nkSubfield)
			#print idData.egId + " " + idData.nkId + " kontrola"
			if len(nkIdsFromEg)>1:	
				if idData.egId!=nkIdsFromEg[-1].egId and idData.nkId!=nkIdsFromEg[-1].nkId:
					nkIdsFromEg.append(idData)
					print "yay"
			#print str(idData.egId) + " " + str(idData.nkId) + " oi"
			

			#self.egSubfield=None
			#self.nkSubfield=None

class nkExportParser(xml.sax.handler.ContentHandler):
	def startDocument(self):
		self.controlfield=None
		self.record=None
		self.counter=0

	def startElement(self,tag,attrs):
		if tag=="control":
			self.datafield=attrs.get('tag')
		elif tag=="record": 
			self.controlfield=None
			self.counter+=1
			if not self.counter%1000:
				print ".",
				sys.stdout.flush()

	def characters(self,data):
		if self.counter <= 5000:	
			code = "%s%s"%(self.datafield,self.subfield)
			if self.controlfield=="001":
				if data in nkIdsFromEg:
					#print(data, "success")
					pass




nkIdsFromEg = []



egExportParser = egExportParser()
parser = xml.sax.parse("EG_auth_UTF-8.xml", egExportParser)
print("Projetych zaznamu z EG: ", len(nkIdsFromEg))

nkExportParser = nkExportParser()
parser = xml.sax.parse("aut_test.xml", egExportParser)

#print out the data
for i in nkIdsFromEg:
	print str(i.egId ) + " " + i.nkId
	

#z EG aut vezme NK cisla a nasype je do pameti, pak se projede saxem
#NK aut a ty, ktery jsou v pameti, napise spolu s id z EG