from bs4 import BeautifulSoup as bs
import requests


class childLink:
  def __init__(self, link, count):
    self.link = link
    self.count = count

  
class parentLink:
   def __init__(self,link,name):
      self.link = link
      self.name = name
      self.children = []

phrases = [
   "File",
   "Wikipedia:",
   "Main",
   "Portal:",
   "Special",
   "Category",
   "Help",
]
def grabLinks(link):
   res = requests.get(link)
   soup = bs(res.text, "html.parser")
   # create a parent node (for returning)
   parent = parentLink(link,soup.title.string.replace(" - Wikipedia", ""))
   
   # store the refined list
   refinedLinks = []
   counter = []
   for link in soup.find_all("a"):
      url = link.get("href", "")
      if url.startswith("/wiki/") and not any(phrase in url for phrase in phrases):
         if(url not in refinedLinks):
            refinedLinks.append(url)
            counter.append(1)
         else:
            counter[refinedLinks.index(url)] += 1


   for x in refinedLinks:
     child = childLink(x,counter[refinedLinks.index(x)])
     parent.children.append(child)
   
   
   
   return parent

