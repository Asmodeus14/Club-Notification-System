from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)

# Enable CORS securely (Allow only specific origins)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ----------------- Error Handling -----------------

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Page Not Found"}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Internal Server Error"}), 500

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method Not Allowed"}), 405

# ----------------- Database Utility Functions -----------------
def get_db_connection(name:str):
    conn = sqlite3.connect(f'./Data/{name}.db')  # SQLite Database
    conn.row_factory = sqlite3.Row  # To access columns by name
    return conn

def init_db_user():
    conn = get_db_connection(name='users')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            position TEXT NOT NULL,
            course TEXT NOT NULL,
            club TEXT NOT NULL,
            name Text Not NULL
        )
    ''')
    conn.commit()
    conn.close()
    
def init_admin_db():
    conn = get_db_connection(name='admin')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            position TEXT NOT NULL
        )
        ''')
    conn.execute("INSERT INTO admin (user_id, email, password, position) VALUES ('Admin', 'Singhabhay3145@gmail.com', ?, 'Admin')", (generate_password_hash('admin12345', salt_length=5),))
    conn.commit()
    conn.close()

# ----------------- API Routes -----------------

@app.route('/api/login', methods=['POST'])
def login():
    try:
        user_id = request.form.get('ID')
        password = request.form.get('password')

        # Validate input
        if not user_id or not password:
            return jsonify({"error": "Missing required fields"}), 400

        # Check database for user
        conn = get_db_connection(name='users')
        user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
        conn.close()
        # Check database for admin
        conn = get_db_connection(name='admin')
        admin = conn.execute('SELECT * FROM admin WHERE user_id = ?', (user_id,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            logging.info(f"User {user_id} logged in successfully.")
            return jsonify({"message": "Login successful", "user_id": user_id, "name": user['name'], "position": user['position'], "course": user['course'], "club": user['club']}), 200
        elif admin and check_password_hash(admin['password'], password):
            logging.info(f"Admin logged in successfully.")
            return jsonify({"message": "Login successful", "user_id": user_id, "position": admin['position']}), 200
        else:
            logging.warning(f"Invalid login attempt for user: {user_id}")
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        logging.error(f"Login error: {str(e)}")
        return jsonify({"error": "Something went wrong"}), 500


@app.route('/api/register', methods=['POST'])
def register():
    try:
        user_id = request.form.get('id')
        email = request.form.get('email')
        password = request.form.get('password')
        position = request.form.get('position')
        course=request.form.get('course')
        club=request.form.get('club')
        name=request.form.get('name')

        # Validate input
        if not user_id or not email or not password or not position:
            return jsonify({"error": "Missing required fields"}), 400

        # Check if user already exists
        conn = get_db_connection(name='users')
        user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
        conn.close()
        if user:
            logging.warning(f"User {user_id} already exists.")
            return jsonify({"error": "User already exists"}), 400

        # Hash password securely
        hashed_password = generate_password_hash(password,salt_length=5)

        # Save user in the database
        conn = get_db_connection(name='users')
        conn.execute('INSERT INTO users (user_id, email, password, position, course, club, name) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (user_id, email, hashed_password, position, course, club, name))
        conn.commit()
        conn.close()

        logging.info(f"New user registered with Id: {user_id} Name:{name}")
        return jsonify({'message': 'Registration successful', 'user_id': user_id})

    except Exception as e:
        logging.error(f"Registration error: {str(e)}")
        return jsonify({"error": "Something went wrong"}), 500


@app.route('/api/forgot', methods=['POST'])
def forgot_password():
    try:
        user_id = request.form.get('id')

        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
        

        # Log password reset request
        logging.info(f"User {user_id} requested password reset.")
        return jsonify({'message': 'Password reset request received', "user_id": user_id})

    except Exception as e:
        logging.error(f"Forgot Password error: {str(e)}")
        return jsonify({"error": "Something went wrong"}), 500


# ----------------- Initialize Database -----------------
init_db_user()
init_admin_db()

# ----------------- Run the Flask App -----------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
