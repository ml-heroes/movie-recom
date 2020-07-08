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

def trending(df, percentile=0.9):
    vote_counts = df[df['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = df[df['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(percentile)

    q_movies = df.copy().loc[(df['vote_count'] >= m) & (df['vote_count'].notnull()) & (df['vote_average'].notnull())]
    q_movies['vote_count'] = q_movies['vote_count'].astype('int')
    q_movies['vote_average'] = q_movies['vote_average'].astype('int')
    q_movies['score'] = q_movies.apply(weighted_rating, args=(m, C), axis=1)
    q_movies = q_movies.sort_values('score', ascending=False)
    
    return q_movies


#  Convert the process into a function we can utilize later
def demographic_movies(df, recent=False, years=10):
    # using a time range of the last 2 years
    # if(recent == True):
    #     start_date = datetime.now() - relativedelta(years=years)
    #     mask = (df['release_date'] > start_date)
    #     df = df.loc[mask]

    return trending(df)


def weighted_rating_genre(df, genre):
    movie_genres = df[df['genres'] == genre]
    return trending(movie_genres)

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
