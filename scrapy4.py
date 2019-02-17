import requests
import json
from bs4 import BeautifulSoup as bs
import sys
from math import sqrt
import multiprocessing as mp
import time

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
url_to_keep = set()
url_in_dict = dict()
how_many_to_keep = 50


def grabLinks(link, sublink=None):
    conn_out = False
    if sublink is None:
        conn_out = True
        sublink = link
        link = "https://en.wikipedia.org" + link
    res = requests.get(link)
    soup = bs(res.text, "html.parser")
    refinedLinks = []
    connection_temp_lst = []
    for link in soup.find_all("a"):
        url = link.get("href", "")
        if url.startswith("/wiki/") and not any(phrase in url for phrase in phrases):
            refinedLinks.append(url)
            if conn_out is False:
                global connection
                connection.append({"start": "" + sublink + "", "end": url})
            else:
                connection_temp_lst.append({"start": "" + sublink + "", "end": url})
    if conn_out is False:
        return refinedLinks
    else:
        return connection_temp_lst, refinedLinks


def start(url):
    nodes = (grabLinks(url, url.replace("https://en.wikipedia.org", "")))
    # ^ this will set the parent connection to nothing .
    nodes2 = []

    conn_temp_lst = []
    with mp.Pool(mp.cpu_count()) as p:
        items = p.map(grabLinks, nodes)
        link_temp_lst = []
        for item in items:
            conn_temp_lst += item[0]
            link_temp_lst += item[1]
        nodes2 += link_temp_lst
    # print(nodes2)#second children
    global connection
    connection += conn_temp_lst
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
    # print("Cleaning")
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
            "id":x,
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

# start_ = time.time()
# api = json.dumps(start('https://en.wikipedia.org/wiki/Fremont,_California'), indent=4, sort_keys=True)
# print(api)
# print(time.time()-start_)

# with open('data.json', 'w') as outfile:
    # json.dump(start('https://en.wikipedia.org/wiki/Breakwind_Ridge'),indent=4, sort_keys=True, outfile)

data = start(sys.argv[1])
with open('./static/data.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
print("SUCCESS")


# print(len(connection))


