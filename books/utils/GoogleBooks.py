import requests


class GoogleBooks:
    google_books_api_url = 'https://www.googleapis.com/books/v1/volumes'
    google_books_api_key = 'AIzaSyAHl2zCwrcshodNuaG1953Vu1i52WkSaaM'

    def __init__(self, book_instance):
        self.book_instance = book_instance

    def get_google_book_description(self):
        author = self.book_instance.authors
        title = self.book_instance.title
        if author and title:
            search_book_url = f"{self.google_books_api_url}?q=inauthor:{author}+intitle:{title}"
            try:
                search_book = requests.get(search_book_url)
                book_data = search_book.json()
                if 'totalItems' in book_data and book_data['totalItems'] == 0:
                    print(f"Unable to find details in Google Books by author: {author} and title: {title}")
                else:
                    google_book_id = book_data['items'][0]['id']
                    book_details_url = f"{self.google_books_api_url}/{google_book_id}"
                    try:
                        book_details = requests.get(book_details_url)
                        book_details_data = book_details.json()
                        if 'totalItems' in book_details_data and book_details_data['totalItems'] == 0:
                            print(f"Unable to find details in Google Books by ID: {google_book_id}, author: {author} and title: {title}")
                        else:
                            print(f"Book details data: {book_details_data['volumeInfo']}")
                            if 'description' in book_details_data['volumeInfo']:
                                description = book_details_data['volumeInfo']['description']
                            else:
                                print(f"Missing description in Google Books for author: {author} and title: {title}")
                                description = None
                            return description
                    except requests.RequestException as e:
                        print(f"Unable to find details in Google Books by ID: {google_book_id}, author: {author} and title: {title}")
            except requests.RequestException as e:
                print(f"Unable to find details in Google Books by author: {author} and title: {title}")
        else:
            print(f"In order to get the google book id you need to specify both author: {author} and title: {title}")

