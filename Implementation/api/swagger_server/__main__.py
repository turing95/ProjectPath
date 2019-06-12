#!/usr/bin/env python3

import connexion

from swagger_server import encoder

from flask import send_from_directory


import os

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')

    @app.app.route('/images/<path:filename>')
    def serve_path_images_as_static(filename):
        print(os.path.realpath('./images/' + filename))

        return send_from_directory('../images/', filename)

    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Tourist app API'})
    app.run(port=5000)


if __name__ == '__main__':
    main()
