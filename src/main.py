import sys
import getopt

import tornado.ioloop
import tornado.web

from books import Books
from booksContent import BooksContent

from booksCatalogHandler import BooksCatalogHandler
from bookHandler import BookHandler
from bookContentHandler import BookContentHandler


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Books Catalog Microservice v1")
        self.write("\n")

# Declare the endpoints of the micro-service
def make_app(config):
    return tornado.web.Application([
        (r"/v1", MainHandler),
        (r"/v1/books", BooksCatalogHandler, dict(books = books, config = config)),
        (r"/v1/books/([0-9]+)", BookHandler, dict(books = books)),
        (r"/v1/books/([0-9]+)/content", BookContentHandler, dict(books = books, booksContent = booksContent)),
        ])


# Micro-service usage
def usage():
    print ("Micro-service: BooksCatalog")
    print ("  Run command: python main.py [options]")
    print ("  Options:")
    print ("    -h / --help: display this help")
    print ("    -c / --config: specify configuration file (default is 'config/BooksCatalog.properties')")
    print ("  Configuration file variables:")
    print ("    listeningPort: port on which the micro-service listens to (default 9990)")
    print ("    externalBaseUrl: if the micro-service is deployed behind a Reverse Proxy, state here the public base URL to be used in API responses URLs")
    print ("    BooksContentService.baseUrl: base URL of the BooksContent micro-service")

# Main
if __name__ == "__main__":
    print ("Starting server...")
		
    # Get parameters from the command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:", ["help", "config="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    configFileName = "config/BooksCatalog.properties"
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-c", "--config"):
            configFileName = arg

    # Read configuration from configuration file
    defaultConfig = {"listeningPort": 9990, "BooksContentService.baseUrl": "http://books-content:9991/"}
    with open(configFileName) as f:
        l = [line.split("=") for line in f.readlines()]
        while ['\n'] in l: l.remove (['\n'])
        config = {key.strip(): value.strip() for key, value in l}
    config = {**defaultConfig, **config}

    # Instantiate helper classes
    books = Books(config)
    booksContent = BooksContent(config)

    # Create the App
    app = make_app(config)
    app.listen(config["listeningPort"])
    print ("BooksCatalog server is ready!")
    tornado.ioloop.IOLoop.current().start()
