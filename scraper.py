import requests
from collections import deque
import json
from bs4 import BeautifulSoup as bs
import sys


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
     child = childLink("https://en.wikipedia.org"+x,counter[refinedLinks.index(x)])
     parent.children.append(child)
   

   return parent



class Node:
    def __init__(self, link, degree):
        self.name = ''
        self.size = 1
        self.link = link
        self.degree = degree
        """references = [[link, count], [link, count], []]"""
        self.references = []

    def buildJSON(self):
        ary = []
        xJSON = {}
        for ref in self.references:
            ary.append({"url": ref[0], "points": ref[1],})
            xJSON = {
                "name": self.name,
                "size": self.size,
                "link": self.link,
                "degree": self.degree,res = requests.get(link)
    soup = bs(res.text, "html.parser")
                "refrence": ary,
            }
        return xJSON


def investigate(node, max_degree_, all_nodes_, q_):
    parent = grabLinks(node.link)
    all_nodes_[node.link].name = parent.name
    for child in parent.children:
        node.references.append([child.link, child.count])
        if child.link in all_nodes_:
            all_nodes_[child.link].size += 1
        else:
            new_node = Node(child.link, degree=node.degree + 1)
            if new_node.degree <= max_degree_:
                q_.append(new_node)
            all_nodes_[child.link] = new_node
    # print(parent.name, "==============", node.degree, "===========", node.link)
    # print("Level:",node.degree,"==",parent.name,"\t\t\t== URL:",node.link)


def sort_dictionary_by_size(lst):
    if len(lst) == 1:
        return lst
    else:
        pivot = lst[0][1].size
        left = []
        right = []
        for i in range(1, len(lst)-1):
            if lst[i][1].size <= pivot:
                left.append(lst[i])
            else:
                right.append(lst[i])
        return left + lst[0] + right


def main():
    all_nodes = dict()
    q = deque()
    max_degree = 1
    how_many_to_keep = 10

    parent = grabLinks("https://en.wikipedia.org/wiki/Breakwind_Ridge")
    new_node = Node(parent.link, degree=0)
    all_nodes[parent.link] = new_node
    q.append(new_node)
    while len(q):
        investigate(q.popleft(),
                    max_degree_=max_degree,
                    all_nodes_=all_nodes,
                    q_=q)
    sorted_list = []
    for key in all_nodes:
        sorted_list.append([key, all_nodes[key]])
    sorted_list = sort_dictionary_by_size(sorted_list)
    x = [item[1].buildJSON() for item in sorted_list[:how_many_to_keep]]
    
    print(json.dumps(x[:6]))

main()

