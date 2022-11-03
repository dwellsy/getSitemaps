#!/usr/bin/env python

import requests
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
from shutil import rmtree
import os

base_url = "https://dwellsy-sitemap.us-west-2.elasticbeanstalk.com"
output_dir = "./output"


def save_file(url, folder, filename):
    out_filename = f"{output_dir}/{folder}/{filename}"
    r = requests.get(url, allow_redirects=False, verify=False)
    if r.status_code != 200:
        # try it again after parsing URL
        url = f"{base_url}{urlparse(url).path}"
        r = requests.get(url, allow_redirects=False, verify=False)
        with open(out_filename, "wb") as f:
            f.write(r.content)

    else:
        with open(out_filename, "wb") as f:
            f.write(r.content)


def save_index(objects, folder, filename):
    print('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    out_filename = f"{output_dir}/{folder}/{filename}"
    with open(out_filename, "a") as f:
        f.write('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for item in objects:
            loc = item["loc"]
            lastmod = item["lastmod"]
            f.write("  <sitemap>\n")
            f.write(f"    <loc>{loc}</loc>\n")
            f.write(f"    <lastmod>{lastmod}</lastmod>\n")
            f.write("  <sitemap>\n")

        f.write("</sitemapindex>\n")


def cleanup():
    try:
        rmtree("./output")
    except Exception:
        pass

    os.mkdir("./output/")
    os.mkdir("./output/listing-history/")


def main():
    cleanup()
    r = requests.get(base_url, verify=False)

    root = ET.fromstring(r.content)

    objects = []

    for sitemap in root:
        children = list(sitemap)
        url = children[0].text
        lastmod = children[1].text
        if url.startswith(f"https://sitemap.dwellsy.com/listing-history/"):
            path = urlparse(url).path
            pathparts = path.split("/")
            folder = pathparts[1]
            filename = pathparts[2]
            objects.append({"loc": url, "lastmod": lastmod})
            # print(url)
            save_file(url, folder, filename)

    save_index(objects, "listing-history", "sitemapindex.xml")

    # xmlDict[children[0].text] = children[1].text
    # print (xmlDict[children[0]))


if __name__ == "__main__":
    main()
