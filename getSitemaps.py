#!/usr/bin/env python

import requests
import xml.etree.ElementTree as ET


base_url = "https://sitemap.dwellsy.com/"
def main():
  r = requests.get(base_url)
  print(r.content)

  root = ET.fromstring(r.content)

  xmlDict = {}
  for sitemap in root:
    children = list(sitemap)
    x = children[0].text
    if x.startswith("https://sitemap.dwellsy.com/address/"):
      print(x)

    # xmlDict[children[0].text] = children[1].text
    # print (xmlDict[children[0])) 





if __name__ == "__main__":
  main()
