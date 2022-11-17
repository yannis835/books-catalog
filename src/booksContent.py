import tornado.httpclient

class BooksContent:

    def __init__(self, config):
        self.config = config

    # Returns:
    # - 1st parameter: The URL where to get the created content, None in case of error
    # - 2nd parameter: The message to be sent back to the client in case of error, None otherwise
    async def set_content(self, bookId, content, contentType):
        http_client = tornado.httpclient.AsyncHTTPClient()

        # Call the BookContentService endpoint to set the content
        req = tornado.httpclient.HTTPRequest(url = self.config["BooksContentService.baseUrl"] + "v1/bookscontent/" + bookId, method = "PUT", headers = {"content-type": contentType}, body = content)
        try:
            response = await http_client.fetch(req)
        except tornado.httpclient.HTTPError as e:
            print("[BooksContent] Error calling BookContent micro-service: status code {0}".format(e.response.code))
            return None, e.response.body.decode("utf-8")

        # Call executed correctly
        if response.code == 200:
            print("[BooksContent] Book Content {0} set with {1} bytes".format(bookId, len(content)))
            return response.headers["Location"], None
        # Call executed with error
        else:
            print("[BooksContent] Error calling BookContent micro-service: status code {0}".format(response.code))
            return None, response.body.decode("utf-8")


#    async def has_content(self, bookId):


    # Returns:
    # - 1st parameter: True if the content no longer exists, False otherwise
    # - 2nd parameter: The message to be sent back to the client in case of error, None otherwise
    async def delete_content(self, bookId):
        http_client = tornado.httpclient.AsyncHTTPClient()

        # Call the BookContentService endpoint to delete the content
        req = tornado.httpclient.HTTPRequest(url = self.config["BooksContentService.baseUrl"] + "v1/bookscontent/" + bookId, method = "DELETE")
        try:
            response = await http_client.fetch(req)
        except tornado.httpclient.HTTPError as e:
            # Code 404 means that the content does not exist
            if e.response.code == 404:
                print("[BooksContent] Error calling BookContent micro-service: status code {0}".format(e.response.code))
                return True, e.response.body.decode("utf-8")
            else:
                print("[BooksContent] Error calling BookContent micro-service: status code {0}".format(e.response.code))
                return False, e.response.body.decode("utf-8")

        # Call executed correctly
        if response.code == 200:
            print("[BooksContent] Book Content {0} deleted".format(bookId))
            return True, None
        # Call executed with error
        else:
            print("[BooksContent] Error calling BookContent micro-service: status code {0}".format(response.code))
            return False, response.body.decode("utf-8")

