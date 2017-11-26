#! /usr/bin/env python

import re
import keyPhrasesMSCS as kp
import urllib, urllib2
#import xml.etree.ElementTree as ET
import feedparser
import wikipedia




# get intro from wikipedia for a topic
def getWikiIntro(inString):
	out = ["FAILFAIL","FAILFAIL"]
	try:
		out[0] = wikipedia.summary(inString, sentences=4)
		out[1] = wikipedia.page(inString).url
	except Exception, e:
		pass
	return out


def infoFromArXiv(arXivCode):
	url = "https://arxiv.org/abs/"+str(arXivCode)
	pagesource = urllib2.urlopen(url)
	title = ""
	abstract = ""
	summary = ""
	onTitle = False
	onSummary = False
	for line in pagesource:
		if line.strip().startswith("<title>"):
			onTitle = True
		if onTitle:
			title = title+line
		if line.strip().endswith("</title>"):
			onTitle = False
		if '<span class="descriptor">Abstract:</span>' in line:
			onSummary = True
		if "</blockquote>" in line:
			onSummary = False
			break
		if onSummary:
			summary = summary+line.strip('"<span class="descriptor">Abstract:</span> "')
	title = title.strip().replace("<title>","").replace("</title>","").replace("\n"," ").replace("   "," ").replace("  "," ")
	summary = summary.strip().replace("\n"," ")
	return [title,summary]
		

def getTopPhrases(longString):
	allkeywords = kp.getKeyWords(longString)
	top = []
	for keyword in allkeywords:
		keystr = str(keyword)
		if len(keystr.split()) > 1:
			top.append(keystr)
	return top




# get PDF url from arxiv-looking string
def arXivPDF(someString):

	# find arxiv code
	arXivCode = re.findall(r'(\d{4}.\d{4})', someString)
	if len(arXivCode) != 1:
		return "FAIL: Couldn't obtain arXiv code."
	code = arXivCode[0]
	pdfurl = "https://arXiv.org/pdf/"+code+".pdf"
	return pdfurl

# get PDF url from arxiv-looking string
def findArXivCode(someString):

	# find arxiv code
	arXivCode = re.findall(r'(\d{4}.\d{4})', someString)
	if len(arXivCode) != 1:
		return "FAIL: Couldn't obtain arXiv code."
	code = arXivCode[0]
	return code

# rank citations by importance
def rankCitations(unrankedCitations):
	rankedCitations = []
	# TODO
	return rankedCitations

# make an HTML card to display citation
def getHTMLcitationCard(citationString):
	citationCard = ""
	# TODO
	return citationCard

# get definitions of key phrases
def definePhrase(somePhrase):
	definition = ""
	# TODO
	return  definition

# make an HTML card to display key phrase and definitio
def getHTMLphraseCard(somePhrase,phraseDefinition):
	phraseCard = ""
	# TODO
	return phraseCard


def buildHTMLDivs(keyps):
	divs = []
	for keyp in keyps:
		wiki = getWikiIntro(keyp)
		description = wiki[0]
		url = wiki[1]
		content = "<p><div><p><b>"
		if description != "FAILFAIL":
			title = keyp[0].upper()+keyp[1:]
			title = '<a href="'+url+'">'+title+'</a>'
			content = content+title+":</b></p><p>"
			content = content+"</b></b></b></b>"+description+"...</p>"
		content = content + "</div></p>"
		divs.append(content)
	return divs


# the mother function
def getFullPageHTML(userInput):

	# get data from arXiv
	code = findArXivCode(userInput)
	url = "https://arxiv.org/abs/"+str(code)
	[paperTitle, paperAbstract] = infoFromArXiv(code)
	print "GOT TITLE: "+paperTitle
	print "GOT ABSTRACT: "+paperAbstract
	keyps = getTopPhrases(paperAbstract)
	paperTitle = '<a href="'+url+'">'+paperTitle+'</a>'
	
	# build content
	content = "" # construct decent looking body (without going to the gym)
	divs = buildHTMLDivs(keyps)
	for div in divs:
		content = content+div
	
	# constant style things
	topOfPage = """<!DOCTYPE html><html lang="en"><head><title>"""+paperTitle+"""</title><link href="http://getbootstrap.com/dist/css/bootstrap.min.css" rel="stylesheet"><link href="http://getbootstrap.com/examples/jumbotron-narrow/jumbotron-narrow.css" rel="stylesheet"><link href="/static/newindex.css" rel="stylesheet"><script src="/static/js/jquery-1.11.2.js"></script><script src="/static/js/signUp.js"></script></head><body><div class="container"><div class="header"><h3 class="text-muted">clarefy</h3></div><div class="jumbotron"><div align="center"><img src="/static/images/clarefy_logo.png" align="middle"></div><h1>""" # everything up to a header
	header = paperTitle+"</h1><p></p><p><h3>Key concepts from this paper:</h3></p>" # set page title from paper title
	
	bottomOfPage = """</p></div><p>Powered by:</p><p></p><a href="https://azure.microsoft.com/en-gb/services/cognitive-services/"><img src="/static/images/mscs.png" style="width:278px;height:83px;"><a href="https://scholar.google.co.uk/"><img src="/static/images/google_scholar.png" style="width:217px;height:83px;"><a href="https://aws.amazon.com"><img src="/static/images/aws_logo.png" style="width:189px;height:83px;"> <a href="http://flask.pocoo.org/"><img src="/static/images/flask.png" style="width:212px;height:83px;"> </a><footer class="footer"><p></p><p>&copy; clarefy 2017</p></footer>"""
	return topOfPage+header+content+bottomOfPage






"""

[testTitle, testSummary] = infoFromArXiv(1412.1633)
keyps = getTopPhrases(testSummary)
for keyp in keyps:
	print keyp+":\n"+getWikiIntro(keyp)+"\n-------------------"

"""



