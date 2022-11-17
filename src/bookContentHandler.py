import tornado.web
import json

import books
import booksContent


class BookContentHandler(tornado.web.RequestHandler):
    def initialize(self, books, booksContent):
        self.books = books
        self.booksContent = booksContent

    async def put(self, id):
        print("[BookContentHandler] Executing HTTP PUT on Book Content {0}".format(id))

        # IN REAL CONDITIONS, DO NOT LET "*" HERE AND SET A REAL DOMAIN
        self.set_header("Access-Control-Allow-Origin", "*")

        b = self.books.get_book(id)
        # If the book exists...
        if b:
            # Set the content of the book
            try:
                ct = self.request.headers["content-type"]
                if ct == "text/plain":
                    # Text content
                    location, message = await self.booksContent.set_content (id, self.request.body.decode("utf-8"), ct)
                else:
                    # Binary content
                    location, message = await self.booksContent.set_content (id, self.request.body, ct)
            except KeyError:
                # Binary content
                location, message = await self.booksContent.set_content (id, self.request.body, "application/octet-stream")
            
            # In case the content storage has been processed correctly
            if message == None:
                self.set_header("Location", location)
                self.set_status(200)
            # In case of error during the content storage
            else:
                self.set_header("Content-Type", "text/plain")
                self.write(message)
                self.write("\n")
                self.set_status(500)

        # If the book does not exist
        else:
            self.set_header("Content-Type", "text/plain")
            self.write("Book {0} not found".format(id))
            self.write("\n")
            self.set_status(404)


    async def delete(self, id):
        print("[BookContentHandler] Executing HTTP DELETE on Book Content {0}".format(id))

        # IN REAL CONDITIONS, DO NOT LET "*" HERE AND SET A REAL DOMAIN
        self.set_header("Access-Control-Allow-Origin", "*")

        b = self.books.get_book(id)
        # If the book exists...
        if b:
            # Delete the book content
            deleted, message = await self.booksContent.delete_content (id)
            # If deletion has been performed
            if deleted:
                # Deletion performed correctly
                if message == None:
                    self.set_header("Content-Type", "text/plain")
                    self.write("Book Content {0} deleted".format(id))
                    self.write("\n")
                    self.set_status(200)
                # No realm deletion because content was not existing
                else:
                    self.set_header("Content-Type", "text/plain")
                    self.write(message)
                    self.write("\n")
                    self.set_status(404)
            else:
                self.set_header("Content-Type", "text/plain")
                self.write(message)
                self.write("\n")
                self.set_status(500)

        # If the book does not exist
        else:
            self.set_header("Content-Type", "text/plain")
            self.write("Book {0} not found".format(id))
            self.write("\n")
            self.set_status(404)

    def options(self, id):
        # IN REAL CONDITIONS, DO NOT LET "*" HERE AND SET A REAL DOMAIN
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "accept, content-type")
        self.set_header("Access-Control-Allow-Methods", "PUT, DELETE, OPTIONS")
        self.set_header("Content-Length", "0")
        self.set_header("Content-Type", "text/plain")
        self.set_status(200)

