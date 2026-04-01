# Library API

A FastAPI application for managing a library's book collection with PostgreSQL database.

## Features

- CRUD operations for books
- Limit-Offset pagination for GET /books endpoint
- PostgreSQL database with SQLAlchemy ORM
- Docker containerization
- Unit tests with pytest

## Setup

### Using Docker (Recommended)

1. Make sure Docker and Docker Compose are installed
2. Run the application:
   ```bash
   docker-compose up --build
   ```
3. The API will be available at http://localhost:8000

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up PostgreSQL database (or use the Docker container)

3. Set environment variable:
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost:5432/library_db"
   ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

- `GET /books/` - Get all books with optional pagination, filtering, and sorting
  - Query parameters:
    - `skip`: Number of books to skip (default: 0)
    - `limit`: Maximum number of books to return (default: 100, max: 1000)
    - `status`: Filter by book status (available/issued)
    - `author`: Filter by author
    - `sort_by`: Sort by title or year

- `GET /books/{book_id}` - Get a specific book by ID

- `POST /books/` - Create a new book

- `DELETE /books/{book_id}` - Delete a book by ID

## Running Tests

```bash
pytest
```

## Project Structure

```
api-main/
├── api/
│   └── books.py          # API routes
├── models/
│   └── book_model.py     # SQLAlchemy model
├── repository/
│   └── book_repository.py # Data access layer
├── schemas/
│   └── book.py           # Pydantic schemas
├── services/
│   └── book_service.py   # Business logic
├── tests/
│   ├── conftest.py       # Test configuration
│   └── test_books.py     # Unit tests
├── database.py           # Database configuration
├── main.py               # FastAPI app
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker image
├── docker-compose.yml    # Docker services
└── README.md             # This file
```