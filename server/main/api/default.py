# -*- coding: utf-8 -*-
"""Default api blueprints for Demo application."""

import pandas as pd
import importlib
from flask import Blueprint, jsonify

import sys
sys.path.append('ml')
sys.path.append('data')
import preprocess
from content_based_rec import ContentRecommender


credits, keywords, links, links_small, metadata, ratings, ratings_small = preprocess.retrieve_datasets()
smd = preprocess.create_content_ds(metadata, links_small, keywords, credits)
content_rec = ContentRecommender(smd)
content_rec.recommend('Titanic', 3)
route = Blueprint('default', __name__)


@route.route("/api")
def hello():
    return "Hello from Flask using Python 3.6.2!!"


@route.route("/api/ping")
def ping():
    return jsonify({"status": 200, "msg": "This message is coming from Flask backend!"})
