from flask import request
from flask_restful import Resource

from schemas.book import BookCreate
from services import book_service


def _build_pagination(total: int, offset: int, limit: int):
    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "has_next": (offset + limit) < total,
        "has_prev": offset > 0,
    }


class BooksListResource(Resource):

    def get(self):
        """
        Get a list of books with filtering and sorting.
        ---
        tags:
          - Books
        summary: List all books
        parameters:
          - name: offset
            in: query
            type: integer
            default: 0
          - name: limit
            in: query
            type: integer
            default: 100
          - name: status
            in: query
            type: string
          - name: author
            in: query
            type: string
          - name: sort_by
            in: query
            type: string
        responses:
          200:
            description: List of books retrieved successfully
            schema:
              type: object
              properties:
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: string
                      title:
                        type: string
                      author:
                        type: string
                      description:
                        type: string
                      status:
                        type: string
                      year:
                        type: integer
                pagination:
                  type: object
                  properties:
                    total:
                      type: integer
                    offset:
                      type: integer
                    limit:
                      type: integer
                    has_next:
                      type: boolean
                    has_prev:
                      type: boolean
        """
        offset = int(request.args.get("offset", 0))
        limit = int(request.args.get("limit", 100))
        status = request.args.get("status")
        author = request.args.get("author")
        sort_by = request.args.get("sort_by")

        if limit < 1 or limit > 1000:
            return {"message": "limit must be between 1 and 1000"}, 400
        if offset < 0:
            return {"message": "offset must be 0 or greater"}, 400

        books, total = book_service.get_books(None, offset, limit, status, author, sort_by)

        return {
            "data": [book.model_dump() for book in books],
            "pagination": _build_pagination(total, offset, limit),
        }

    def post(self):
        """
        Create a new book.
        ---
        tags:
          - Books
        summary: Create a new book
        consumes:
          - application/json
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              required: [title, author, description, status, year]
              properties:
                title:
                  type: string
                author:
                  type: string
                description:
                  type: string
                status:
                  type: string
                year:
                  type: integer
        responses:
          201:
            description: Book created successfully
            schema:
              type: object
              properties:
                id:
                  type: string
                title:
                  type: string
                author:
                  type: string
                description:
                  type: string
                status:
                  type: string
                  enum: ["available", "issued"]
                year:
                  type: integer
          400:
            description: Invalid request body
            schema:
              type: object
              properties:
                message:
                  type: string
        """
        payload = request.get_json(force=True, silent=True)
        if payload is None:
            return {"message": "Request body must be valid JSON"}, 400

        try:
            book_data = BookCreate.model_validate(payload)
        except Exception as exc:
            return {"message": str(exc)}, 400

        book = book_service.create_book(None, book_data)
        return book.model_dump(), 201


class BookResource(Resource):

    def get(self, book_id: str):
        """
        Get a book by ID.
        ---
        tags:
          - Books
        summary: Get a book by ID
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          200:
            description: Book retrieved successfully
            schema:
              type: object
              properties:
                id:
                  type: string
                title:
                  type: string
                author:
                  type: string
                description:
                  type: string
                status:
                  type: string
                  enum: ["available", "issued"]
                year:
                  type: integer
          404:
            description: Book not found
            schema:
              type: object
              properties:
                message:
                  type: string
        """
        book = book_service.get_book(None, book_id)
        if not book:
            return {"message": "Book not found"}, 404
        return book.model_dump()

    def delete(self, book_id: str):
        """
        Delete a book by ID.
        ---
        tags:
          - Books
        summary: Delete a book
        parameters:
          - name: book_id
            in: path
            type: string
            required: true
        responses:
          204:
            description: Book deleted successfully
          404:
            description: Book not found
            schema:
              type: object
              properties:
                message:
                  type: string
        """
        deleted = book_service.delete_book(None, book_id)
        if not deleted:
            return {"message": "Book not found"}, 404
        return None, 204