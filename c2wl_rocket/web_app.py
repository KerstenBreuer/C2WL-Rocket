from flask import Flask


class Config(object):
    def __init__(self, web_server_host="0.0.0.0", web_server_port=5000):
        self.WEB_SERVER_HOST = web_server_host
        self.WEB_SERVER_PORT = web_server_port


def create_app(web_server_host, web_server_port):
    app = Flask(__name__)
    config = Config(
        web_server_host=web_server_host,
        web_server_port=web_server_port
    )
    app.config.from_object(config)
    return app
