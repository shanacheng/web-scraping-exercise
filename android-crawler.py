# Shana Cheng

from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import os

#path for outFiles
path = "/Users/shanacheng/Documents/337_2020/outFiles"
url = "https://developer.android.com"


p = "/reference/android/app/package-summary"
os.makedirs(path, exist_ok=True)
html = requests.get(url+p)

soup = BeautifulSoup(html.content, "html.parser")

get_links = soup.findAll("td", {"class": "jd-linkcol"})

path_links = []

for link in get_links:
    path_links.append(link.a["href"])


# def dep(tag):
#     return tag.has_attr("data-version-deprecated")


count = 0
for x in range(len(path_links)-1):
    key = path_links[x]
    filename = key[23:]
    h = requests.get(url+key)
    soup2 = BeautifulSoup(h.content, "html.parser")
    content = soup2.findAll("div")
    z = 0
    cautions = []
    notes = []
    titles = []
    for y in content:

        if y.has_attr("data-version-deprecated"):

            caution = y.find("p", {"class": "caution"})
            note = y.find("p", {"class": "note"})

            if caution is not None:
                inter = "This interface was deprecated"
                if y.h3.contents != ['Public methods'] and y.h3.contents != ['Constants'] and y.h3.contents != ['Public constructors'] and y.h3.contents != ['Developer Guides'] and y.h3.contents != ['Inherited methods'] and y.h3.contents != ['Lifecycle'] and y.h3.contents != ['Inherited constants'] and y.h3.contents != ['Nested classes'] and y.h3.contents != ['Inherited XML attributes']:

                    title = y.h3.string

                    with open(os.path.join(path, filename), 'a') as fp:

                        fp.write(str(title)+":")

                        for p in caution.contents:
                            fp.write(p.getText()+"\n")

                    z = 1

                else:
                    a = 0
            if note is not None:
                note = y.findAll("p", {"class": "note"})

                if note is not None:
                    for n in note:
                        if y.h3.contents != ['Constants'] and y.h3.contents != ['Developer Guides'] and y.h3.contents != ['Nested classes']:
                            title = y.h3.string

                            with open(os.path.join(path, filename), 'a') as fp:
                                if title not in titles:
                                    fp.write(str(title)+":")
                                    titles.append(title)
                                for x in n.contents:
                                    if isinstance(x, NavigableString):
                                        fp.write(x+"\n")
                                        z = 1
                                    if isinstance(x, Tag):
                                        fp.write(x.getText())

        else:
            note = y.findAll("p", {"class": "note"})
            if note is not None:
                for n in note:
                    if y.h3.contents != ['Constants'] and y.h3.contents != ['Developer Guides'] and y.h3.contents != ['Nested classes']:
                        title = y.h3.string
                        with open(os.path.join(path, filename), 'a') as fp:

                            if title not in titles:
                                fp.write(str(title)+":")
                                titles.append(title)
                            for x in n.contents:
                                if isinstance(x, NavigableString):
                                    fp.write(x+"\n")
                                if isinstance(x, Tag):
                                    fp.write(x.getText())

                    z = 1
