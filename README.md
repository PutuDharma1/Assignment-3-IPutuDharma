# 📚 Book Library API

A simple RESTful API built using **Flask** that allows users to manage a collection of books.
This API supports basic CRUD operations including viewing all books, retrieving a single book, adding a new book, updating existing book data, and deleting a book.

This project is created as part of **Assignment 3 - System Integration** .


## Project Description

The Book Library API uses a simple in-memory Python list to store book records.
Each book contains:

* `id`
* `title`
* `author`
* `year`
* `available`

The API provides endpoints to manipulate this dataset. No database is required.


# API Endpoints

### **1. GET /books**

Retrieve all books.

**Response Example:**

json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "title": "Marmut Merah Jambu",
      "author": "Raditya Dika",
      "year": 2010,
      "available": true
    }
  ]
}



### **2. GET /books/<id>**

Retrieve a specific book by ID.

**Example:**


GET /books/1


**Response:**

json
{
  "status": "success",
  "data": {
    "id": 1,
    "title": "Marmut Merah Jambu",
    "author": "Raditya Dika",
    "year": 2010,
    "available": true
  }
}



### **3. POST /books**

Add a new book.

**Request Body:**

json
{
  "title": "Laskar Pelangi",
  "author": "Andrea Hirata",
  "year": 2005
}



### **4. PUT /books/<id>**

Update an existing book.

**Request Body Example:**

json
{
  "title": "Laskar Pelangi (Revised Edition)",
  "available": false
}



### **5. DELETE /books/<id>**

Delete a book by ID.

**Example:**


DELETE /books/2



# Setup Instructions

### **1. Clone the repository**


git clone https://github.com/PutuDharma1/Assignment-3-IPutuDharma.git
cd Assignment-3-IPutuDharma


### **2. Install dependencies**


pip install flask


### **3. Run the Flask server**


python app.py


The API will run at:


http://127.0.0.1:5000



# Example API Calls (cURL)

### **GET all books**


curl -X GET http://127.0.0.1:5000/books



### **GET book by ID**


curl -X GET http://127.0.0.1:5000/books/1



### **POST – Add a new book**


curl -X POST http://127.0.0.1:5000/books \
-H "Content-Type: application/json" \
-d "{\"title\":\"Laskar Pelangi\",\"author\":\"Andrea Hirata\",\"year\":2005}"



### **PUT – Update book**


curl -X PUT http://127.0.0.1:5000/books/1 \
-H "Content-Type: application/json" \
-d "{\"title\":\"Updated Title\",\"available\":false}"



### **DELETE – Remove a book**


curl -X DELETE http://127.0.0.1:5000/books/1

