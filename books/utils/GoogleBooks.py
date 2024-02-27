import requests
import main.settings


class GoogleBooks:
    google_books_api_url = main.settings.GOOGLE_BOOKS_API_ENDPOINT
    google_books_api_key = main.settings.GOOGLE_BOOKS_API_KEY

    def __init__(self, book_instance):
        self.book_instance = book_instance

    def get_book_details(self):
        author = self.book_instance.authors
        title = self.book_instance.title
        published_date = self.book_instance.published_date
        isbn_13 = self.book_instance.isbn_13
        search_criteria = f"author {author}, title {title}, published date {published_date} and isbn {isbn_13}"

        if author and title and published_date and isbn_13:
            query = f"{published_date}+inauthor:{author}+intitle:{title}+isbn:{isbn_13}"
            search_book_url = f"{self.google_books_api_url}?q={query}"

            try:
                search_book = requests.get(search_book_url)
                book_details = search_book.json()
                if book_details['totalItems'] == 0:
                    print(f"Unable to find book details by {search_criteria}!")
                else:
                    if 'items' in book_details and len(book_details['items']) > 0 and 'volumeInfo' in book_details['items'][0]:
                        items = book_details['items']
                        return items[0]['volumeInfo']
                    else:
                        print(f"There was a problem in getting the Google Books API volume info: {str(book_details)}!")
            except requests.RequestException as e:
                print(f"There was a problem communicating with the Google Books API: {str(e)}!")
        else:
            print(f"In order to search for book details you need to specify: {search_criteria}!")
