# Books API with Authentication

This is a FastAPI application for managing books with JWT-based authentication.

## Features

- User registration and login
- JWT access and refresh tokens
- Protected book CRUD operations
- MongoDB database

## Authentication Endpoints

### Register a new user
```
POST /auth/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

### Login
```
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=testuser&password=password123
```

Response:
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### Refresh access token
```
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ..."
}
```

## Book Endpoints (Protected)

All book endpoints require authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Get books
```
GET /books/?offset=0&limit=100&status=available&author=Author&sort_by=title
```

### Get book by ID
```
GET /books/{book_id}
```

### Create book
```
POST /books/
Content-Type: application/json

{
  "title": "Book Title",
  "author": "Author Name",
  "description": "Book description",
  "status": "available",
  "year": 2023
}
```

### Delete book
```
DELETE /books/{book_id}
```

## Running the Application

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start MongoDB (using Docker):
```bash
docker-compose up -d
```

3. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## Testing

Run tests:
```bash
pytest
```