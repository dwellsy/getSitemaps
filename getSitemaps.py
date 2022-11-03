#!/usr/bin/env python

import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse


base_url = "https://sitemap.dwellsy.com/"
output_dir = "./output"


def save_file(url, folder, filename):
    r = requests.get(url, allow_redirects=False)
    out_filename = f"{output_dir}/{folder}/{filename}"
    with open(out_filename, "wb") as f:
        f.write(r.content)


def main():
    r = requests.get(base_url)
    print(r.content)

    root = ET.fromstring(r.content)

    xmlDict = {}
    for sitemap in root:
        children = list(sitemap)
        x = children[0].text
        if x.startswith("https://sitemap.dwellsy.com/address/"):
            path = urlparse(x).path
            pathparts = path.split("/")
            folder = pathparts[1]
            filename = pathparts[2]
            save_file(x, folder, filename)

        # xmlDict[children[0].text] = children[1].text
        # print (xmlDict[children[0]))


if __name__ == "__main__":
    main()
