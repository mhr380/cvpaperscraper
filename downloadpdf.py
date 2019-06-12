#!/usr/bin/env python3
# coding: utf-8

import os
import urllib.request
import socket
socket.setdefaulttimeout(10) # set timeout length as 10[s]

from bs4 import BeautifulSoup
from tqdm import tqdm

import arxivsearch as arxiv

# turn True this flag to get paper from ArXiv
search_from_arxiv = False

# information of ICCV open access page
conf_name = 'CVPR'
conf_year = str(2019)

base_url        = 'http://openaccess.thecvf.com/'
html_url        = '{}{}.py'.format(conf_name, conf_year)
pdf_folder_url  = 'content_{}_{}/papers/'.format(conf_name, conf_year)


save_html_name = '{}{}.html'.format(conf_name, conf_year) # index page
conference_name = '{}{}'.format(conf_name, conf_year) # use as html header.
pdf_local_folder_name = '{}{}/'.format(conf_name, conf_year) # local directory for storing pdfs

# make directory for storing pdfs if it does not exist
if not os.path.exists(pdf_local_folder_name):
    os.makedirs(pdf_local_folder_name)

# parsing openaccess page to obtain paper titles using BeautifulSoup4
req = urllib.request.Request(base_url + html_url)
html = urllib.request.urlopen(req)
soup = BeautifulSoup(html, 'html.parser')

paper_infos = soup.find('dl')
paper_titles = paper_infos.find_all('dt', attrs={'class': 'ptitle'})
links = paper_infos.find_all('a')

with open(save_html_name, 'w') as f:
    f.write('<h1>' + conference_name + '</h1>')

    paper_id = 0
    for n, link in enumerate(tqdm(links)):

        link_url = str(link.get('href'))

        if pdf_folder_url in link_url:

            paper_title = paper_titles[paper_id].a.string

            if search_from_arxiv:
                full_url = arxiv.search_from_title(paper_title)
            else:
                full_url = base_url + link_url

            pdf_file_name = link_url.split('/')[-1]

            http_status_code = urllib.request.urlopen(full_url).getcode() # 200 is OK. Other numbers (such as 404) are NG

            if http_status_code is 200: # if remote url exists
                save_name = os.path.join(pdf_local_folder_name, pdf_file_name)

                try:
                    urllib.request.urlretrieve(full_url, save_name)
                    tag_string = '<a href=' + save_name + '>' + paper_title + '</a>'

                except socket.Timeouterror:
                    print('timeout')
                    tag_string = paper_title

            else: # url not found
                print('url not found')
                tag_string = paper_title

            tag_string += '<br> \n'
            f.write(tag_string)

            paper_id += 1
