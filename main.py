from flask import Flask
from flask_restful import Api
from flasgger import Swagger

from api.books import BooksListResource, BookResource


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        SWAGGER={
            "title": "Library API",
            "uiversion": 3,
        },
    )

    if test_config is not None:
        app.config.update(test_config)

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Library API",
            "version": "1.0.0",
        },
        "definitions": {
            "Book": {
                "type": "object",
                "required": ["id", "title", "author", "description", "status", "year"],
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "description": {"type": "string"},
                    "status": {"type": "string", "enum": ["available", "issued"]},
                    "year": {"type": "integer"}
                }
            },
            "BookCreate": {
                "type": "object",
                "required": ["title", "author", "description", "status", "year"],
                "properties": {
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "description": {"type": "string"},
                    "status": {"type": "string", "enum": ["available", "issued"]},
                    "year": {"type": "integer"}
                }
            },
            "PaginationMeta": {
                "type": "object",
                "properties": {
                    "total": {"type": "integer"},
                    "offset": {"type": "integer"},
                    "limit": {"type": "integer"},
                    "has_next": {"type": "boolean"},
                    "has_prev": {"type": "boolean"}
                }
            },
            "BooksResponse": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/Book"}
                    },
                    "pagination": {"$ref": "#/definitions/PaginationMeta"}
                }
            },
            "Error": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                }
            }
        }
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)

    api = Api(app)
    api.add_resource(BooksListResource, "/books/")
    api.add_resource(BookResource, "/books/<string:book_id>")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
    