import pytest
from flask import Flask as _Flask


class Flask(_Flask):
    testing = True
    secret_key = __name__

    def make_response(self, rv):
        if rv is None:
            rv = ""

        return super().make_response(rv)


@pytest.fixture
def app():
    app = Flask(__name__)
    return app
