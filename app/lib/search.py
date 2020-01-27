import subprocess

from bs4 import BeautifulSoup
from flask import current_app

RES_P_PAGE = 8
URL_DOCID_PATH = 'ClueWeb12_B13_DocID_To_URL.txt'  # Change this path as necessary.


def search_(keyword, page):
    if not current_app.searcher:
        return
    
    hits = current_app.searcher.search(keyword, page * RES_P_PAGE + 1)
    results = [(hits[i].ldocid, hits[i].docid, extract(hits[i].content)) for i in range((page - 1) * RES_P_PAGE, min(page * RES_P_PAGE, len(hits)))]
    return results, len(hits) > page * RES_P_PAGE

def get_content_ldocid(ldocid):
    """Retrieve indexed content from Anserini"""
    if not current_app.searcher:
        return
    html = current_app.searcher.doc(int(ldocid))
    soup = BeautifulSoup(html, "html5lib")
    # Remove tags that link to other resources
    for tag in ["a", "img", "script", "link"]:
        for t in soup(tag):
            t.decompose()
    return str(soup)

def get_url_docid(docid):
    # Get the URL for the docID by calling grep
    b_url = subprocess.check_output(["grep", docid, PATH_URLS])
    url = b_url.decode('utf-8').split(',', maxsplit=1)[1].strip()
    return url
    
def extract(html):
    soup = BeautifulSoup(html, "html5lib")
    if soup.title:
        return soup.title.text[:500]
    return soup.body.text[:500]

def set_rm3():
    current_app.searcher.set_rm3_reranker(rm3_output_query=True)
    current_app.rm3 = True

def unset_rm3():
    current_app.searcher.unset_rm3_reranker()
    current_app.rm3 = False

def set_bm25(k, b):
    current_app.searcher.set_bm25_similarity(k, b)

