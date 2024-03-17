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
        if hasattr(game_instance, 'image') and game_instance.image or \
                hasattr(game_instance, 'game_image_link') and game_instance.game_image_link:
            print(f"The game {game_instance} already have a cover! Scraping was skipped!")
        else:
            game_cover_element = soup.find('div', class_='game_header_image_ctn').find('img')
            if game_cover_element:
                cover_url = game_cover_element['src']
                self.game_details['cover_url'] = cover_url
                print(f"Game cover URL: {cover_url}")
            else:
                print(f"Could not find the game cover element on the page.")

    def _get_game_rating(self, game_instance, soup):
        if hasattr(game_instance, 'genre') and game_instance.genre:
            print(f"The game {game_instance} already have a rating! Scraping was skipped!")
        else:
            meta_tag = soup.find('meta', itemprop='ratingValue')
            if meta_tag and 'content' in meta_tag.attrs:
                self.game_details['rating'] = meta_tag['content']
                print(f"Game rating: {self.game_details['rating']}")
            else:
                print("Could not find the game rating element on the page.")

    def _get_game_released_date(self, game_instance, soup):
        if hasattr(game_instance, 'released_date') and game_instance.released_date:
            print(f"The game {game_instance} already have a released date! Scraping was skipped!")
        else:
            self.game_details['released_date'] = None

    def _get_game_description(self, game_instance, soup):
        if hasattr(game_instance, 'description') and game_instance.description:
            print(f"The game {game_instance} already have a description! Scraping was skipped!")
        else:
            game_description_element = soup.find('div', class_='game_description_snippet')
            if game_description_element:
                game_description_text = game_description_element.text.strip()
                if game_description_text:
                    book_description_element = (f"<p><span style=\"color:hsl(0, 0%, 0%);\">"
                                                f"{game_description_text}</span></p>")
                    self.game_details['description'] = book_description_element
                    print(f"Game description: {book_description_element}")
                else:
                    print("Found game description element, but it's empty.")
            else:
                print("Could not find the game description element on the page.")
