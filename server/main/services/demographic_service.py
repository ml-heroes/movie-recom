# -*- coding: utf-8 -*-
"""
DemographicService class - This class holds the method related to Demographic manipulations.
"""

from server.models.demo.demographics import (demographic_movies,
    weighted_rating_genre,
    likeable_movies,
    popular_movies)

LIMIT = 10

class DemographicService:
    def __init__(self, processed_data=None):
        self.df = processed_data

    def trending(self):
        movies = demographic_movies(self.df)
        return movies.head(LIMIT)
    
    def popular(self):
        movies = popular_movies(self.df)
        return movies.head(LIMIT)

    def likeable(self):
        movies = likeable_movies(self.df)
        return movies.head(LIMIT)

    def trending_genre(self, genre):
        movies = weighted_rating_genre(self.df, genre)
        return movies.head(LIMIT)

    def find_movie_by_id(self, movie_id):
        movie = self.data.iloc[movie_id]
        return movie
