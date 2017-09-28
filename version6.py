#!/usr/bin/python

import os
import xml.sax
from xml.sax.saxutils import quoteattr,escape
import sys
import codecs
import argparse
import re

class egExportParser(xml.sax.handler.ContentHandler):
	def startDocument(self):
		self.datafield=None
		self.subfield=None
		self.controlfield=None
		self.egSubfield=None        
		self.nkSubfield=None        
		self.counter=0
		self.wrongData=False

		self.setOfDatafields={'100', '110', '111', '130', '240', '600', 
		'610', '611', '630', '648', '650', '651', '654', '655', '700',
		'710', '711', '730'}

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
				print self.counter, " "
				print ".",
				sys.stdout.flush()

	def characters(self,data):
		data = data.strip()
	
		if (self.datafield in self.setOfDatafields) and (self.subfield=="7"):
			if data!="":
				self.nkSubfield = data

		if self.nkSubfield:
			nkIdsFromEg.add(self.nkSubfield)

			self.nkSubfield=None

class nkExportParser(xml.sax.handler.ContentHandler):
	def startDocument(self):
		self.controlfield=None
		self.datafield=None
		self.subfield=None
		self.record=None
		self.recordData=None
		self.isRecord=False
		self.counter=0
		self.txtXml=""
		self.idIn=None
		self.writeToOutput=False
		self.writeToCut=False

	def startElement(self,tag,attrs):
		if tag=="datafield":
			self.datafield=attrs.get('tag')
			self.subfield=None
			if self.datafield!=None:
				self.txtXml+='<datafield tag=\"'+self.datafield+'\">'
			elif self.datafield==None:
				self.txtXml+='<datafield>'
		elif tag=="subfield":
			self.subfield=attrs.get('code')
			self.egSubfield=None
			if self.subfield!=None:
				self.txtXml+='<subfield code=\"'+self.subfield+'\">'
			elif self.subfield==None:
				self.txtXml+='<subfield>'
		elif tag=="controlfield":
			self.controlfield=attrs.get('tag')
			if self.controlfield!=None:
				self.txtXml+='<controlfield tag=\"'+self.controlfield+'\">'
			elif self.controlfield==None:
				self.txtXml+='<controlfield>'
		elif tag=="record": 
			self.datafield=None
			self.subfield=None
			self.counter+=1
			print self.counter, " "
			if not self.counter%1000:
				print ".",
				sys.stdout.flush()
			self.txtXml+='<record>'
		elif tag=="leader":
			self.txtXml+='<leader>'

	def endElement(self,tag):
		if tag=="datafield":
			self.txtXml+='</datafield>'
		elif tag=="subfield":
			self.txtXml+='</subfield>'
		elif tag=="controlfield":
			self.txtXml+='</controlfield>'
		elif tag=="leader":
			self.txtXml+='</leader>'
		elif tag=="record": 
			self.txtXml+='</record> \n'
			#self.txtXml+='\n'

			if self.writeToOutput:
				self.txtXml=self.txtXml
				outXmlFile.write(self.txtXml)
			elif self.writeToCut:
				cutXmlFile.write(self.txtXml)

					
			self.writeToOutput=False
			self.txtXml=""
			
	def characters(self,data):
		self.txtXml += data.rstrip()

		if self.controlfield=="001":

			#self.idIn = nkIdsFromEg.get(data)
			#if nkIdsFromEg:	
			if data in nkIdsFromEg:
				self.writeToOutput=True
				self.writeToCut=True




nkIdsFromEg = set()

parser = argparse.ArgumentParser(description='Nazdarek')

parser.add_argument("egFile",nargs='?',help="export XML file",default="EG_biblio_UTF-8.xml") 
parser.add_argument("nkFile",nargs='?',help="authority XML file",default="cut.xml")
parser.add_argument("-o","--output",help="output file",default="bib_output.xml")

args = parser.parse_args()

egFile=args.egFile
nkFile=args.nkFile
pathOut = args.output

outXmlFile = codecs.open(pathOut,"w","utf-8")
cutXmlFile = codecs.open("cut2.xml","w","utf-8")

egExportParser = egExportParser()
parser = xml.sax.parse(egFile, egExportParser)
print("Projetych zaznamu z EG: ", len(nkIdsFromEg))

nkExportParser = nkExportParser()
parser = xml.sax.parse(nkFile, nkExportParser)

outXmlFile.close()
print "Konec :]"
os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.2, 1000))
os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.2, 1500))
os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.2, 2500))
os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.4, 1000)) 