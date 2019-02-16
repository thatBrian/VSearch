import scraper

parent = scraper.grabLinks("https://en.wikipedia.org/wiki/Trains")

for x in parent.children:
    print(x.count, " " + x.link)

print(parent.name)
print(parent.link)