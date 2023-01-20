import requests
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

        def complete_request(self, author):
                # generate GET request
                tw_headers = {"Authorization": "Bearer YOUR_TWITTER_API_KEY_HERE"}
                tw_url = "https://api.twitter.com/2/tweets/search/recent?query=from:{}&tweet.fields=author_id&max_results=30".format(author)

                # connect to endpoint
                tw_response = requests.request("GET", tw_url, headers=tw_headers)
                tw_response_json = tw_response.json()

                # generate HTML response
                result = '<!doctype html><html lang="en"><head><meta charset="UTF-8"><style> body { font-family: Arial; color: #a9a9a9; background-color: #1e1e1e; } </style></head>'
                for data_item in tw_response_json["data"]:
                        title = data_item["text"]
                        end_link_start = title.rfind('http') # trim trailing link
                        result += ''.join(('<h2>', title[:end_link_start], '</h2>'))
                result += "</body></html>"

                self.wfile.write(result.encode())

        def do_GET(self):

                if len(self.path) > 1 and "." not in self.path:
                        self.send_response(200)
                        self.end_headers()

                        self.complete_request(self.path[1:])
                else:
                        self.send_response(404)
                        self.end_headers()

                        self.wfile.write("bad request".encode())

httpd = HTTPServer(('0.0.0.0', 8898), SimpleHTTPRequestHandler)
httpd.serve_forever()
