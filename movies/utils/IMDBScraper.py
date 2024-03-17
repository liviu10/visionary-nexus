import requests
import re
import json
from bs4 import BeautifulSoup


class IMDBScraper:
    steam_base_url = None

    def __init__(self, movie_instance):
        self.movie_instance = movie_instance
        self.movie_details = {}

    def get_movie_details(self):
        movie_instance = self.movie_instance
        if movie_instance.movie_link:
            response = requests.get(movie_instance.movie_link)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get movie image:
            self._get_movie_image(movie_instance, soup)

            # Get movie launch date:
            self._get_movie_launch_date(movie_instance, soup)

            # Get movie description:
            self._get_movie_description(movie_instance, soup)

            return self.movie_details
        else:
            print(f"Movie {movie_instance} is missing the IMDB link")
            return self.movie_details

    def _get_movie_image(self, movie_instance, soup):
        if hasattr(movie_instance, 'image') and movie_instance.image or \
                hasattr(movie_instance, 'movie_image_link') and movie_instance.movie_image_link:
            print(f"The movie {movie_instance} already have a cover! Scraping was skipped!")
        else:
            self.movie_details['cover_url'] = None

    def _get_movie_launch_date(self, movie_instance, soup):
        if hasattr(movie_instance, 'launch_date') and movie_instance.launch_date:
            print(f"The movie {movie_instance} already have a launch date! Scraping was skipped!")
        else:
            self.movie_details['launch_date'] = None

    def _get_movie_description(self, movie_instance, soup):
        if hasattr(movie_instance, 'description') and movie_instance.description:
            print(f"The movie {movie_instance} already have a description! Scraping was skipped!")
        else:
            self.movie_details['description'] = None
