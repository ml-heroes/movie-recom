# -*- coding: utf-8 -*-
"""User Route for Demo application."""

import requests
import pickle
from flask import Blueprint, jsonify
from server.main.services.demographic_service import DemographicService
from server.models.prep.preprocess import Process
from server.models.content.content_based_rec import ContentRecommender

route = Blueprint('demographic', __name__)

BASE_PATH = 'https://raw.githubusercontent.com/ml-heroes/ml-dataset/master/movies/'
LARGE_BASE_PATH = 'https://dl.dropboxusercontent.com/s/toir5bjqhl463q4/'
LOCAL_BASE_PATH = 'server/data/'
MOVIE_DB_URL = 'https://api.themoviedb.org/3/movie/{}?api_key=2085f970b90ca4a5b5047991206ede55'
BASE_POSTER_URL = 'http://image.tmdb.org/t/p/w185/'

print('>>>> Loading datasets...')
processed_data = Process(LOCAL_BASE_PATH, LOCAL_BASE_PATH, BASE_POSTER_URL)
print('<<<< Finished loading datasets\n')
print('>>>> Building demographic recommender...')
demographic_rec = DemographicService(processed_data.metadata, processed_data.genre_metadata)
print('<<<< Finished Building demographic recommender\n')
print('>>>> Building content-based recommender...')
content_rec = ContentRecommender(processed_data.metadata, processed_data.links_small,
                                 processed_data.keywords, processed_data.credits)
print('>>>> Finished building content-based recommender...')


svd = pickle.load(open("server/models/collab/svd.data", "rb"))
top_n = pickle.load(open("server/models/collab/top_n.data", "rb"))


@route.route("/api/collabs/<int:user_id>/<int:movie_id>")
def get_collaborative(user_id, movie_id):
    return jsonify(svd.predict(user_id, movie_id))


@route.route("/api/collabs/<int:user_id>")
def get_top_n(user_id):
    top_n_ratings = top_n[user_id]
    results = []
    for i in range(len(top_n_ratings)):
        mv_id = top_n_ratings[i][0]
        mv_rtng = top_n_ratings[i][1]
        mv_dtls = movies_details_from_ids([mv_id])
        if len(mv_dtls) > 0:
            mv_dtls[0]['rating'] = mv_rtng
            results += mv_dtls
    return jsonify(results)


@route.route("/api/movies/<movie_id>")
def get_movie_detail(movie_id):
    return demographic_rec.find_movie_by_id(movie_id).to_json(orient='records')


@route.route("/api/trending")
def get_demographics():
    return demographic_rec.trending().to_json(orient='records')


@route.route("/api/popular")
def get_popular():
    return demographic_rec.popular().to_json(orient='records')


@route.route("/api/likeable")
def get_likeable():
    return demographic_rec.likeable().to_json(orient='records')


@route.route("/api/genres/<genre>")
def get_genres(genre):
    return demographic_rec.trending_genre(genre).to_json(orient='records')


def movies_details_from_ids(ids):
    rslts = []
    for id in ids:
        ttl_ovw = processed_data.metadata[processed_data.metadata['id'] == id][['title', 'overview']].values
        if ttl_ovw.size > 0:
            resp = requests.get(MOVIE_DB_URL.format(id))
            resp_json = resp.json()
            rslts.append({"id": id, "title": ttl_ovw[0][0],
                          "poster_path": resp_json.get('poster_path'), "overview": ttl_ovw[0][1]})
    return rslts


def movies_details_from_titles(titles):
    results = []
    for title in titles:
        ids = processed_data.metadata[processed_data.metadata['title'] == title]['id']
        mvs_dtls = movies_details_from_ids(ids)
        results += mvs_dtls
    return results


@route.route("/api/content/<title>")
def content_based(title):
    mvs = content_rec.recommend(title, 20)
    results = movies_details_from_titles(mvs)
    return jsonify(results)
