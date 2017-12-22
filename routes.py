import re
from bs4 import BeautifulSoup
from application import app
from flask import render_template
import os

def parse_htmlbook(page):
	links = get_chap_links(page)
	sections = {}
	for index in range(len(links)):
		section = {}
		start = links[index]
		if index < len(links)-1:
			end = links[index+1]
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
	return links, sections

def get_chap_links(page):
	soup = BeautifulSoup(page, 'html.parser')
	links = [str(link.get('href'))[1:] for link in soup.find_all('a') if link.get('href')]
	return links

@app.route('/', methods=['GET'])
def index():
	image_url = open('static/images/title_img.jpg', 'r')
	page = open('static/data/senseandsensibility.html', 'r').read()
	p = parse_htmlbook(page)
	print(type(p[1]))
	titles = []
	for chap in p[1]:
		titles.append(p[1][chap]['title'])
	# print(p[1])             
	return render_template('home.html', chapters=p[1], image_url=image_url, title="Sense and Sensibility")

@app.route('/<section>/', methods=['GET'])
def viewSection(section):
	page = open('static/data/senseandsensibility.html', 'r').read()
	p = parse_htmlbook(page)
	return render_template('section.html', chapters=p[1], section=p[1][section])
