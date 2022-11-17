import tornado.web
import books
import json

class BooksCatalogHandler(tornado.web.RequestHandler):
    def initialize(self, books, config):
        self.books = books
        self.config = config

    def prepare(self):
        # Parse the HTTP request body, as a JSON content
        self.args = {}
        try:
            if self.request.headers["Content-Type"] == "application/json" or self.request.headers["Content-Type"] == "application/xjson" or self.request.headers["Content-Type"] == "application/x-json":
                self.args = json.loads(self.request.body)
        except KeyError:
            None

    def get(self):
        print("[BooksCatalogHandler] Executing HTTP GET on Books Catalog")

        # IN REAL CONDITIONS, DO NOT LET "*" HERE AND SET A REAL DOMAIN
        self.set_header("Access-Control-Allow-Origin", "*")

        request = self.request

        # Response will contain URLs. Start of these URL may be forced by the
        # "externalBaseUrl" configration parameter.
        # If not set, the protocol and host of the incoming request is used.
        response_urls_start = request.protocol + "://" + request.host
        if "externalBaseUrl" in self.config:
            # Avoid having a double "/" in the URL
            if self.config["externalBaseUrl"][-1] == '/':
                response_urls_start = self.config["externalBaseUrl"][:-1]
            else:
                response_urls_start = self.config["externalBaseUrl"]

        # Extract the query parameters of the URL: offset and pageSize
        offset = int (self.get_argument("offset", 1))
        if offset <= 0:
            offset = 1
        pageSize = int (self.get_argument("pageSize", 5))
        if pageSize <= 0:
            pageSize = 5

        # Get the list of book ids matching the offset and pageSize
        # (iterate through all books and only get the ones matching the good page)
        books_ids_urls = []
        books_ids = self.books.get_all_books_ids()
        for idx, id in enumerate(books_ids):
            if (idx + 1) < offset:
                next
            elif (idx + 1) >= (offset + pageSize):
                break
            else:
                # Each book is represented by the URL where to get the book definition
                books_ids_urls.append(response_urls_start + "/v1/books/" + id)

        # Building the result:
        # - offset, pageSize
        # - previousPage URL and nextPage URL
        # - the list of books URLs for the current page
        res = {}
        res["offset"] = offset
        res["pageSize"] = pageSize
        res["books"] = books_ids_urls
        if offset != 1 and len(books_ids_urls) != 0:
            if offset <= pageSize:
                res["previousPage"] = response_urls_start + "/v1/books?offset=1&pageSize=" + str(pageSize)
            else:
                res["previousPage"] = response_urls_start + "/v1/books?offset=" + str(offset - pageSize) + "&pageSize=" + str(pageSize)
        if (offset + pageSize) <= len (books_ids):
            res["nextPage"] = response_urls_start + "/v1/books?offset=" + str(offset + pageSize) + "&pageSize=" + str(pageSize)

        self.set_header("Content-Type", "application/x-json")
        self.write(json.dumps(res))
        self.write("\n")


    def post(self):
        print("[BooksCatalogHandler] Executing HTTP POST on Books Catalog")

        # IN REAL CONDITIONS, DO NOT LET "*" HERE AND SET A REAL DOMAIN
        self.set_header("Access-Control-Allow-Origin", "*")

        title = ""
        author = ""
        year = ""
        editor = ""

        # Book title and author are mandatory field. Retrieved from the JSON body
        try:
            title = self.args["Title"]
            author = self.args["Author"]
        except KeyError:
            # If either title or author are not present, then error
            self.set_header("Content-Type", "text/plain")
            self.write("Title and author are mandatory fields for a book")
            self.write("\n")
            self.set_status(400)
            return

        if title == "" or author == "":
            self.set_header("Content-Type", "text/plain")
            self.write("Title and Author shall not be empty")
            self.write("\n")
            self.set_status(400)
            return

        # Year and editor are optional fields
        if "Year" in self.args:
            year = self.args["Year"]
        if "Editor" in self.args:
            editor = self.args["Editor"]

        # Add the book to the catalog
        b = self.books.add_book(title, author, year, editor)
        # If ok, then return the URL where to get the book definition in the Location header
        if b:
            request = self.request

            # Response will contain URLs. Start of these URL may be forced by the
            # "externalBaseUrl" configration parameter.
            # If not set, the protocol and host of the incoming request is used.
            response_url_start = request.protocol + "://" + request.host
            if "externalBaseUrl" in self.config:
                # Avoid having a double "/" in the URL
                if self.config["externalBaseUrl"][-1] == '/':
                    response_url_start = self.config["externalBaseUrl"][:-1]
                else:
                    response_url_start = self.config["externalBaseUrl"]

            self.set_header("Location", response_url_start + "/v1/books/" + b["Id"])
            self.set_header("Content-Type", "application/x-json")
            self.write(json.dumps(b))
            self.write("\n")

    def options(self):
        # IN REAL CONDITIONS, DO NOT LET "*" HERE AND SET A REAL DOMAIN
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "accept, content-type")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.set_header("Content-Length", "0")
        self.set_header("Content-Type", "text/plain")
        self.set_status(200)
