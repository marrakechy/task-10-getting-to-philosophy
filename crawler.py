import requests
from bs4 import BeautifulSoup
import time


def getTopic(site):
	result = requests.get(site)
	bs = BeautifulSoup(result.text, "html.parser")
	try:
		title = bs.find("title")
		topic = title.getText()
	except:
		topic = "No Title"
	return topic


def getLinks(bs):
	#theLinks = bs.findAll("a")
	theLinks = bs.find("div", {"id": "bodyContent"}).findAll("a")
	links = []
	for link in theLinks:
		try:
			if link["href"][:6] == "/wiki/" and ":" not in link["href"]:
				links.append(link["href"][6:])
		except KeyError:
			pass  #some a tags don't have the href  --we don't care about those.
	return links

def parseURL(url):
	parts = url.split("/")
	protocol = parts[0]
	domain = parts[2]
	path = "/".join(parts[3:-1])
	resource = parts[-1]
	return protocol, domain, path, resource

def buildURL(p,d,pa, r):
    return p+"//"+ d+"/"+pa+ "/"+r

def getSiteInfo(site):
	result = requests.get(site)
	bs = BeautifulSoup(result.text, "html.parser")
	try:
		title = bs.find("title")
		topic = title.getText()
	except:
		topic = "No Title"
	links = getLinks(bs)
	return (topic, links)

def visit(site):

	toVisit = []
	p,d,path,r = parseURL(site)
	topic, links = getSiteInfo(site)
	print(topic)
	toVisit += links
	print(len(links))
	for link in toVisit:
		print(link,end= " ")
		newURL = buildURL(p,d,path, link)
		print(newURL)
		#topic = getTopic(newURL)
		#print(topic)
		#time.sleep(1)
	return topic

visit("http://en.wikipedia.org/wiki/Coe_College")
