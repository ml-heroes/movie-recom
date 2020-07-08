from flask import Blueprint, jsonify
import pickle

route = Blueprint('collab', __name__)

svd = pickle.load(open("server/models/collab/svd.data", "rb" ))
top_n = pickle.load(open("server/models/collab/top_n.data", "rb" ))

@route.route("/api/collabs/<int:user_id>/<int:movie_id>")
def get_collaborative(user_id, movie_id):
    return jsonify(svd.predict(user_id, movie_id))

@route.route("/api/collabs/<int:user_id>")
def get_top_n(user_id):
    return jsonify(top_n[user_id])
