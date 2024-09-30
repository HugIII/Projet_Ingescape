#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Image_server version 1.0
#  Created by Ingenuity i/o on 2024/09/29
#

import sys
import ingescape as igs

import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from PIL import Image
import io
import os

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        image_file = query_params.get('url', [None])[0]
        width = query_params.get('width', [None])[0]
        height  = query_params.get('height', [None])[0]

        if not image_file or not width or not height:
            self.send_response(400)
            self.end_headers()
            return

        try:
            width = int(width)
            height = int(height)

            if not os.path.isfile(image_file):
                self.send_response(404)
                self.end_headers()
                self.wfile.write('Fichier non trouvé.')
                return

            image = Image.open(image_file)

            resized_image = image.resize((width,height))

            img_io = io.BytesIO()
            resized_image.save(img_io,format='PNG')
            img_io.seek(0)

            self.send_response(200)
            self.send_header('Content-Type','image/png')
            self.send_header('Content-Length',str(len(img_io.getvalue())))
            self.end_headers()
            self.wfile.write(img_io.getvalue())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Erreur : {str(e)}".encode())

if __name__=="__main__":
    if len(sys.argv) < 4:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)

    igs.agent_set_name(sys.argv[1])
    igs.definition_set_version("1.0")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    with socketserver.TCPServer(("",PORT),Handler) as httpd:
        httpd.serve_forever()

    input()

    igs.stop()

