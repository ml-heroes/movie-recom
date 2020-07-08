# -*- coding: utf-8 -*-
"""User Route for Demo application."""

from flask import Blueprint, jsonify
import os
from server.main.services.demographic_service import DemographicService
from server.models.demo.preprocess import Process

route = Blueprint('demographic', __name__)

print("===Loading data into memory===")
# processed_data = Process(os.path.abspath('model/input/movies_metadata.csv'))
processed_data = Process('https://raw.githubusercontent.com/ml-heroes/ml-dataset/master/movies/movies_metadata.csv')
demographic_service = DemographicService(processed_data)
print("===Loading data complete===")

@route.route("/api/trendings")
def get_demographics():
    return demographic_service.trending().to_json(orient='records')

@route.route("/api/populars")
def get_popular():
    return demographic_service.popular().to_json(orient='records')

@route.route("/api/likeables")
def get_likeable():
    return demographic_service.likeable().to_json(orient='records')

@route.route("/api/genres/<genre>")
def get_genres(genre):
    return demographic_service.trending_genre(genre).to_json(orient='records')
