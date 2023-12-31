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


def get_first_link(bs):
    content_div = bs.find(id="mw-content-text").find(class_="mw-parser-output")

    #find the first link in the main body of the article
    for element in content_div.find_all("p", recursive=False):
        if element.find("a", recursive=False):
            return element.find("a", recursive=False).get('href')
    return None


def follow_to_philosophy(start_topic):
	visited_topics = set()  # keeping track of visited topics
	current_topic = start_topic
	p, d, path, _ = parseURL('http://en.wikipedia.org/wiki/' + current_topic)
	while current_topic.lower() != "philosophy":
		print(current_topic)
		site = buildURL(p, d, path, current_topic)
		result = requests.get(site)
		bs = BeautifulSoup(result.text, "html.parser")

		if current_topic in visited_topics:
			print("loop detected, stopping.")
			return
		visited_topics.add(current_topic)



