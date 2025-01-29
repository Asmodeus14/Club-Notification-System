from flask import Flask, request, jsonify
from flask_cors import CORS
import  Function

app = Flask(__name__)
CORS(app)

# Error handeling
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Page Not Found"}), 404
@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Internal Server Error"}), 500
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method Not Allowed"}), 405




# Routes

@app.route('/api/login', methods=['POST'])
def handle_form():
    if request.method == 'POST':
        
        user_id = request.form.get('ID')  
        password = request.form.get('password') 
        password = Function.hashing(password)
        return jsonify({'user_id': user_id, 'password': password})  # Send JSON response
        
    return jsonify({"error": "Method Not Allowed"}), 405

@app.route('/api/register', methods=['POST'])
def sign_in():
    if request.method == 'POST':
        data=request.form.get('password')
        
        return jsonify({'message': 'Sign Up Success',"Data":data})  # Send JSON response
    
    return jsonify({"error": "Method Not Allowed"}), 405



@app.route('/api/forgot', methods=['POST'])
def forget():
    if request.method == 'POST':
        data=request.form.get('id')
        
        return jsonify({'message': 'Forget Password',"Data":data})
    
    return jsonify({"error": "Method Not Allowed"}), 405




if __name__ == '__main__':
    app.run(debug=True, port=5000)
