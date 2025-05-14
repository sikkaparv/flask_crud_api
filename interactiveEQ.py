from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/bookstore"  # Replace if your URI is different
mongo = PyMongo(app)

# Helper function to serialize MongoDB objects
def serialize_doc(doc):
    if doc is None:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

@app.route("/",methods=["GET"])
def welcome():
    return "welcome to MyApi"

# Route to add a new book (POST)
@app.route('/books', methods=['POST'])
def add_book():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        if 'title' not in data or 'author' not in data:
            return jsonify({'error': 'Title and author are required'}), 400

        book_data = {
            'title': data['title'],
            'author': data['author'],
            'year': data.get('year'),  # Optional fields
            'isbn': data.get('isbn')
        }

        result = mongo.db.books.insert_one(book_data)
        new_book = mongo.db.books.find_one({'_id': result.inserted_id})
        return jsonify(serialize_doc(new_book)), 201  # 201 Created
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get all books (GET)
@app.route('/books', methods=['GET'])
def get_all_books():
    try:
        books = list(mongo.db.books.find())
        return jsonify([serialize_doc(book) for book in books])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get a specific book by ID (GET)
@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    try:
        book = mongo.db.books.find_one({'_id': ObjectId(book_id)})
        if book:
            return jsonify(serialize_doc(book))
        else:
            return jsonify({'error': 'Book not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Route to delete a book by ID (DELETE)
@app.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        result = mongo.db.books.delete_one({'_id': ObjectId(book_id)})
        if result.deleted_count:
            return jsonify({'message': 'Book deleted'})
        else:
            return jsonify({'error': 'Book not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5005)
