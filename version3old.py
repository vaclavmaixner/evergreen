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
			self.egSubfield=None
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
		#idData = Id(data, )
		#egId = None

		

		if self.datafield=="035" and self.subfield=="a":
			if "(CZ PrNK)" in data:
				data = data.replace("(CZ PrNK)", "")
			data = data.strip()

			if data!="":
				#idData=Id(egId, data)

				#if not nkIdsFromEg:
				#	nkIdsFromEg.append(idData)
				#elif idData!=nkIdsFromEg[-1]:
				#	nkIdsFromEg.append(idData)

				self.nkSubfield = data

			if data!="" and len(data)<=4:
				print(data, "chyba vole")

		if self.datafield=="901" and self.subfield=="c":
			if data!="":
				self.egSubfield=data

			
		if self.egSubfield and self.nkSubfield:
			idData=Id(self.egSubfield,self.nkSubfield)
			nkIdsFromEg.append(idData)

			self.egSubfield=None
			self.nkSubfield=None

class nkExportParser(xml.sax.handler.ContentHandler):
	def startDocument(self):
		self.controlfield=None
		self.record=None
		self.recordData=None
		self.isRecord=False
		self.counter=0
		print "yup"

	def startElement(self,tag,attrs):
		if tag=="controlfield":
			self.controlfield=attrs.get('tag')
		elif tag=="record": 
			self.controlfield=None
			self.counter+=1
			if not self.counter%1000:
				print ".",
				sys.stdout.flush()

	def characters(self,data):
		if self.controlfield=="001":
			for i in nkIdsFromEg:
				pass
				if i.nkId==data:
					outXmlFile.write(i.egId + "	" + "success")


nkIdsFromEg = []

pathOut = "biblio_output.xml"

outXmlFile = codecs.open(pathOut,"w","utf-8")
outXmlFile.write('<collection xmlns="http://www.loc.gov/MARC21/slim" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.loc.gov/MARC21/slim http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">')


egExportParser = egExportParser()
parser = xml.sax.parse("EG_auth_UTF-8.xml", egExportParser)
print("Projetych zaznamu z EG: ", len(nkIdsFromEg))

nkExportParser = nkExportParser()
parser = xml.sax.parse("../autority_zaklad/aut_exp.xml", nkExportParser)

#print out the data
#for i in nkIdsFromEg:
#	print i.egId, i.nkId


outXmlFile.write('</collection> uspech2')
outXmlFile.close()
print "konec vole"

#z EG aut vezme NK cisla a nasype je do pameti, pak se projede saxem
#NK aut a ty, ktery jsou v pameti, napise spolu s id z EG