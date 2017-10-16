# CVPaperScraper

CVPaperScraper is tiny script for downloading pdfs from CVFoundation Open Access Repository: 
http://openaccess.thecvf.com/menu.py

or Arxiv: https://arxiv.org/

This script also make all paper list as html file.

## Requirements
- Python3 (Confirmed in Python3.5)
- BeautifulSoup4 (https://pypi.python.org/pypi/beautifulsoup4)

## Usage
`python downloadpdf.py`

## Notice
- Turn True the flag `search_from_arxiv` on downloadpdf.py if you want to get pdf from ArXiv. 
    - Not able to download pdfs from CVF Open Access page yet (I confirmed in Oct. 16th).
- arxivsearch modlue searches from paper title, however it returns papar that has most similar title query. So this script downloads different paper if the paper on ICCV is not stored to ArXiv. (To be fixed.)
