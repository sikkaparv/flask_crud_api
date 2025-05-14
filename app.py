from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookstore"  # Replace if your URI is different
mongo = PyMongo(app)

# Helper function to serialize MongoDB objects
def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.route('/')
def index():
    return "Welcome to the Book API!"

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    if 'title' in data and 'author' in data:
        book_id = mongo.db.books.insert_one(data).inserted_id
        new_book = mongo.db.books.find_one({'_id': book_id})
        return jsonify(serialize_doc(new_book)), 201
    else:
        return jsonify({'error': 'Title and author are required'}), 400

@app.route('/books', methods=['GET'])
def get_all_books():
    books = mongo.db.books.find()
    return jsonify([serialize_doc(book) for book in books])

@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
    if book:
        return jsonify(serialize_doc(book))
    else:
        return jsonify({'error': 'Book not found'}), 404

@app.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    result = mongo.db.books.update_one({'_id': ObjectId(book_id)}, {'$set': data})
    if result.modified_count:
        updated_book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
        return jsonify(serialize_doc(updated_book))
    else:
        return jsonify({'error': 'Book not found'}), 404

@app.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    result = mongo.db.books.delete_one({'_id': ObjectId(book_id)})
    if result.deleted_count:
        return jsonify({'message': 'Book deleted'})
    else:
        return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)