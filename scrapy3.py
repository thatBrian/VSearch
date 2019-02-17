import requests
import json
from bs4 import BeautifulSoup as bs
import sys
from math import sqrt

phrases = [
    "File",
    "Wikipedia:",
    "Main",
    "Portal:",
    "Special",
    "Category",
    "Help",
    "Empty",
    "Template",
]

# Global connection variable
connection = []
url_to_keep = set()
url_in_dict = dict()
how_many_to_keep = 30

def grabLinks(link, sublink):
    res = requests.get(link)
    soup = bs(res.text, "html.parser")
    refinedLinks = []
    for link in soup.find_all("a"):
        url = link.get("href", "")
        if url.startswith("/wiki/") and not any(phrase in url for phrase in phrases):
            refinedLinks.append(url)
            connection.append({"start": "" + sublink + "", "end": url})
    return refinedLinks


def start(url):
    # nodes = []
    nodes = (grabLinks(url, url.replace("https://en.wikipedia.org","")))
    # ^ this will set the parent connection to nothing .
    # print(nodes)#first children
    nodes2 = []
    for x in nodes:
        nodes2 = nodes2 + (grabLinks("https://en.wikipedia.org" + x, x))
    # print(nodes2)#second children
    return clean(url, nodes, nodes2)


def sort_OBJ_by_size(lst):
    if len(lst) <= 1:
        return lst
    else:
        pivot_value = lst[0]['size']
        left = []
        right = []
        for i in range(1, len(lst)-1):
            if lst[i]["size"] <= pivot_value:
                left.append(lst[i])
            else:
                right.append(lst[i])
        return sort_OBJ_by_size(right) + [lst[0]] + sort_OBJ_by_size(left)


def filter_connections():
    global connection
    for i, item in enumerate(connection):
        if item["start"] not in url_to_keep:
            connection.pop(i)
            continue
        elif item["end"] not in url_to_keep:
            connection.pop(i)
            continue
        else:
            address_code = item["start"] + "~" + item["end"]
            if address_code in url_in_dict:
                url_in_dict[address_code] += 1
            else:
                url_in_dict[address_code] = 1
    connection = []
    for item in url_in_dict:
        # weight = url_in_dict[item]
        conn_start, conn_end = item.split("~")
        connection.append({
            "source": conn_start,
            "target": conn_end,
            # "weight": weight
        })



def clean(url, b, c):
    links = (b + c)
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

    for x in nodes:
        nodeOBJ.append({
            "title": x.replace("/wiki/", ""),
            "url": x,
            "id": x,
            "size": counter[nodes.index(x)]
        })

    nodeOBJ = sort_OBJ_by_size(nodeOBJ)[:how_many_to_keep]
    average = 0
    variance = 0
    for node in nodeOBJ:
        average += node["size"] / how_many_to_keep
        variance += (node["size"]**2) / (how_many_to_keep+1)
    variance = sqrt(variance)
    for node in nodeOBJ:
        z = int(3 * (node["size"] - average) / variance) + 4
        if z > 10:
            z = 10
        if z < 1:
            z = 1
        node["size"] = z
        url_to_keep.add(node["url"])
    filter_connections()
    # the api to return

    api = {
        "title": soup.title.string.replace(" - Wikipedia", ""),
        "url": url,
        "nodes": nodeOBJ,
        "links": connection
    }
    return api





# print(len(connection))
data = start(sys.argv[1])
with open('./static/data.json', 'w') as f:
  json.dump(data, f, ensure_ascii=False,indent=4)
print("SUCCESS")