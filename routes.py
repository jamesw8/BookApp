import re
from bs4 import BeautifulSoup
from application import app
from flask import render_template
import os

def parse_htmlbook(page):
	links = get_chap_links(page)
	sections = {}
	for ind in range(len(links)):
		section = {}
		start = links[ind]
		if ind < len(links)-1:
			end = links[ind+1]
			patt = ('<A NAME="' + start + '"></A>(?P<sectionbody>.*)<A NAME="' + end + '">' )
			match = re.search(patt,page,re.MULTILINE|re.DOTALL)
			if match == None:
				raise Exception('patt: '+patt+'\n\n')
		else:
			patt = ('<A NAME="' + start + '"></A>(?P<sectionbody>.*)<pre>')
			match = re.search(patt,page,re.MULTILINE|re.DOTALL)
		if match:
			soup = BeautifulSoup(match.group("sectionbody"), 'html.parser')
			plist = [p.contents[0] for p in soup.find_all('p')]
			section['title']= (soup.find('h3').contents)[0]
			section['plist']= plist
			sections[start] = section
		print(links, sections) 
		return links, sections

def get_chap_links(page):
	soup = BeautifulSoup(page, 'html.parser')
	links = [str(link.get('href'))[1:] for link in soup.find_all('a') if link.get('href')]
	return links

@app.route('/', methods=['GET'])
def index():
	image_url = open('static/images/title_img.jpg', 'r')
	print(os.listdir())
	page = open('static/data/senseandsensibility.html', 'r').read()
	p = parse_htmlbook(page) 
	print(p[1].keys())             
	return render_template('home.html', chapters=p[0], image_url=image_url, title="Sense and Sensibility")

@app.route('/<section>/', methods=['GET'])
def viewSection(section):
	page = open('static/data/senseandsensibility.html', 'r').read()
	p = parse_htmlbook(page) 
	return render_template('section.html', chapters=p[0], section=section)
