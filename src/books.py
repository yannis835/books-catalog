import json

class Books:

    def __init__(self, config):
        self.config = config
        # Internal book storage
        self.books = []
        # Book identifier generator
        self.id = 0

    # Add a book to the catalog
    def add_book(self, title, author, year, editor):
        # Generate a new id for the book
        self.id += 1

        # Create the book object
        new_book = {}
        new_book["Id"] = str(self.id)
        new_book["Title"] = title
        new_book["Author"] = author
        new_book["Year"] = year
        new_book["Editor"] = editor

        # Add the book to the internal book storage
        self.books.append(new_book)

        print("[Books] Book {0} added to catalog".format(json.dumps(new_book)))
        print("[Books] Books catalog: {0}".format(json.dumps(self.books)))
        return new_book


    # Delete a book from the catalog
    def del_book(self, id):
        # Find the book by iterating on the list of books and checking the id
        found = False
        for idx, b in enumerate(self.books):
            # If id is found, then delete the book
            if b["Id"] == id:
                index = idx
                found = True
                # Remove the book for the internal book storage
                del self.books[idx]

        print("[Books] Book {0} deleted from catalog".format(id))
        print("[Books] Books catalog: {0}".format(json.dumps(self.books)))
        return found


    # Get the book description
    def get_book(self, id):
        # Find the book by iterating on the list of books and checking the id
        for idx, b in enumerate(self.books):
            if b["Id"] == id:
                print("[Books] Book {0} found: {1}".format(id, json.dumps(b)))
                return b

    # Get the list of all books
    def get_all_books(self):
        print("[Books] Books catalog: {0}".format(self.books))
        return self.books

    # Get the list of ids of all books
    def get_all_books_ids(self):
        books_ids = []
        for idx, b in enumerate(self.books):
            books_ids.append(b["Id"])

        print("[Books] Books Ids: {0}".format(books_ids))
        return books_ids

