from flask import Blueprint, jsonify

from server.models.content.preprocess import preprocess
from server.models.content.content_based_rec import ContentRecommender

route = Blueprint('content', __name__)

credits, keywords, links, links_small, metadata, ratings, ratings_small = preprocess.retrieve_datasets()
smd = preprocess.create_content_ds(metadata, links_small, keywords, credits)
content_rec = ContentRecommender(smd)

@route.route("/api/contents/<title>/<movie_id>")
def recommend_content(title, movie_id):
    return content_rec.recommend(title, movie_id).to_json(orient='records')
