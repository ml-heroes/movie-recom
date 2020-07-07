# -*- coding: utf-8 -*-
"""
DemographicService class - This class holds the method related to Demographic manipulations.
"""

from server.model.demo.demographics import demographic_movies, weighted_rating_genre, likeable_movies
# data = process_data.df;
# gen_md = process_data.gen_md;

class DemographicService:
    def __init__(self, data):
        self.data = data

    def trending(self):
        return 'Hello'
    
    def popular(self):
        pass

    def likeable(self):
        pass
