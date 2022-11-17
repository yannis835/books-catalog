import tornado.web
import books
import json


class BookHandler(tornado.web.RequestHandler):
    def initialize(self, books):
        self.books = books
        
    def get(self, id):
        print("[BookHandler] Executing HTTP GET on Book Content {0}".format(id))

        # IN REAL CONDITIONS, DO NOT LET "*" HERE AND SET A REAL DOMAIN
        self.set_header("Access-Control-Allow-Origin", "*")

        b = self.books.get_book(id)
        # If the book exists...
        if b:
            # Return the book description
            self.set_header("Content-Type", "application/x-json")
            self.write(json.dumps(b))
            self.write("\n")
            self.set_status(200)

        # If the book does not exist
        else:
            self.set_status(204)


    def delete(self, id):
        print("[BookHandler] Executing HTTP DELETE on Book Content {0}".format(id))

        # IN REAL CONDITIONS, DO NOT LET "*" HERE AND SET A REAL DOMAIN
        self.set_header("Access-Control-Allow-Origin", "*")

        # Deleting the book
        result = self.books.del_book(id)
        # Deletion performed correctly
        if result:
            self.set_header("Content-Type", "text/plain")
            self.write("Book {0} deleted".format(id))
            self.write("\n")
            self.set_status(200)
        # Book not found
        else:
            self.set_header("Content-Type", "text/plain")
            self.write("Book {0} not found".format(id))
            self.write("\n")
            self.set_status(404)


    def options(self, id):
        # IN REAL CONDITIONS, DO NOT LET "*" HERE AND SET A REAL DOMAIN
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "accept, content-type")
        self.set_header("Access-Control-Allow-Methods", "GET, DELETE, OPTIONS")
        self.set_header("Content-Length", "0")
        self.set_header("Content-Type", "text/plain")
        self.set_status(200)

