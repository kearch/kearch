#!/usr/bin/env python3

import connexion

from sp_gateway_server import encoder


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml', arguments={'title': 'Kearch specialist search engine gateway API'})
    app.run(port=10080)


if __name__ == '__main__':
    main()
