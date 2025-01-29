from flask import Flask, request, jsonify
from flask_cors import CORS
import  Function

app = Flask(__name__)
CORS(app)

@app.route('/api/login', methods=['POST'])
def handle_form():
    if request.method == 'POST':
        # Extract form data sent from the frontend
        user_id = request.form.get('ID')  # Retrieves the value of the input with id="ID"
        password = request.form.get('password') # Retrieves the value of the input with id="password"
        password = Function.hashing(password)
        return jsonify({'user_id': user_id, 'password': password})  # Send JSON response
        
    return jsonify({"error": "Method Not Allowed"}), 405

if __name__ == '__main__':
    app.run(debug=True, port=5000)
