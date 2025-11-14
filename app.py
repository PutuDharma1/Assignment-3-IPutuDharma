from flask import Flask, jsonify, request, abort

app = Flask(__name__)

books = [
    {
        "id": 1,
        "title": "Marmut Merah Jambu",
        "author": "Raditya Dika",
        "year": 2010,
        "available": True
    },
    {
        "id": 2,
        "title": "Ngenest: Ngetawain Hidup A la Ernest",
        "author": "Ernest Prakasa",
        "year": 2013,
        "available": True
    }
]

def get_next_id():
    if not books:
        return 1
    return max(book["id"] for book in books) + 1

# GET /books
@app.route("/books", methods=["GET"])
def get_books():
    return jsonify({
        "status": "success",
        "data": books
    }), 200


# GET /books/<id> 
@app.route("/books/<int:book_id>", methods=["GET"])
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
def create_book():
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
        "available": data.get("available", True) 
    }

    books.append(new_book)

    return jsonify({
        "status": "success",
        "message": "Book created successfully",
        "data": new_book
    }), 201


# PUT /books/<id>
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
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
def delete_book(book_id):
    global books
    book = next((b for b in books if b["id"] == book_id), None)
    if book is None:
        return jsonify({
            "status": "error",
            "message": "Book not found"
        }), 404

    books = [b for b in books if b["id"] != book_id]

    return jsonify({
        "status": "success",
        "message": "Book deleted successfully"
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
