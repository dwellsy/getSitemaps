#!/usr/bin/env python

import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse


base_url = "https://dwellsy-sitemap.us-west-2.elasticbeanstalk.com"
output_dir = "./output"


def save_file(url, folder, filename):
    r = requests.get(url, allow_redirects=False, verify=False)
    out_filename = f"{output_dir}/{folder}/{filename}"
    with open(out_filename, "wb") as f:
        f.write(r.content)


def main():
    r = requests.get(base_url, verify=False)

    root = ET.fromstring(r.content)

    output_index = ""

    xmlDict = {}

    for sitemap in root:
        children = list(sitemap)
        url = children[0].text
        lastmod = children[1].text
        if url.startswith(f"https://sitemap.dwellsy.com/listing-history/"):
            path = urlparse(url).path
            pathparts = path.split("/")
            folder = pathparts[1]
            filename = pathparts[2]
            print(f"""<sitemap>
  <loc>{url}</loc>
  <lastmod>{lastmod}</loc>
</sitemap>""")
            # print(url)
            # save_file(x, folder, filename)

        # xmlDict[children[0].text] = children[1].text
        # print (xmlDict[children[0]))


if __name__ == "__main__":
    main()
