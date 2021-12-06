#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import pandas as pd
import csv
import os

app = Flask(__name__, static_url_path='/static')

def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))

root = root_dir() + '/'

def fmt(c):
    if c.startswith('https'):
        c = '<a href="%s" target=_blank>Ссылка</a>' % (c)
    return c

def filter_table(filename, q, ofs, per_page, key):

    f = open(root+filename, encoding="utf-8")
    rows = csv.DictReader(f, delimiter=',', quotechar='"')
    fields = rows.fieldnames

    data = {}
    data['headers'] = fields
    data['rows'] = []

    res = []
    for row in rows:
        if key and 'id' in row.keys() and key!=row['id']:
            continue
        if not q or any(q.lower() in (str(v)).lower() for v in row.values()):
            res.append(row)

    data['rows'] = res[ofs:ofs+per_page]
    return data

@app.route('/', methods=['GET', 'POST'])
def index():

    filename = 'df.csv'
    q = request.args.get('q') or ''
    ofs = 0
    per_page = 20

    key = request.args.get('id') or ''
    data = filter_table(filename, q, ofs, per_page, key)
    
    text = ''
    if key:
        text = data['rows'][0]['text']
        text = text.replace('\n', '<br>')

    return render_template('index.html', data=data, id=key, result=text, q=q)


if __name__ == '__main__':
    app.run(debug=True)
