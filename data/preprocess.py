from os import path
import pandas as pd
import numpy as np

DS_PATH = 'https://raw.githubusercontent.com/ml-heroes/ml-dataset/master/movies/'
LOCAL_DS_PATH = 'data'


def retrieve_datasets():
    credits = pd.read_csv(path.join(LOCAL_DS_PATH, 'credits.csv'))
    keywords = pd.read_csv(path.join(DS_PATH, 'keywords.csv'))
    links = pd.read_csv(path.join(DS_PATH, 'links.csv'))
    links_small = pd.read_csv(path.join(DS_PATH, 'links_small.csv'))
    metadata = pd.read_csv(path.join(DS_PATH, 'movies_metadata.csv'))
    #ratings = pd.read_csv(path.join(LOCAL_DS_PATH, 'ratings.csv'))
    ratings = None
    ratings_small = pd.read_csv(path.join(DS_PATH, 'ratings_small.csv'))
    return credits, keywords, links, links_small, metadata, ratings, ratings_small


def create_content_ds(metadata, links, keywords, credits):
    # The following three movies' records are corrupted
    metadata = metadata.drop([19730, 29503, 35587])

    metadata['id'] = metadata['id'].astype('int')
    links = links[links['tmdbId'].notnull()]['tmdbId'].astype('int')
    keywords['id'] = keywords['id'].astype('int')
    credits['id'] = credits['id'].astype('int')

    smd = metadata[metadata['id'].isin(links)]
    smd = smd.merge(credits, on='id')
    smd = smd.merge(keywords, on='id')
    return smd
