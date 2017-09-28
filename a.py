#!/usr/bin/python

import os
import xml.sax
from xml.sax.saxutils import quoteattr,escape
import sys
import codecs
import argparse
import re

import xml.sax.saxutils

class egExportParser(xml.sax.handler.ContentHandler):
	def startDocument(self):
		self.datafield=None
		self.subfield=None
		self.controlfield=None
		self.egSubfield=None        
		self.nkSubfield=None        
		self.counter=0
		self.wrongData=False

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

	def characters(self,data):
		data = data.strip()
		if self.datafield=="035" and self.subfield=="a":
			if "(CZ PrNK)" in data:
				data = data.replace("(CZ PrNK)", "")

			if data!="":
				self.nkSubfield = data

			if data!="" and len(data)<=4:
				#print data, " Nasel jsem tu chybu >:[ ", self.counter
				#self.wrongData=True
				pass

		if self.datafield=="901" and self.subfield=="c":
			if data!="":
				self.egSubfield=data
			if self.wrongData:
				print data, "chybnej zaznam"
				self.wrongData=False

		if self.egSubfield and self.nkSubfield:
			nkIdsFromEg[self.nkSubfield]=self.egSubfield

			self.egSubfield=None
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
			if not self.counter%1000:
				print ".",
				sys.stdout.flush()
			self.txtXml+='<record>\n'
		elif tag=="leader":
			self.txtXml+='<leader>'

	def endElement(self,tag):
		if tag=="datafield":
			self.txtXml+='</datafield>\n'
		elif tag=="subfield":
			self.txtXml+='</subfield>\n'
		elif tag=="controlfield":
			self.txtXml+='</controlfield>\n'
		elif tag=="leader":
			self.txtXml+='</leader>\n'
		elif tag=="record": 
			self.txtXml+='</record>\n'
			#self.txtXml+='\n'


			if self.writeToOutput:
				self.txtXml=self.txtXml.replace('\n', '')
				outXmlFile.write(self.txtXml)
				outXmlFile.write("\n")
			elif self.writeToCut and self.counter<=5000:
				cutXmlFile.write(self.txtXml)				
			self.writeToOutput=False
			self.txtXml=""
			
	def characters(self,data):
		dataEscaped = xml.sax.saxutils.escape(data)
		self.txtXml += dataEscaped.rstrip()
		if self.controlfield=="001":
			self.idIn = nkIdsFromEg.get(data)
			if self.idIn!=None:
				outXmlFile.write(nkIdsFromEg[data] + "	")
				self.writeToOutput=True
				self.writeToCut=True



nkIdsFromEg = {}

parser = argparse.ArgumentParser(description='Nazdarek')

parser.add_argument("egFile",nargs='?',help="export XML file",default="EG_auth_UTF-8.xml") 
parser.add_argument("nkFile",nargs='?',help="authority XML file",default="../autority_zaklad/aut_exp.xml")
parser.add_argument("-o","--output",help="output file",default="biblio_output.txt")

args = parser.parse_args()

egFile=args.egFile
nkFile=args.nkFile
pathOut = args.output

outXmlFile = codecs.open(pathOut,"w","utf-8")
cutXmlFile = codecs.open("cut.xml","w","utf-8")
cutXmlFile.write("""<?xml version = "1.0" encoding = "UTF-8"?>\n""")
cutXmlFile.write("""<collection xmlns="http://www.loc.gov/MARC21/slim" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.loc.gov/MARC21/slim http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">\n""")




egExportParser = egExportParser()
parser = xml.sax.parse(egFile, egExportParser)
print("Projetych zaznamu z EG: ", len(nkIdsFromEg))

nkExportParser = nkExportParser()
parser = xml.sax.parse(nkFile, nkExportParser)

outXmlFile.close()
cutXmlFile.write("</collection>")
cutXmlFile.close()

print "Konec :]"
os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.2, 1000))
os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.2, 1500))
os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.2, 2500))
os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 0.4, 1000))