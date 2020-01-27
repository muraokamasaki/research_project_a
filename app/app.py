from flask import Flask
from pyserini.search import pysearch


# Location of the clueweb 12 Disk b index
INDEX_DIR = '/ir/index/lucene-index.cw12b13.pos+docvectors+transformed'

app = Flask(__name__)
app.searcher = pysearch.SimpleSearcher(INDEX_DIR)
app.rm3 = False # Tracks state of RM3 Reranking

import routes
