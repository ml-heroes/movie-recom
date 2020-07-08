#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime

def weighted_rating(x, m, C):
    v = x['vote_count']
    R = x['vote_average']
    # Calculation based on the IMDB formula
    return (v/(v+m) * R) + (m/(m+v) * C)


#  Convert the process into a function we can utilize later
def demographic_movies(df, recent=False, percentile=0.9, years=10):
    # using a time range of the last 2 years
    if(recent == True):
        df['release_date'] = pd.to_datetime(df['release_date'])
        #greater than the start date and smaller than the end date
        start_date = datetime.now() - relativedelta(years=years)
        mask = (df['release_date'] > start_date)
        df = df.loc[mask]

    vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = df[df['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(percentile)

    q_movies = df.copy().loc[(df['vote_count'] >= m) & (df['vote_count'].notnull()) & (df['vote_average'].notnull())]
    q_movies['vote_count'] = q_movies['vote_count'].astype('int')
    q_movies['vote_average'] = q_movies['vote_average'].astype('int')
    if not q_movies.empty:
        q_movies['score'] = q_movies.apply(weighted_rating, args=(m, C), axis=1)
        q_movies = q_movies.sort_values('score', ascending=False)
        return q_movies
    else:
        return df


def weighted_rating_genre(gen_md, genre, percentile=0.9):
    df = gen_md[gen_md['genre'] == genre]
    vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = df[df['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(percentile)
    
    qualified = df[(df['vote_count'] >= m) & (df['vote_count'].notnull()) & (df['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity']]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')
    
    qualified['score'] = qualified.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average']) + (m/(m+x['vote_count']) * C), axis=1)
    qualified = qualified.sort_values('score', ascending=False).head(250)
    
    return qualified

def likeable_score(x):
    score = x['score']
    pop = x['popularity']
    return score/pop

def likeable_movies(df):
    likeable_movies = demographic_movies(df)
    likeable_movies['score'] = likeable_movies.apply(likeable_score, axis=1)
    likeable_movies = likeable_movies.sort_values('score', ascending=False)
    return likeable_movies

def popular_movies(df):
    pop = df.sort_values('popularity', ascending=False)
    return pop
