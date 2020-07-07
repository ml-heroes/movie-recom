# -*- coding: utf-8 -*-
"""User Route for Demo application."""

from flask import Blueprint, jsonify
import os
from server.main.services.demographic_service import DemographicService
from server.model.demo.preprocess import Process

route = Blueprint('demographic', __name__)

print("===Loading data into memory===")
# processed_data = Process(os.path.abspath('model/input/movies_metadata.csv'))
processed_data = Process('https://raw.githubusercontent.com/ml-heroes/ml-dataset/master/movies/movies_metadata.csv')
demographic_service = DemographicService(processed_data)
print("===Loading data complete===")

@route.route("/api/demographics")
def get_demographics():
    return jsonify(demographic_service.trending())
