from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)

# Enable CORS securely (Allow only specific origins)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:8080","http://192.168.101.86:8080"]}})

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Database connection settings
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "Abhaysingh14",
    "host": "localhost",
    "port": "5432"
}

# ----------------- Database Utility Functions -----------------
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            position TEXT NOT NULL,
            course TEXT NOT NULL,
            club TEXT NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            position TEXT NOT NULL
        )
    ''')
    
    # Insert admin if not exists
    cur.execute("SELECT * FROM admin WHERE user_id = 'Admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO admin (user_id, email, password, position) VALUES (%s, %s, %s, %s)",
                    ('Admin', 'Singhabhay3145@gmail.com', generate_password_hash('admin12345', salt_length=5), 'Admin'))
    
    conn.commit()
    cur.close()
    conn.close()

# ----------------- API Routes -----------------

@app.route('/api/login', methods=['POST'])
def login():
    try:
        user_id = request.form.get('ID')
        password = request.form.get('password')

        if not user_id or not password:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check user table
        cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        
        # Check admin table
        cur.execute("SELECT * FROM admin WHERE user_id = %s", (user_id,))
        admin = cur.fetchone()
        
        cur.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            return jsonify({"message": "Login successful", "user_id": user_id, "name": user['name'], "position": user['position'], "course": user['course'], "club": user['club']}), 200
        elif admin and check_password_hash(admin['password'], password):
            return jsonify({"message": "Login successful", "user_id": user_id, "position": admin['position']}), 200
        else:
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
        course = request.form.get('course')
        club = request.form.get('club')
        name = request.form.get('name')

        if not user_id or not email or not password or not position:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        if cur.fetchone():
            return jsonify({"error": "User already exists"}), 400

        hashed_password = generate_password_hash(password, salt_length=5)
        cur.execute("INSERT INTO users (user_id, email, password, position, course, club, name) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (user_id, email, hashed_password, position, course, club, name))
        conn.commit()
        cur.close()
        conn.close()

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
        return jsonify({'message': 'Password reset request received', "user_id": user_id})
    except Exception as e:
        logging.error(f"Forgot Password error: {str(e)}")
        return jsonify({"error": "Something went wrong"}), 500

# ----------------- Initialize Database -----------------
init_db()

# ----------------- Run the Flask App -----------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
