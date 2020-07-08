import json
import ast
from os import path
import pandas as pd
import numpy as np


class Process:
    def __init__(self, ds_path, big_ds_path):
        self.DS_PATH = ds_path
        self.BIG_DS_PATH = big_ds_path
        credits, keywords, links, links_small, metadata, ratings, ratings_small = self.retrieve_datasets()
        self.credits = self.process_credits(credits)
        self.keywords = self.process_keywords(keywords)
        self.links = self.process_links(links)
        self.links_small = self.process_links(links_small)
        self.metadata = self.process_metadata(metadata)
        self.ratings = self.process_ratings(ratings)
        self.ratings_small = self.process_ratings(ratings_small)

    def retrieve_datasets(self):
        credits = pd.read_csv(path.join(self.BIG_DS_PATH, 'credits.csv'))
        keywords = pd.read_csv(path.join(self.DS_PATH, 'keywords.csv'))
        links = pd.read_csv(path.join(self.DS_PATH, 'links.csv'))
        links_small = pd.read_csv(path.join(self.DS_PATH, 'links_small.csv'))
        metadata = pd.read_csv(path.join(self.DS_PATH, 'movies_metadata.csv'))
        #ratings = pd.read_csv(path.join(LOCAL_DS_PATH, 'ratings.csv'))
        ratings = None
        ratings_small = pd.read_csv(path.join(self.DS_PATH, 'ratings_small.csv'))
        return credits, keywords, links, links_small, metadata, ratings, ratings_small

    def process_metadata(self, md):
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

        md['genres'] = md['genres'].fillna('[]').apply(ast.literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
        s = md.apply(lambda x: pd.Series(x['genres']),axis=1).stack().reset_index(level=1, drop=True)
        s.name = 'genres'
        md = md.drop('genres', axis=1).join(s)

        return md

    def process_credits(self, crds):
        if crds is None:
            return crds
        crds['id'] = crds['id'].astype('int')
        return crds

    def process_keywords(self, kwds):
        if kwds is None:
            return kwds
        kwds['id'] = kwds['id'].astype('int')
        return kwds

    def process_links(self, lnks):
        if lnks is None:
            return lnks
        lnks = lnks[lnks['tmdbId'].notnull()]['tmdbId'].astype('int')
        return lnks

    def process_ratings(self, rts):
        if rts is None:
            return rts
        rts['movieId'] = rts['movieId'].astype('int')
        return rts

    def clean_numeric(self, x):
        try:
            return float(x)
        except:
            return np.nan
