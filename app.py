from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data storage (since there is no database)
items = [
    {"id": 1, "name": "Apple"},
    {"id": 2, "name": "Banana"}
]

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Simple Flask API!"})

@app.route('/api/items', methods=['GET'])
def get_items():
    """Retrieve all items"""
    return jsonify({"items": items})

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Retrieve a single item by ID"""
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

@app.route('/api/items', methods=['POST'])
def add_item():
    """Add a new item"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({"error": "Bad Request, 'name' is required"}), 400
        
    new_item = {
        "id": items[-1]['id'] + 1 if items else 1,
        "name": data['name']
    }
    items.append(new_item)
    
    return jsonify({"message": "Item created successfully", "item": new_item}), 201

if __name__ == '__main__':      
    app.run(host='0.0.0.0', port=5000)
