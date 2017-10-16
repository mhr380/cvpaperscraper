#!/usr/bin/env python3
# coding: utf-8

import os
import urllib.request
import socket
socket.setdefaulttimeout(10) # set timeout length as 10[s]

from bs4 import BeautifulSoup

import arxivsearch as arxiv

#
# turn True this flag to get paper from ArXiv
#
search_from_arxiv = True 

#
# information of ICCV open access page
#
base_url        = 'http://openaccess.thecvf.com/'
html_url        = 'ICCV2017.py'
pdf_folder_url  = 'content_ICCV_2017/papers/'


save_html_name = 'iccv2017.html' # index page
conference_name = 'ICCV2017' # use as html header.
pdf_local_folder_name = 'iccv2017/' # local directory for storing pdfs


#
# make directory for storing pdfs if it does not exist
#
if not os.path.exists(pdf_local_folder_name):
    os.makedirs(pdf_local_folder_name)


#
# parsing openaccess page to obtain paper titles using BeautifulSoup4
#
req = urllib.request.Request(base_url + html_url)
html = urllib.request.urlopen(req)
soup = BeautifulSoup(html, 'html.parser')

paper_infos = soup.find('dl')
paper_titles = paper_infos.find_all('dt', attrs={'class': 'ptitle'})
links = paper_infos.find_all('a')


with open(save_html_name, 'w') as f:
    f.write('<h1>' + conference_name + '</h1>')

    paper_id = 0
    for n, link in enumerate(links):

        link_url = str(link.get('href'))

        if pdf_folder_url in link_url:

            paper_title = paper_titles[paper_id].a.string
            print('downloading {}'.format(paper_title)

            if search_from_arxiv:
                pdf_url = arxiv.search_from_title(paper_title)
            else:
                pdf_url = base_url + link_url


            http_status_code = urllib.request.urlopen(pdf_url).getcode() # 200 is OK. Other numbers (such as 404) are NG

            if http_status_code is 200: # if remote url exists
                save_name = os.path.join(pdf_local_folder_name, str(paper_id) + u'.pdf')

                try:
                    urllib.request.urlretrieve(pdf_url, save_name)
                    tag_string = '<a href=' + save_name + '>' + paper_title + '</a>'

                except socket.Timeouterror:
                    print('timeout')
                    tag_string = paper_title

            else: # url not found
                tag_string = paper_title


            tag_string += '<br> \n'
            f.write(tag_string)

            paper_id += 1
