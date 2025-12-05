from flask import Flask, jsonify, request
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "951008c8bca3eda63f6925073dfb80af72c728a16c2b8c5e"
jwt = JWTManager(app)

USER_DATA_FILE = "users.json"

def load_users():
    """Loads user data from a JSON file."""
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {} 

def save_users(users_dict):
    """Saves user data to a JSON file."""
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users_dict, f, indent=4)

users = load_users()

books = [
    {
        "id": 1,
        "title": "Marmut Merah Jambu",
        "author": "Raditya Dika",
        "year": 2010,
        "available": True,
        "owner_username": "initial_user" 
    },
    {
        "id": 2,
        "title": "Ngenest: Ngetawain Hidup A la Ernest",
        "author": "Ernest Prakasa",
        "year": 2013,
        "available": True,
        "owner_username": "initial_user" 
    }
]

def get_next_id():
    if not books:
        return 1
    return max(book["id"] for book in books) + 1

# POST /register (Add a User)
@app.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing username or password"}), 400

    if username in users:
        return jsonify({"status": "error", "message": "User already exists"}), 409

    # Hash the password
    hashed_password = generate_password_hash(password)
    users[username] = hashed_password
    save_users(users)

    return jsonify({"status": "success", "message": "User registered successfully"}), 201

# POST /login (Get JWT)
@app.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing username or password"}), 400

    if username not in users or not check_password_hash(users[username], password):
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    
    return jsonify({
        "status": "success",
        "message": "Login successful",
        "access_token": access_token
    }), 200

# GET /books
@app.route("/books", methods=["GET"])
@jwt_required() 
def get_books():
    return jsonify({
        "status": "success",
        "data": books
    }), 200


# GET /books/<id> 
@app.route("/books/<int:book_id>", methods=["GET"])
@jwt_required() 
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({
            "status": "error",
            "message": "Book not found"
        }), 404
    return jsonify({
        "status": "success",
        "data": book
    }), 200


# POST /books
@app.route("/books", methods=["POST"])
@jwt_required() 
def create_book():
    current_user = get_jwt_identity() 
    
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Request body must be JSON"
        }), 400

    data = request.get_json()

    required_fields = ["title", "author", "year"]
    for field in required_fields:
        if field not in data:
            return jsonify({
                "status": "error",
                "message": f"Missing required field: {field}"
            }), 400

    new_book = {
        "id": get_next_id(),
        "title": data["title"],
        "author": data["author"],
        "year": data["year"],
        "available": data.get("available", True),
        "owner_username": current_user # Assign the current user as the owner
    }

    books.append(new_book)

    return jsonify({
        "status": "success",
        "message": "Book created successfully",
        "data": new_book
    }), 201


# PUT /books/<id>
@app.route("/books/<int:book_id>", methods=["PUT"])
@jwt_required()
def update_book(book_id):
    current_user = get_jwt_identity() 
    
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Request body must be JSON"
        }), 400

    data = request.get_json()

    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({
            "status": "error",
            "message": "Book not found"
        }), 404

    if book["owner_username"] != current_user:
        return jsonify({
            "status": "error",
            "message": "Unauthorized: You are not the owner of this book."
        }), 403

    if "title" in data:
        book["title"] = data["title"]
    if "author" in data:
        book["author"] = data["author"]
    if "year" in data:
        book["year"] = data["year"]
    if "available" in data:
        book["available"] = data["available"]

    return jsonify({
        "status": "success",
        "message": "Book updated successfully",
        "data": book
    }), 200


# DELETE /books/<id>
@app.route("/books/<int:book_id>", methods=["DELETE"])
@jwt_required() 
def delete_book(book_id):
    global books
    current_user = get_jwt_identity()
    
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({
            "status": "error",
            "message": "Book not found"
        }), 404
        
    if book["owner_username"] != current_user:
        return jsonify({
            "status": "error",
            "message": "Unauthorized: You are not the owner of this book."
        }), 403

    books = [b for b in books if b["id"] != book_id]

    return jsonify({
        "status": "success",
        "message": "Book deleted successfully"
    }), 200

if __name__ == "__main__":
    app.run(debug=True)