from os import path
from ast import literal_eval
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

DS_PATH = 'https://raw.githubusercontent.com/ml-heroes/ml-dataset/master/movies/'
LOCAL_DS_PATH = 'data'

md = pd.read_csv(path.join(DS_PATH, 'movies_metadata.csv'))
links = pd.read_csv(path.join(DS_PATH, 'links_small.csv'))
credits = pd.read_csv(path.join(LOCAL_DS_PATH, 'credits.csv'))
keywords = pd.read_csv(path.join(DS_PATH, 'keywords.csv'))

# The following three movies' records are corrupted
md = md.drop([19730, 29503, 35587])

md['id'] = md['id'].astype('int')
links = links[links['tmdbId'].notnull()]['tmdbId'].astype('int')
keywords['id'] = keywords['id'].astype('int')
credits['id'] = credits['id'].astype('int')

smd = md[md['id'].isin(links)]
smd = smd.merge(credits, on='id')
smd = smd.merge(keywords, on='id')

smd['tagline'] = smd['tagline'].fillna('')
smd['description'] = smd['overview'] + smd['tagline']
smd['description'] = smd['description'].fillna('')

tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2),
                     min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(smd['description'])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

smd = smd.reset_index()
titles = smd['title']
indices = pd.Series(smd.index, index=smd['title'])


def get_recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:31]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices]


smd['cast'] = smd['cast'].apply(literal_eval)
smd['crew'] = smd['crew'].apply(literal_eval)
smd['keywords'] = smd['keywords'].apply(literal_eval)
smd['cast_size'] = smd['cast'].apply(lambda x: len(x))
smd['crew_size'] = smd['crew'].apply(lambda x: len(x))


def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan


smd['director'] = smd['crew'].apply(get_director)

smd['cast'] = smd['cast'].apply(lambda x: [i['name']
                                           for i in x] if isinstance(x, list) else [])

smd['cast'] = smd['cast'].apply(lambda x: x[:3] if len(x) >= 3 else x)

smd['keywords'] = smd['keywords'].apply(
    lambda x: [i['name'] for i in x] if isinstance(x, list) else [])


get_recommendations('The Social Network').head(10)
