# -*- coding: utf-8 -*-
"""Default api blueprints for Demo application."""


import pandas as pd
import importlib
from flask import Blueprint, jsonify
from ast import literal_eval
import os
import sys
import requests

sys.path.append('ml')
sys.path.append('data')
import preprocess
from content_based_rec import ContentRecommender


credits, keywords, links, links_small, metadata, ratings, ratings_small = preprocess.retrieve_datasets()
smd = preprocess.create_content_ds(metadata, links_small, keywords, credits)
content_rec = ContentRecommender(smd)

route = Blueprint('default', __name__)

@route.route("/api")
def hello():
    return "Hello from Flask using Python 3.6.2!!"
POSTER_API_URL = 'https://api.themoviedb.org/3/movie/{}?api_key=2085f970b90ca4a5b5047991206ede55'

@route.route("/api/content/<title>")
def content_based(title):
    mvs = content_rec.recommend(title,3)
    results = dict()
    for mv in mvs:
        mv_ids = metadata[metadata['title'] == mv]['id']
        for mv_id in mv_ids:
            mv_ovw = metadata[metadata['id'] == mv_id]['overview'].values[0]
            resp = requests.get(POSTER_API_URL.format(mv_id))
            resp_json = resp.json()
            results[mv_id] = {"title":mv, "poster_path":resp_json.get('poster_path'), "overview":mv_ovw}
    return results


@route.route("/api/ping")
def ping():
    return jsonify({"status": 200, "msg": "This message is coming from Flask backend!"})
