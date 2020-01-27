from flask import Flask, jsonify, request, render_template, url_for, redirect

from app import app
from forms import SearchForm
from lib.search import *


@app.route('/')
def main():
    form = SearchForm()
    return render_template('main.html', form=form)


@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('q', default='')
    page = request.args.get('page', default=1, type=int)

    if keyword == '':
        return redirect(url_for('main'))

    form = SearchForm()
    res, more = search_(keyword, page)

    next_url = url_for('search', q=keyword, page=page + 1) if more else None
    prev_url = url_for('search', q=keyword, page=page - 1) if page > 1 else None

    return render_template('results.html', results=res, page=page, next_url=next_url, prev_url=prev_url, form=form)


@app.route('/display/<ldocid>', methods=['GET'])
def display(ldocid):
    return get_content_ldocid(ldocid)


@app.route('/goto/<docid>')
def goto(docid):
    return redirect(get_url_docid(docid))


@app.route('/api/search',methods=['GET'])
def api_search():
    # Returns a jsonified results of `search` method
    keyword = request.args.get('q', default='')
    page = request.args.get('page', default=1, type=int)

    res = search_(keyword, page)

    return jsonify({
        'hits': res,
        'number': len(res),
        'args': {
            'q': keyword,
            'page': page
        }
    })


@app.route('/rm3on')
def rm3_setter():
    set_rm3()
    return redirect(url_for('search'))


@app.route('/rm3off')
def rm3_unsetter():
    unset_rm3()
    return redirect(url_for('search'))

