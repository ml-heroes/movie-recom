from flask import Blueprint, jsonify
import pickle

route = Blueprint('collab', __name__)

svd = pickle.load(open("server/models/collab/svd.data", "rb" ))
top_n = pickle.load(open("server/models/collab/top_n.data", "rb" ))

@route.route("/api/collabs/svd/<user_id>/<movie_id>")
def get_collaborative(user_id, movie_id):
    return svd.predict(user_id, movie_id).to_json(orient='records')


@route.route("/api/collabs/top/<user_id>")
def get_collaborative(user_id):
    return top_n[user_id].to_json(orient='records')
