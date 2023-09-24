#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

FORMAT = 'utf-8'


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)

        #print(f"DATA --> {self.data}\n\n\n")
        request_input = self.data.decode(FORMAT).split('\n')
        #print(f"REQUEST INPUT --> {request_input}\n\n\n")
        request_line = request_input[0].split()
        #print(f"REQUEST LINE --> {request_line}\n\n\n")
        method = request_line[0]
        path = request_line[1]
        #print(f"METHOD --> {method}\n\n\n")
        print(f"PATH --> {path}\n\n\n")

        

        #need to respond to redirects

        if method == "GET":
            #maybe make more general get request method in the future?
            if path == "/base.css":
                self.serve_css("./www/base.css")
            elif path == "/deep.css": 
                self.serve_css("./www/deep/deep.css")
            elif path == "/index.html" or path == "/" or path == "/www/":
                self.serve_html("./www/index.html")
            elif path == "/deep/":
                self.serve_html("./www/deep/index.html")
            elif path == "/deep":
                self.send_301_redirect("/deep/")
            elif path == "/www":
                self.send_301_redirect("/www/")

            else:
                self.send_404_response()

        else:
            self.send_405_response()
            


        #parse_lines = self.data.decode

    def send_301_redirect(self, path):
        response_header = "HTTP/1.1 301 Moved Permanently\r\n" 
        response_header += "Location: " + path + "\r\n\r\n"
        
        self.request.sendall(response_header.encode(FORMAT))

    def send_404_response(self):
        response_header = "HTTP/1.1 404 Not Found\r\n\r\n"
        message = "Not Found"

        self.request.sendall(response_header.encode(FORMAT) + message.encode(FORMAT))

    def send_405_response(self):
        response_header = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
        message = "Method Not Allowed"

        self.request.sendall(response_header.encode(FORMAT) + message.encode(FORMAT))

    """
    def send_200_response(self, content_type, content):
        response_header = "HTTP/1.1 200 OK\r\n" + content_type

        self.request.sendall(response_header.encode(FORMAT) + content.encode(FORMAT))
    """

    def serve_css(self, css_path):
        print("Serve css function")

        response_header = "HTTP/1.1 200 OK\r\n" + "Content-Type: text/css\r\n"
        #response_header_1 = "HTTP/1.1 200 OK\r\n"
        #content_type = "Content-Type: text/css\r\n"

        content = ""
        try:
            with open(css_path, "r") as css_file:
                content = css_file.read()
                print(content)
        except FileNotFoundError:
            self.send_404_response()

        #self.send_200_response()

        self.request.sendall(response_header.encode(FORMAT) + content.encode(FORMAT)) #--> option 1 preferable
        #self.request.sendall(response_header_1.encode(FORMAT) + response_header_2.encode(FORMAT)) this and next line option 2
        #self.request.sendall(content.encode(FORMAT)) --> could include this in the previous line

    def serve_html(self, html_path):
        print("Serve html function")
        response_header = "HTTP/1.1 200 OK\r\n" + "Content-Type: text/html\r\n"

        content = ""
        try:
            with open(html_path, "r") as html_file:
                content = html_file.read()
                print(content)
        except FileNotFoundError:
            self.send_404_response()

        self.request.sendall(response_header.encode(FORMAT) + content.encode(FORMAT))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    print("--- Server Running ---")

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
