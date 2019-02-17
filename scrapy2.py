import requests
import json
from bs4 import BeautifulSoup as bs
import sys


phrases = [
   "File",
   "Wikipedia:",
   "Main",
   "Portal:",
   "Special",
   "Category",
   "Help",
   "Empty",
   "Template"
]

# Global connection variable
connection = []

def grabLinks(link,sublink):
    res = requests.get(link)
    soup = bs(res.text, "html.parser")
    refinedLinks = []
    for link in soup.find_all("a"):
        url = link.get("href", "")
        if url.startswith("/wiki/") and not any(phrase in url for phrase in phrases):
            refinedLinks.append(url)
            connection.append({"start":""+sublink+"","end":url})
    return refinedLinks




def start(url):
    nodes = []
    nodes = (grabLinks(url,url.replace("https://en.wikipedia.org","")))#<-- this will set the parent connection to nothing . 
    # print(nodes)#first children
    nodes2 = []
    for x in nodes:
        nodes2 = nodes2 + (grabLinks("https://en.wikipedia.org"+x,x))
    # print(nodes2)#second children
    return clean(url,nodes,nodes2)
    
def clean(url,b,c):
    links = (b+c)
    counter = []
    nodes = []
    for x in links:
        if x not in nodes:
            nodes.append(x)
            counter.append(1)
        else:
            counter[nodes.index(x)] += 1
    nodeOBJ = []
    res = requests.get(url)
    soup = bs(res.text, "html.parser")
    # GET SIDE BAR STUFF
        
    for x in nodes:
        nodeOBJ.append({
            "title":x.replace("/wiki/",""),
            "size":counter[nodes.index(x)]
        })
    # the api to return
    api = {
        "title":soup.title.string.replace(" - Wikipedia", ""),
        "url":url,
        "nodes": nodeOBJ,
        "connections":connection
    }
    return api
        
data = start(sys.argv[1])
with open('data.json', 'w') as f:
  json.dump(data, f, ensure_ascii=False,indent=4)
print("SUCCESS")
