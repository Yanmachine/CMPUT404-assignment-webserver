#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Ian Harding
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
    ROOT = "./www" #root of server

    def handle(self):
        self.data = self.request.recv(1024).strip()

        #print(f"DATA --> {self.data}\n\n\n")
        request_input = self.data.decode(FORMAT).split('\n')
        #print(f"REQUEST INPUT --> {request_input}\n\n\n")
        request_line = request_input[0].split()
        #print(f"REQUEST LINE --> {request_line}\n\n\n")
        method = request_line[0]
        path = request_line[1]
        #print(f"METHOD --> {method}\n\n\n")
        print(f"PATH --> {path}\n\n\n")
        

        if method == "GET":

            if not os.path.exists("./www" + path):
                self.send_404_response()

            absolute_path = os.path.abspath(os.path.join(self.ROOT, path.strip("/"))) #finds the absolute path after joining root with requested path
            #absolute path removes unnecesary /../v
            if not absolute_path.startswith(os.path.abspath(self.ROOT)): #so if directory is after /www, request is ok, but if it is before, error
                self.send_404_response()

            end_of_path = os.path.basename(absolute_path)
            print(f"ABSOLUTE PATH ========= {absolute_path}")
            print(f" END OF PATH ========= {end_of_path}")

                #css request
            if end_of_path.endswith(".css"):
                self.serve_css(absolute_path)
            
            #html request
            elif end_of_path.endswith(".html"): 
                self.serve_html(absolute_path)

            #if ends with a /, then serve .html
            #if not ends with a /, then redirect

            elif path.endswith("/"):
                print("Endswith ---> ")
                print(absolute_path + "index.html")
                self.serve_html(absolute_path + "/index.html")
            else:
                print(end_of_path)
                self.send_301_redirect("/" + end_of_path + "/")
            

        #     elif path == "/" or path == "/www/":
        #         self.serve_html("./www/index.html")
        #     elif path == "/deep/":
        #         self.serve_html("./www/deep/index.html")

        #     elif path == "/deep":
        #         self.send_301_redirect("/deep/")
        #   #  else:
           #     print("THIS SHOULD ONLY RUN ON ON 404 RESPONSE")
            #    self.send_404_response()

        else:
            self.send_405_response()

               

    
    def send_200_response(self, content_type, content):
        response_header = "HTTP/1.1 200 OK\r\n"

        if type != None:
            response_header += content_type

        if content != None:
            self.request.sendall(response_header.encode(FORMAT) + content.encode(FORMAT))
        else:
            self.request.sendall(response_header.encode(FORMAT))


    def send_301_redirect(self, path):
        response_header = "HTTP/1.1 301 Moved Permanently\r\n" 
        response_header += "Location: " + path + "\r\n\r\n"
        
        self.request.sendall(response_header.encode(FORMAT))
    
    def send_403_response(self):
        response_header = "HTTP/1.1 403 Forbidden\r\n\r\n"
        message = "Forbidden"

        self.request.sendall(response_header.encode(FORMAT) + message.encode(FORMAT))

    def send_404_response(self):
        response_header = "HTTP/1.1 404 Not Found\r\n\r\n"
        message = "Not Found"

        self.request.sendall(response_header.encode(FORMAT) + message.encode(FORMAT))

    def send_405_response(self):
        response_header = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
        message = "Method Not Allowed"

        self.request.sendall(response_header.encode(FORMAT) + message.encode(FORMAT))

    def send_500_response(self):
        response_header = "HTTP/1.1 500 Internal Server Error\r\n\r\n"
        message = "Internal Server Error"

        self.request.sendall(response_header.encode(FORMAT) + message.encode(FORMAT))



    def serve_css(self, css_path):
        content = ""

        try:
            with open(css_path, "r") as css_file:
                content = css_file.read()
        except FileNotFoundError:
            self.send_404_response()

        self.send_200_response("Content-Type: text/css\r\n", content)



    def serve_html(self, html_path):
        content = ""

        try:
            with open(html_path, "r") as html_file:
                content = html_file.read()
        except FileNotFoundError:
            self.send_404_response()

        self.send_200_response("Content-Type: text/html\r\n", content)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    print("--- Server Running ---")

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
