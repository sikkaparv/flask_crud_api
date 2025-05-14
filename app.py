import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Get MongoDB URI from environment variables
app.config["MONGO_URI"] = "mongodb+srv://parvsikka36:Parvpilot6@cluster0.yhzugep.mongodb.net/bookstore?retryWrites=true&w=majority&appName=Cluster0"

# Initialize MongoDB connection
mongo = PyMongo(app)
books_collection = mongo.db.books

# Helper to convert ObjectId to string
def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.route('/')
def index():
    return "Welcome to the Book API!"

# Create a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Invalid or missing JSON'}), 400

    # Basic required fields
    if 'title' not in data or 'author' not in data:
        return jsonify({'error': 'Title and author are required'}), 400

    # Insert book
    book_id = books_collection.insert_one(data).inserted_id
    new_book = books_collection.find_one({'_id': book_id})
    return jsonify(serialize_doc(new_book)), 201

# Get all books
@app.route('/books', methods=['GET'])
def get_all_books():
    books = books_collection.find()
    return jsonify([serialize_doc(book) for book in books]), 200

# Get a single book by ID
@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    try:
        book = books_collection.find_one({'_id': ObjectId(book_id)})
        if book:
            return jsonify(serialize_doc(book)), 200
        else:
            return jsonify({'error': 'Book not found'}), 404
    except Exception:
        return jsonify({'error': 'Invalid book ID'}), 400

# Delete a book by ID
@app.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        result = books_collection.delete_one({'_id': ObjectId(book_id)})
        if result.deleted_count:
            return jsonify({'message': 'Book deleted'}), 200
        else:
            return jsonify({'error': 'Book not found'}), 404
    except Exception:
        return jsonify({'error': 'Invalid book ID'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5009)
