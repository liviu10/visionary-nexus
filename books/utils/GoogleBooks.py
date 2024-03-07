import requests
import main.settings
from settings.utils import LogEventPayload


class GoogleBooks:
    google_books_base_url = None
    google_books_api_key = None
    log_data = None

    def __init__(self, book_instance):
        self.google_books_base_url = 'https://www.googleapis.com/books/v1/volumes'
        self.google_books_api_key = main.settings.GOOGLE_BOOKS_API_KEY
        self.book_instance = book_instance

    def get_google_book_details_by_author_and_title(self):
        if self._check_search_parameters():
            author = self.book_instance.authors
            title = self.book_instance.title
            published_date = self.book_instance.published_date
            isbn_13 = self.book_instance.isbn_13
            query = f"{published_date}+inauthor:{author}+intitle:{title}+isbn:{isbn_13}"
            search_book_url = f"{self.google_books_base_url}?q={query}&key={self.google_books_api_key}"
            google_book_details = self._search_book(search_book_url, author, title, isbn_13)
            return google_book_details
        else:
            self._create_log_data(
                "Notice",
                f"Unable to perform the search because both author and title does not exist!",
            )

    def _check_search_parameters(self):
        if hasattr(self.book_instance, 'authors') and \
                hasattr(self.book_instance, 'title') and hasattr(self.book_instance, 'isbn_13'):
            authors = self.book_instance.authors
            title = self.book_instance.title
            isbn_13 = self.book_instance.isbn_13

            if authors and title and isbn_13:
                return True
            else:
                self._create_log_data(
                    "Notice",
                    f"The book ID {self.book_instance.id} does not have any author, title or isbn_13!",
                )
                return False
        else:
            self._create_log_data(
                "Notice",
                f"The book instance {self.book_instance.id} is missing author, title or isbn_13!",
            )
            return False

    def _search_book(self, search_book_url, author, title, isbn_13):
        try:
            search_criteria = f"author {author}, title {title}, isbn_13 {isbn_13}"
            search_book = requests.get(search_book_url)
            google_book_details = search_book.json()
            if google_book_details['totalItems'] == 0:
                self._create_log_data(
                    "Notice",
                    f"Unable to find book details by {search_criteria}!",
                    search_book_url,
                    google_book_details
                )
            else:
                if 'items' in google_book_details and len(google_book_details['items']) > 0 and 'volumeInfo' in \
                        google_book_details['items'][0]:
                    items = google_book_details['items']
                    print(f"items: {items}")
                    return items[0]['volumeInfo']
                else:
                    self._create_log_data(
                        "Notice",
                        f"There was a problem in getting the Google Books API volume info: \
                        {str(google_book_details)}!",
                    )
        except requests.RequestException as e:
            self._create_log_data(
                "Error",
                f"There was a problem communicating with the Google Books API: {str(e)}!",
            )
            return False

    def _create_log_data(self, log_type, description, request_details=None, response_details=None):
        self.log_data = {
            "log_type": log_type,
            "description": description,
            "request_details": f"{request_details}",
            "response_details": f"{response_details}",
        }
        LogEventPayload(self.log_data)
