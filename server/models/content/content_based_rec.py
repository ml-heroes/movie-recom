import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

MAX_DESC_WORDS = 10000
MAX_KWD_WORDS = 500


class ContentRecommender:
    def __init__(self, metadata, links, keywords, credits):
        cds = metadata[metadata['id'].isin(links)]
        cds = cds.merge(credits, on='id')
        cds = cds.merge(keywords, on='id')
        self.cos_sim_desc = self.create_cosine_sim_desc(cds)
        self.cos_sim_soup = self.create_cosine_sim_soup(cds)
        #self.cos_sim_kwd = self.create_cosine_sim_kwd(cds)
        #self.cos_sim_dir_cast = self.create_cosine_sim_dir_cast(cds)
        #self.cos_sim_genre = self.create_cosine_sim_genre(cds)
        cds = cds.reset_index()
        self.titles = cds['title']
        self.indices = pd.Series(cds.index, index=cds['title'].apply(lambda x: str.lower(x.replace(" ", ""))))

    def create_cosine_sim_desc(self, content_ds):
        print('>>>> Building similarity matrix for description...')
        tf_vect = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
        tfidf_matrix_desc = tf_vect.fit_transform(content_ds['description'])
        return cosine_similarity(tfidf_matrix_desc, tfidf_matrix_desc)

    def create_cosine_sim_kwd(self, content_ds):
        print('>>>> Building similarity matrix for keywords...')
        count_vect = CountVectorizer(analyzer='word', min_df=0, stop_words='english', max_features=MAX_KWD_WORDS)
        count_matrix_kwd = count_vect.fit_transform(content_ds['keywords'])
        return cosine_similarity(count_matrix_kwd, count_matrix_kwd)

    def create_cosine_sim_dir_cast(self, content_ds):
        print('>>>> Building similarity matrix for cast and crew...')
        count_vect = CountVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0,
                                     stop_words='english', max_features=MAX_KWD_WORDS)
        count_matrix_dirast = count_vect.fit_transform(content_ds['dirast'])
        return cosine_similarity(count_matrix_dirast, count_matrix_dirast)

    def create_cosine_sim_genre(self, content_ds):
        print('>>>> Building similarity matrix for genres...')
        count_vect = CountVectorizer(analyzer='word', min_df=0, stop_words='english', max_features=MAX_KWD_WORDS)
        count_matrix_gnr = count_vect.fit_transform(content_ds['genres_vect'])
        return cosine_similarity(count_matrix_gnr, count_matrix_gnr)

    def create_cosine_sim_soup(self, content_ds):
        print('>>>> Building similarity matrix for keywords, genre, director, and cast...')
        soup = content_ds['keywords'] + content_ds['dirast'] + content_ds['genres_vect']
        count_vect = CountVectorizer(analyzer='word', min_df=0, stop_words='english', ngram_range=(1, 2))
        count_matrix_soup = count_vect.fit_transform(soup)
        return cosine_similarity(count_matrix_soup, count_matrix_soup)

    def get_sim_mov_titles(self, title, num, sim_mat):
        idx = self.indices.get(str.lower(title.replace(" ", "")))
        if idx is None:
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
        sim_titles.update(self.get_sim_mov_titles(title, num, self.cos_sim_desc))
        sim_titles.update(self.get_sim_mov_titles(title, num, self.cos_sim_soup))
        #sim_titles.update(self.get_sim_mov_titles(title, num, self.cos_sim_kwd))
        #sim_titles.update(self.get_sim_mov_titles(title, num, self.cos_sim_genre))
        #sim_titles.update(self.get_sim_mov_titles(title, num, self.cos_sim_dir_cast))
        sim_titles = list(sim_titles)
        return sim_titles
