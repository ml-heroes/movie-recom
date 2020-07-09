import json
import ast
from os import path
import pandas as pd
import numpy as np
from ast import literal_eval
from nltk.stem.snowball import SnowballStemmer


class Process:
    def __init__(self, ds_path, big_ds_path, base_poster_url):
        print("===Setting up data===")
        self.DS_PATH = ds_path
        self.BIG_DS_PATH = big_ds_path
        credits, keywords, links, links_small, metadata, ratings, ratings_small = self.retrieve_datasets()
        self.credits = self.process_credits(credits)
        self.keywords = self.process_keywords(keywords)
        self.links = self.process_links(links)
        self.links_small = self.process_links(links_small)
        self.metadata = self.process_metadata(metadata, base_poster_url)
        self.genre_metadata = self.process_genre_data(metadata)
        self.ratings = self.process_ratings(ratings)
        self.ratings_small = self.process_ratings(ratings_small)
        print("===Finished setting up data===")

    def retrieve_datasets(self):
        print('>>>> Reading credits.csv...')
        credits = pd.read_csv(path.join(self.BIG_DS_PATH, 'credits.csv'))
        print('>>>> Reading keywords.csv...')
        keywords = pd.read_csv(path.join(self.DS_PATH, 'keywords.csv'))
        print('>>>> Reading links.csv...')
        links = pd.read_csv(path.join(self.DS_PATH, 'links.csv'))
        print('>>>> Reading links_small.csv...')
        links_small = pd.read_csv(path.join(self.DS_PATH, 'links_small.csv'))
        print('>>>> Reading movies_metadata.csv...')
        metadata = pd.read_csv(path.join(self.DS_PATH, 'movies_metadata.csv'))
        #ratings = pd.read_csv(path.join(LOCAL_DS_PATH, 'ratings.csv'))
        ratings = None
        print('>>>> Reading ratings_small.csv...')
        ratings_small = pd.read_csv(path.join(self.DS_PATH, 'ratings_small.csv'))
        return credits, keywords, links, links_small, metadata, ratings, ratings_small

    def process_metadata(self, md, base_poster_url):
        print('>>>> Preparing metadata...')
        if md is None:
            return md
        # These three movies' records are corrupted
        md = md.drop([19730, 29503, 35587])
        md['id'] = md['id'].astype('int')
        md = md.drop(['imdb_id'], axis=1)
        md[md['original_title'] != md['title']][['title', 'original_title']].head()
        md['revenue'] = md['revenue'].replace(0, np.nan)
        md['budget'] = pd.to_numeric(md['budget'], errors='coerce')
        md['budget'] = md['budget'].replace(0, np.nan)
        md['return'] = md['revenue'] / md['budget']
        md['year'] = pd.to_datetime(md['release_date'], errors='coerce').apply(
            lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
        md = md.drop('adult', axis=1)
        md['poster_img'] = "<img src='" + base_poster_url + md['poster_path'] + "' style='height:100px;'>"
        md['title'] = md['title'].astype('str')
        md['overview'] = md['overview'].astype('str')
        md['production_countries'] = md['production_countries'].fillna('[]').apply(ast.literal_eval)
        md['production_countries'] = md['production_countries'].apply(
            lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
        md['production_companies'] = md['production_companies'].fillna('[]').apply(ast.literal_eval)
        md['production_companies'] = md['production_companies'].apply(
            lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

        md['popularity'] = md['popularity'].apply(self.clean_numeric).astype('float')
        md['vote_count'] = md['vote_count'].apply(self.clean_numeric).astype('float')
        md['vote_average'] = md['vote_average'].apply(self.clean_numeric).astype('float')
        md['runtime'] = md['runtime'].astype('float')
        md[md['runtime'] > 0][['runtime', 'title', 'year']].sort_values('runtime').head(10)
        md[(md['return'].notnull()) & (md['budget'] > 5e6)][['title', 'budget',
                                                             'revenue', 'return', 'year']].sort_values('return', ascending=False).head(10)
        md[(md['return'].notnull()) & (md['budget'] > 5e6) & (md['revenue'] > 10000)][[
            'title', 'budget', 'revenue', 'return', 'year']].sort_values('return').head(10)

        md['year'] = md['year'].replace('NaT', np.nan)
        md['year'] = md['year'].apply(self.clean_numeric)

        md['tagline'] = md['tagline'].fillna('')
        md['description'] = md['overview'] + md['tagline']
        md['description'] = md['description'].fillna('')

        md['genres_vect'] = md['genres'].apply(lambda x: ' '.join(x))

        return md

    def process_genre_data(self, df):
        df['genres'] = df['genres'].fillna('[]').apply(ast.literal_eval).apply(
            lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
        s = df.apply(lambda x: pd.Series(x['genres']), axis=1).stack().reset_index(level=1, drop=True)
        s.name = 'genres'
        genre_df = df.drop('genres', axis=1).join(s)
        return genre_df

    def get_director(self, x):
        for i in x:
            if i['job'] == 'Director':
                return i['name']
        return np.nan

    def process_credits(self, crds):
        if crds is None:
            return crds
        print('>>>> Preparing credits...')
        crds['id'] = crds['id'].astype('int')
        crds['cast'] = crds['cast'].apply(literal_eval)
        crds['crew'] = crds['crew'].apply(literal_eval)
        crds['cast_size'] = crds['cast'].apply(lambda x: len(x))
        crds['crew_size'] = crds['crew'].apply(lambda x: len(x))
        crds['director'] = crds['crew'].apply(self.get_director)
        crds['director'] = crds['director'].astype('str').apply(lambda x: [str.lower(x.replace(" ", ""))])
        crds['cast'] = crds['cast'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
        crds['cast'] = crds['cast'].apply(lambda x: x[:3] if len(x) >= 3 else x)
        crds['cast'] = crds['cast'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])
        crds['dirast'] = crds['director'] + crds['cast']
        crds['dirast'] = crds['dirast'].apply(lambda x: ' '.join(x))
        return crds

    def filter_keywords(self, keywords, value_counts):
        words = []
        for i in keywords:
            if i in value_counts:
                words.append(i)
        return words

    def process_keywords(self, kwds):
        if kwds is None:
            return kwds
        print('>>>> Preparing keywords...')
        kwds['id'] = kwds['id'].astype('int')
        kwds['keywords'] = kwds['keywords'].apply(literal_eval)
        kwds['keywords'] = kwds['keywords'].apply(
            lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
        s = kwds.apply(lambda x: pd.Series(x['keywords']), axis=1).stack().reset_index(level=1, drop=True)
        val_cnts = s.value_counts()
        val_cnts = val_cnts[val_cnts > 1]
        kwds['keywords'] = kwds['keywords'].apply(self.filter_keywords, args=(val_cnts,))
        stemmer = SnowballStemmer('english')
        kwds['keywords'] = kwds['keywords'].apply(lambda x: [stemmer.stem(i) for i in x])
        kwds['keywords'] = kwds['keywords'].apply(lambda x: [str.lower(i.replace(" ", "")) for i in x])
        kwds['keywords'] = kwds['keywords'].apply(lambda x: ' '.join(x))
        return kwds

    def process_links(self, lnks):
        if lnks is None:
            return lnks
        print('>>>> Preparing links...')
        lnks = lnks[lnks['tmdbId'].notnull()]['tmdbId'].astype('int')
        return lnks

    def process_ratings(self, rts):
        if rts is None:
            return rts
        print('>>>> Preparing ratings...')
        rts['movieId'] = rts['movieId'].astype('int')
        return rts

    def clean_numeric(self, x):
        try:
            return float(x)
        except:
            return np.nan
