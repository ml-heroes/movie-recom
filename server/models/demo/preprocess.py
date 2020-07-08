import json
# import datetime
import ast
import pandas as pd
import numpy as np

def clean_numeric(x):
  try:
    return float(x)
  except:
    return np.nan

class Process:
  def __init__(self, url):
    self.process_data(url)

  def process_data(self, url):
    df = pd.read_csv(url)
    df = df.drop([19730, 29503, 35587])
    df = df.drop(['imdb_id'], axis=1)
    df[df['original_title'] != df['title']][['title', 'original_title']].head()
    df['revenue'] = df['revenue'].replace(0, np.nan)
    df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
    df['budget'] = df['budget'].replace(0, np.nan)
    df['return'] = df['revenue'] / df['budget']
    df['year'] = pd.to_datetime(df['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
    df = df.drop('adult', axis=1)
    base_poster_url = 'http://image.tmdb.org/t/p/w185/'
    df['poster_img'] = "<img src='" + base_poster_url + df['poster_path'] + "' style='height:100px;'>"
    df['title'] = df['title'].astype('str')
    df['overview'] = df['overview'].astype('str')
    df['production_countries'] = df['production_countries'].fillna('[]').apply(ast.literal_eval)
    df['production_countries'] = df['production_countries'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    df['production_companies'] = df['production_companies'].fillna('[]').apply(ast.literal_eval)
    df['production_companies'] = df['production_companies'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

    df['popularity'] = df['popularity'].apply(clean_numeric).astype('float')
    df['vote_count'] = df['vote_count'].apply(clean_numeric).astype('float')
    df['vote_average'] = df['vote_average'].apply(clean_numeric).astype('float')
    df['runtime'] = df['runtime'].astype('float')
    df[df['runtime'] > 0][['runtime', 'title', 'year']].sort_values('runtime').head(10)
    df[(df['return'].notnull()) & (df['budget'] > 5e6)][['title', 'budget', 'revenue', 'return', 'year']].sort_values('return', ascending=False).head(10)
    df[(df['return'].notnull()) & (df['budget'] > 5e6) & (df['revenue'] > 10000)][['title', 'budget', 'revenue', 'return', 'year']].sort_values('return').head(10)

    df['year'] = df['year'].replace('NaT', np.nan)
    df['year'] = df['year'].apply(clean_numeric)

    df['genres'] = df['genres'].fillna('[]').apply(ast.literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    s = df.apply(lambda x: pd.Series(x['genres']),axis=1).stack().reset_index(level=1, drop=True)
    s.name = 'genres'
    df = df.drop('genres', axis=1).join(s)

    self.df = df
