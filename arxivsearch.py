#!/usr/bin/env python3
# coding: utf-8

import urllib

import urllib.request
import re
import datetime as dt
import xml
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup


def search_from_title(paper_title):

    paper_title_q = paper_title.replace(' ', '+')

    api_url = 'http://export.arxiv.org/api/query?'
    api_url += 'search_query=' + paper_title_q
    api_url += '&start=0&max_results=1'


    opener = urllib.request.build_opener()
    xml = opener.open(api_url)
    tree = ET.parse(xml)
    root = tree.getroot()

    pdf_link_url = None

    for element in root:
        for e in element:
            link_url = e.attrib.get('href')
            if link_url is not None:
                link_url = str(link_url)

                if 'pdf' in link_url:
                    # get http://arxiv.org/pdf/1705.07162v1
                    # then replace to http://arxiv.org/pdf/1705.07162.pdf
                    pdf_link_url = re.sub(r'v[0-9]', '.pdf', link_url)
                    pdf_link_url = pdf_link_url.replace('http', 'https')

    return pdf_link_url


if __name__ == '__main__':

    pdf_link_url = search_from_title('A Lightweight Approach for On-The-Fly Reflectance Estimation')
    print(pdf_link_url)