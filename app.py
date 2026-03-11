from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import json
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # Secret key for flashing messages

# MongoDB Atlas connection
uri = "mongodb+srv://dummy:1234@apurvadb.gl0f3.mongodb.net/"
client = MongoClient(uri)
db = client['ApurvaDB']
collection = db['users']

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('username')
    password = request.form.get('Password')
    collection.insert_one({"username": name, "password": password})
    flash("User registered successfully!")
    return redirect(url_for('success'))

@app.route('/todo', methods=['GET'])
def todo():
    return render_template('todo.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/submittodoitem', methods=['POST'])
def submittodoitem():
    item_name = request.form.get('itemName')
    item_description = request.form.get('itemDescription')
    todo_collection = db['todoitems']
    todo_collection.insert_one({"itemName": item_name, "itemDescription": item_description})
    return jsonify({"message": "Todo item added successfully"}), 201

@app.route('/view', methods=['GET'])
def view():
    try:
        users = list(collection.find({}, {"_id": 0}))  # Exclude the _id field
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5500)
