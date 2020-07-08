# -*- coding: utf-8 -*-
"""ML_Project02_CF.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uNJij8aRvCQjgLIrwzLgB91-beDiUjH2

# Settings and Imports
"""

!pip install surprise

import pandas as pd 
import numpy as np
from collections import defaultdict
import pickle

from surprise import Reader, Dataset, SVD, accuracy
from surprise.model_selection import cross_validate, GridSearchCV, train_test_split

"""## Dataset"""

ratings = pd.read_csv('/content/drive/My Drive/Colab_Notebooks/data/movies/ratings_small.csv')
ratings.head()

print("Total number of records:", len(ratings))
print("Number of unique users:", len(ratings.userId.unique()))
print("Number of unique movies:", len(ratings.movieId.unique()))

"""## Prepare data for surprise"""

reader = Reader()
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

"""# Baseline classifier"""

trainset, testset = train_test_split(data, test_size=.2, random_state=42)
algo = SVD()

cross_validate(algo, data, measures = ['RMSE', 'MAE'], cv = 3, verbose = True)

algo.fit(trainset)

predictions = algo.test(testset)
accuracy.rmse(predictions)

uid = 1
ratings[ratings['userId'] == 1]

# get a prediction for specific users and items.
algo.predict(uid, 302)

"""# Grid Search CV"""

param_grid = {'n_epochs': [5, 10, 15], 'lr_all': [0.002, 0.005, 0.008],
              'reg_all': [0.2, 0.4, 0.6]}

gs = GridSearchCV(SVD, param_grid, measures = ['RMSE', 'MAE'], cv = 3)

gs.fit(data)
print(gs.best_score['rmse'])
print(gs.best_params['rmse'])

algo = gs.best_estimator['rmse']
algo.fit(data.build_full_trainset())

"""# API"""

def get_top_n(predictions, n = 10):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n

reader = Reader()
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

trainset = data.build_full_trainset()
algo = SVD()
algo.fit(trainset)

# Than predict ratings for all pairs (u, i) that are NOT in the training set.
testset = trainset.build_anti_testset()
predictions = algo.test(testset)

top_n = get_top_n(predictions, n=10)

# # Print the recommended items for each user
# for uid, user_ratings in top_n.items():
#     print(uid, [iid for (iid, _) in user_ratings])

"""## Get top 10 recommendations per user
Given a user
"""

top_n[1]

top_n[2]

"""## Get predicted movie rating

Given a user and a movie
"""

algo.predict(2, 904)

"""## Exporting"""

# saving the top_n for all users
pickle.dump(top_n, open("top_n.data", "wb"))

# saving the model
pickle.dump(algo, open("svd.data", "wb"))

"""## Importing"""

new_top_n = pickle.load(open("top_n.data", "rb"))
new_top_n[1]

new_algo = pickle.load(open("svd.data", "rb"))
algo.predict(2, 904)

"""# Neural Netwrok"""



"""References:
* https://surprise.readthedocs.io/en/stable/getting_started.html
* https://www.kaggle.com/ibtesama/getting-started-with-a-movie-recommendation-system
* https://www.kaggle.com/rounakbanik/movie-recommender-systems
* https://www.kaggle.com/fabiendaniel/film-recommendation-engine
* https://www.kaggle.com/fabiendaniel/film-recommendation-engine
* https://surprise.readthedocs.io/en/stable/FAQ.html
* https://surprise.readthedocs.io/en/stable/matrix_factorization.html?highlight=svd#surprise.prediction_algorithms.matrix_factorization.SVD
* https://wiki.python.org/moin/UsingPickle
"""