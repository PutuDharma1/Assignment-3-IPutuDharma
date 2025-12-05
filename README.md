# 📚 Book Library API

A simple RESTful API built using **Flask** that allows users to manage a collection of books.
This API supports basic CRUD operations including viewing all books, retrieving a single book, adding a new book, updating existing book data, and deleting a book.

This project is created as part of **Assignment 3** and **Assignment 4**.

***

## Project Description

The Book Library API uses a simple in-memory Python list to store book records.

Each book contains:

* `id`
* `title`
* `author`
* `year`
* `available`
* `owner_username` (New field added for Authorization)

### Authentication and Authorization (Assignment 4)

This API is secured using **JSON Web Tokens (JWT)** for Authentication and **Resource Ownership Check** for Authorization.

* **Technology Used:** `Flask-JWT-Extended` for token management and `Werkzeug` for secure password hashing.
* **User Persistence:** Registered user credentials (username and hashed password) are stored persistently in the file `users.json`, ensuring user data is retained across application restarts.
* **Authorization Rule:** All book manipulation endpoints (`POST`, `PUT`, `DELETE`) require a valid JWT. The `PUT /books/<id>` and `DELETE /books/<id>` endpoints are protected by an **ownership check**, meaning a user can only modify or delete a book if their authenticated username matches the book's `owner_username`.

***

# API Endpoints

### **Authentication Endpoints**

| Method | Endpoint | Description | Requires Auth |
| :--- | :--- | :--- | :--- |
| **POST** | `/register` | Register a new user with username and password. | No |
| **POST** | `/login` | Log in and receive a JWT access token. | No |

### **Secured Book Endpoints**

Semua endpoint di bawah ini memerlukan header `Authorization: Bearer <TOKEN>`.

1. GET /books

Retrieve all books.

**Response Example:**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "title": "Marmut Merah Jambu",
      "author": "Raditya Dika",
      "year": 2010,
      "available": true,
      "owner_username": "initial_user"
    }
  ]
}

2. GET /books/<id>

Retrieve a specific book by ID.

Example:

GET /books/1

Response:
{
  "status": "success",
  "data": {
    "id": 1,
    "title": "Marmut Merah Jambu",
    "author": "Raditya Dika",
    "year": 2010,
    "available": true,
    "owner_username": "initial_user"
  }
}

3. POST /books
Add a new book. The authenticated user will be automatically set as the owner_username.

Request Body:
{
  "title": "Laskar Pelangi",
  "author": "Andrea Hirata",
  "year": 2005
}

4. PUT /books/<id>
Update an existing book. Requires Authorization (must be the owner).

Request Body Example:
{
  "title": "Laskar Pelangi (Revised Edition)",
  "available": false
}

5. DELETE /books/<id>
Delete a book by ID. Requires Authorization (must be the owner).

Example:

DELETE /books/2

Setup Instructions
1. Clone the repository
git clone https://github.com/PutuDharma1/Assignment-3-IPutuDharma.git](https://github.com/PutuDharma1/Assignment-3-IPutuDharma.git)
cd Assignment-3-IPutuDharma

2. Install dependencies (Updated for Assignment 4)
pip install flask flask-jwt-extended werkzeug

3. Run the Flask server
python app.py

The API will run at:
http://127.0.0.1:5000

Example API Calls
1. POST – Register a new user
$body = @{ username = "testuser"; password = "password123" } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:5000/register](http://127.0.0.1:5000/register) -Method Post -Body $body -ContentType "application/json"

2. POST – Log in and get the JWT
$body = @{
    username = "testuser"
    password = "password123"
} | ConvertTo-Json

$login_response = Invoke-RestMethod -Uri http://127.0.0.1:5000/login](http://127.0.0.1:5000/login) -Method Post -Body $body -ContentType "application/json"
$TOKEN = $login_response.access_token

3. GET – Retrieve all books (Requires Token)
$headers = @{"Authorization" = "Bearer " + $TOKEN}
Invoke-RestMethod -Uri http://127.0.0.1:5000/books](http://127.0.0.1:5000/books) -Method Get -Headers $headers

4. POST – Add a new book (The owner is set automatically)
$new_book_body = @{
    title  = "Buku JWT Baru"
    author = "Penulis Aman"
    year   = 2024
} | ConvertTo-Json

$headers = @{"Authorization" = "Bearer " + $TOKEN}
Invoke-RestMethod -Uri http://127.0.0.1:5000/books](http://127.0.0.1:5000/books) -Method Post -Body $new_book_body -ContentType "application/json" -Headers $headers

5. DELETE – Remove a book (Requires Ownership)
$headers = @{"Authorization" = "Bearer " + $TOKEN}
Invoke-RestMethod -Uri [http://127.0.0.1:5000/books/3](http://127.0.0.1:5000/books/3) -Method Delete -Headers $headers