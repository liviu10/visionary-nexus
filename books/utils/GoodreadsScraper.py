import requests
import re
import json
from bs4 import BeautifulSoup


class GoodreadsScraper:
    goodreads_base_url = None
    goodreads_bookshelves_url = None

    def __init__(self, book_instance):
        self.book_instance = book_instance
        self.goodreads_base_url = "https://www.goodreads.com"
        self.goodreads_bookshelves_url = "https://www.goodreads.com/review/list/109191783?ref=nav_mybooks"
        self.book_details = {}

    def get_goodreads_link(self):
        book_instance = self.book_instance
        if book_instance.goodreads_link:
            print(f"The book {book_instance} already have a google book link! Scraping was skipped!")
        else:
            page_number = 1
            while True:
                response = requests.get(f"{self.goodreads_bookshelves_url}&page={page_number}")
                soup = BeautifulSoup(response.text, 'html.parser')
                goodreads_book_id = book_instance.goodreads_book_id
                anchor_tag = soup.find('a', href=lambda href: href and str(goodreads_book_id) in href)
                if anchor_tag:
                    goodreads_link = anchor_tag.get('href')
                    print(f"Goodreads link: {self.goodreads_base_url}{goodreads_link}")
                    return f"{self.goodreads_base_url}{goodreads_link}"
                else:
                    next_page_button = soup.find('a', class_='next_page')
                    if next_page_button:
                        page_number += 1
                    else:
                        print(f"Could not find the anchor tag with data-resource-id={goodreads_book_id} on any page.")
                        return None

    def get_goodreads_details(self):
        book_instance = self.book_instance
        if book_instance.goodreads_link:
            response = requests.get(book_instance.goodreads_link)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Get book language:
            self._get_book_language(book_instance, soup)

            # Get book authors:
            self._get_book_authors(book_instance, soup)

            # Get book cover URL:
            self._get_book_cover(book_instance, soup)

            # Get book title:
            self._get_book_title(book_instance, soup)

            # Get book genre:
            self._get_book_genre(book_instance, soup)

            # Get book rating
            self._get_book_rating(book_instance, soup)

            # Get book published date:
            self._get_book_published_date(book_instance, soup)

            # Get book description:
            self._get_book_description(book_instance, soup)

            # Get book isbn 13:
            self._get_book_isbn(book_instance, soup)

            # Get book page count:
            self._get_book_page_count(book_instance, soup)

            # Get gook status:
            self._get_book_status(book_instance, soup)

            return self.book_details
        else:
            print(f"Book {book_instance} is missing the Goodreads link")
            return self.book_details

    def _get_book_language(self, book_instance, soup):
        if hasattr(book_instance, 'language') and book_instance.language:
            print(f"The book {book_instance} already have a language set! Scraping was skipped!")
        else:
            book_language_element = soup.find('script', type='application/ld+json')
            if book_language_element:
                if book_language_element:
                    json_content = re.search(r'({.*})', book_language_element.string)
                    if json_content:
                        book_data = json.loads(json_content.group(1))
                        book_language = book_data.get('inLanguage')
                        if book_language:
                            self.book_details['language'] = book_language
                            print(f"Book language: {book_language}")
                        else:
                            print("Could not find the book language in the JSON data.")
                    else:
                        print("Could not extract JSON content from the script tag.")
                else:
                    print("Could not find the script tag with the JSON data.")
            else:
                print(f"Could not find the book language element on the page.")

    def _get_book_authors(self, book_instance, soup):
        if hasattr(book_instance, 'authors') and book_instance.authors:
            print(f"The book {book_instance} already have an author! Scraping was skipped!")
        else:
            book_author_element = soup.find('div', class_='ContributorLink__name').text.strip()
            if book_author_element:
                self.book_details['authors'] = book_author_element
                print(f"Book authors: {book_author_element}")
            else:
                print(f"Could not find the book author element on the page.")

    def _get_book_cover(self, book_instance, soup):
        if hasattr(book_instance, 'image') and book_instance.image or \
                hasattr(book_instance, 'goodreads_image_link') and book_instance.goodreads_image_link or \
                hasattr(book_instance, 'google_image_link') and book_instance.google_image_link:
            print(f"The book {book_instance} already have a cover! Scraping was skipped!")
        else:
            book_cover_element = soup.find('div', class_='BookCover__image').find('img')
            if book_cover_element:
                cover_url = book_cover_element['src']
                self.book_details['cover_url'] = cover_url
                print(f"Book cover URL: {cover_url}")
            else:
                print(f"Could not find the book cover element on the page.")

    def _get_book_title(self, book_instance, soup):
        if hasattr(book_instance, 'title') and book_instance.title:
            print(f"The book {book_instance} already have a title! Scraping was skipped!")
        else:
            book_title_element = soup.find('div', class_='Text Text__title1').text.strip()
            if book_title_element:
                self.book_details['title'] = book_title_element
                print(f"Book title: {book_title_element}")
            else:
                print(f"Could not find the book title element on the page.")

    def _get_book_genre(self, book_instance, soup):
        if hasattr(book_instance, 'genre') and book_instance.genre:
            print(f"The book {book_instance} already have a genre! Scraping was skipped!")
        else:
            self.book_details['genre'] = None

    def _get_book_rating(self, book_instance, soup):
        if hasattr(book_instance, 'rating') and book_instance.rating:
            print(f"The book {book_instance} already have a rating! Scraping was skipped!")
        else:
            book_rating_element = soup.find('div', class_='RatingStatistics__rating').text.strip()
            if book_rating_element:
                self.book_details['rating'] = book_rating_element
                print(f"Book rating: {book_rating_element}")
            else:
                print(f"Could not find the book rating element on the page.")

    def _get_book_published_date(self, book_instance, soup):
        if hasattr(book_instance, 'published_date') and book_instance.published_date:
            print(f"The book {book_instance} already have a published date! Scraping was skipped!")
        else:
            self.book_details['published_date'] = None

    def _get_book_description(self, book_instance, soup):
        if hasattr(book_instance, 'description') and book_instance.description:
            print(f"The book {book_instance} already have a description! Scraping was skipped!")
        else:
            book_description_element = soup.find('div', class_='DetailsLayoutRightParagraph__widthConstrained')
            if book_description_element:
                book_description_text = book_description_element.text.strip()
                if book_description_text:
                    book_description_element = (f"<p><span style=\"color:hsl(0, 0%, 0%);\">"
                                                f"{book_description_text}</span></p>")
                    self.book_details['description'] = book_description_element
                    print(f"Book description: {book_description_element}")
                else:
                    print("Found book description element, but it's empty.")
            else:
                print("Could not find the book description element on the page.")

    def _get_book_isbn(self, book_instance, soup):
        if hasattr(book_instance, 'isbn_13') and book_instance.isbn_13:
            print(f"The book {book_instance} already have a ISBN 13! Scraping was skipped!")
        else:
            book_isbn_element = soup.find('script', type='application/ld+json')
            if book_isbn_element:
                if book_isbn_element:
                    json_content = re.search(r'({.*})', book_isbn_element.string)
                    if json_content:
                        book_data = json.loads(json_content.group(1))
                        book_isbn = book_data.get('isbn')
                        if book_isbn:
                            self.book_details['isbn_13'] = book_isbn
                            print(f"Book ISBN 13: {book_isbn}")
                        else:
                            print("Could not find the book ISBN in the JSON data.")
                    else:
                        print("Could not extract JSON content from the script tag.")
                else:
                    print("Could not find the script tag with the JSON data.")
            else:
                print(f"Could not find the book language element on the page.")

    def _get_book_page_count(self, book_instance, soup):
        if hasattr(book_instance, 'page_count') and book_instance.page_count and book_instance.page_count > 0:
            print(f"The book {book_instance} already have a page count! Scraping was skipped!")
        else:
            book_page_count_element = soup.find('script', type='application/ld+json')
            if book_page_count_element:
                if book_page_count_element:
                    json_content = re.search(r'({.*})', book_page_count_element.string)
                    if json_content:
                        book_data = json.loads(json_content.group(1))
                        book_page_count = book_data.get('format')
                        if book_page_count:
                            self.book_details['page_count'] = book_page_count
                            print(f"Book page count: {book_page_count}")
                        else:
                            print("Could not find the book page count in the JSON data.")
                    else:
                        print("Could not extract JSON content from the script tag.")
                else:
                    print("Could not find the script tag with the JSON data.")
            else:
                print(f"Could not find the book language element on the page.")

    def _get_book_status(self, book_instance, soup):
        if hasattr(book_instance, 'book_status') and book_instance.book_status:
            print(f"The book {book_instance} already have a status! Scraping was skipped!")
        else:
            self.book_details['status'] = None
