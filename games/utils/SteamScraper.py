import requests
import re
import json
from bs4 import BeautifulSoup


class SteamScraper:
    steam_base_url = None

    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.game_details = {}

    def get_game_details(self):
        game_instance = self.game_instance
        if game_instance.game_link:
            response = requests.get(game_instance.game_link)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get game image:
            self._get_game_image(game_instance, soup)

            # Get game rating:
            self._get_game_rating(game_instance, soup)

            # Get game released date:
            self._get_game_released_date(game_instance, soup)

            # Get game description:
            self._get_game_description(game_instance, soup)

            return self.game_details
        else:
            print(f"Game {game_instance} is missing the Steam link")
            return self.game_details

    def _get_game_image(self, game_instance, soup):
        if hasattr(game_instance, 'image') and game_instance.image and \
                hasattr(game_instance, 'game_image_link') and game_instance.game_image_link:
            print(f"The game {game_instance} already have a cover! Scraping was skipped!")
        else:
            self.game_details['cover_url'] = None

    def _get_game_rating(self, game_instance, soup):
        if hasattr(game_instance, 'genre') and game_instance.genre:
            print(f"The game {game_instance} already have a rating! Scraping was skipped!")
        else:
            self.game_details['rating'] = None

    def _get_game_released_date(self, game_instance, soup):
        if hasattr(game_instance, 'released_date') and game_instance.released_date:
            print(f"The game {game_instance} already have a released date! Scraping was skipped!")
        else:
            self.game_details['released_date'] = None

    def _get_game_description(self, game_instance, soup):
        if hasattr(game_instance, 'description') and game_instance.description:
            print(f"The game {game_instance} already have a description! Scraping was skipped!")
        else:
            self.game_details['description'] = None
