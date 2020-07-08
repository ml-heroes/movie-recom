# -*- coding: utf-8 -*-
"""
DemographicService class - This class holds the method related to Demographic manipulations.
"""

from server.model.demo.demographics import (demographic_movies,
    weighted_rating_genre,
    likeable_movies,
    popular_movies)

# data = process_data.df;
# gen_md = process_data.gen_md;
LIMIT = 15

class DemographicService:
    def __init__(self, processed_data=None):
        self.df = processed_data.df
        self.gen_md = processed_data.gen_md

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
        movies = weighted_rating_genre(self.gen_md, genre)
        return movies.head(LIMIT)
