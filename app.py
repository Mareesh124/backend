from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import certifi

# Load .env variables
load_dotenv()

app = Flask(__name__)

# Enable CORS for your frontend
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URL"), tlsCAFile=certifi.where())
db = client["user_database"]
users_collection = db["Boutique_collection"]

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask backend!"})

# GET endpoint
@app.route('/api/data', methods=['GET'])
def get_data():
    users = list(users_collection.find({}, {"_id": 0}))
    return jsonify(users), 200

# POST endpoint
@app.route('/api/data', methods=['POST', 'OPTIONS'])
def create_data():
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Insert into MongoDB
        users_collection.insert_one(data)

        # Always return safe JSON (avoid returning ObjectId)
        return jsonify({"message": "Data received successfully!"}), 201
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)