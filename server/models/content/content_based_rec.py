import random
from ast import literal_eval
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer


class ContentRecommender:
    def __init__(self, content_ds):
        cds = content_ds.copy()
        self.cos_sim_desc = self.create_cosine_sim_desc(cds)
        self.cos_sim_kwd = self.create_cosine_sim_kwd(cds)
        self.cos_sim_dir_cast = self.create_cosine_sim_dir_cast(cds)
        self.cos_sim_genre = self.create_cosine_sim_genre(cds)
        cds = cds.reset_index()
        self.titles = cds['title']
        self.indices = pd.Series(cds.index, index=cds['title'].apply(lambda x: str.lower(x.replace(" ", ""))))

    def create_cosine_sim_desc(self, content_ds):
        content_ds['tagline'] = content_ds['tagline'].fillna('')
        content_ds['description'] = content_ds['overview'] + content_ds['tagline']
        content_ds['description'] = content_ds['description'].fillna('')
        tf_vect = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
        tfidf_matrix_desc = tf_vect.fit_transform(content_ds['description'])
        return cosine_similarity(tfidf_matrix_desc, tfidf_matrix_desc)

    def filter_keywords(self, keywords, value_counts):
        words = []
        for i in keywords:
            if i in value_counts:
                words.append(i)
        return words

    def create_cosine_sim_kwd(self, content_ds):
        content_ds['keywords'] = content_ds['keywords'].apply(literal_eval)
        content_ds['keywords'] = content_ds['keywords'].apply(
            lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
        s = content_ds.apply(lambda x: pd.Series(x['keywords']), axis=1).stack().reset_index(level=1, drop=True)
        #s.name = 'keyword'
        val_cnts = s.value_counts()
        val_cnts = val_cnts[val_cnts > 1]
        content_ds['keywords'] = content_ds['keywords'].apply(self.filter_keywords, args=(val_cnts,))
        stemmer = SnowballStemmer('english')
        content_ds['keywords'] = content_ds['keywords'].apply(lambda x: [stemmer.stem(i) for i in x])
        content_ds['keywords'] = content_ds['keywords'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])
        content_ds['keywords'] = content_ds['keywords'].apply(lambda x: ' '.join(x))
        count_vect = CountVectorizer(analyzer='word', min_df=0, stop_words='english')
        count_matrix_kwd = count_vect.fit_transform(content_ds['keywords'])
        return cosine_similarity(count_matrix_kwd, count_matrix_kwd)

    def get_director(self, x):
        for i in x:
            if i['job'] == 'Director':
                return i['name']
        return np.nan

    def create_cosine_sim_dir_cast(self, content_ds):
        content_ds['cast'] = content_ds['cast'].apply(literal_eval)
        content_ds['crew'] = content_ds['crew'].apply(literal_eval)
        #content_ds['cast_size'] = content_ds['cast'].apply(lambda x: len(x))
        #content_ds['crew_size'] = content_ds['crew'].apply(lambda x: len(x))
        content_ds['director'] = content_ds['crew'].apply(self.get_director)
        content_ds['director'] = content_ds['director'].astype('str').apply(lambda x: [str.lower(x.replace(" ", ""))])
        #content_ds['director'] = content_ds['director'].apply(lambda x: [x, x, x])
        content_ds['cast'] = content_ds['cast'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
        content_ds['cast'] = content_ds['cast'].apply(lambda x: x[:3] if len(x) >= 3 else x)
        content_ds['cast'] = content_ds['cast'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])
        content_ds['dirast'] = content_ds['director'] + content_ds['cast']
        content_ds['dirast'] = content_ds['dirast'].apply(lambda x: ' '.join(x))
        count_vect = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
        count_matrix_dirast = count_vect.fit_transform(content_ds['dirast'])
        return cosine_similarity(count_matrix_dirast, count_matrix_dirast)

    def create_cosine_sim_genre(self, content_ds):
        content_ds['genres'] = content_ds['genres'].apply(literal_eval)
        content_ds['genres'] = content_ds['genres'].apply(
            lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
        content_ds['genres'] = content_ds['genres'].apply(lambda x: ' '.join(x))
        count_vect = CountVectorizer(analyzer='word', min_df=0, stop_words='english')
        count_matrix_gnr = count_vect.fit_transform(content_ds['genres'])
        return cosine_similarity(count_matrix_gnr, count_matrix_gnr)

    def get_sim_mov_tiles(self, title, num, sim_mat):
        idx = self.indices.get(str.lower(title.replace(" ", "")))
        if idx == None:
            return []
        movies_scores = sim_mat[idx]
        movies_indices = []
        if len(movies_scores.shape) == 1:
            movies_scores = np.reshape(movies_scores, (1, -1))
        for i in range(movies_scores.shape[0]):
            sim_scores = list(enumerate(movies_scores[i]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:(num + 1)]
            movie_indices = [i[0] for i in sim_scores]
            movies_indices += movie_indices
        movies_indices = list(dict.fromkeys(movies_indices))
        return self.titles.iloc[movies_indices]

    def recommend(self, title, num):
        sim_titles = set()
        sim_titles.update(self.get_sim_mov_tiles(title, num, self.cos_sim_genre))
        sim_titles.update(self.get_sim_mov_tiles(title, num, self.cos_sim_desc))
        sim_titles.update(self.get_sim_mov_tiles(title, num, self.cos_sim_kwd))
        sim_titles.update(self.get_sim_mov_tiles(title, num, self.cos_sim_dir_cast))
        sim_titles = list(sim_titles)
        return sim_titles
