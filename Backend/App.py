from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)

# Enable CORS securely (Allow only specific origins)
CORS(app, resources={
     r"/api/*": {"origins": ["http://localhost:8080", "http://192.168.101.86:8080"]}})

# Configure Logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

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
            position TEXT NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS approval (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            position TEXT NOT NULL,
            course TEXT NOT NULL,
            club TEXT NOT NULL,
            name TEXT NOT NULL
            )'''
                )
    cur.execute('''CREATE TABLE IF NOT EXISTS rejected (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            position TEXT NOT NULL,
            course TEXT NOT NULL,
            club TEXT NOT NULL,
            name TEXT NOT NULL
            )'''
                )

    # Insert admin if not exists
    cur.execute("SELECT * FROM admin WHERE user_id = 'Admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO admin (user_id, email, password, position, name) VALUES (%s, %s, %s, %s,%s)",
                    ('Admin', 'Singhabhay3145@gmail.com', generate_password_hash('admin12345', salt_length=5), 'Admin', 'Admin'))

    conn.commit()
    cur.close()
    conn.close()


init_db()
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
        position=position.lower()

        if not user_id or not email or not password or not position:
            return jsonify({"error": "Missing required fields"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        if cur.fetchone():
            return jsonify({"error": "User already exists"}), 400

        hashed_password = generate_password_hash(password, salt_length=5)
        cur.execute("INSERT INTO approval (user_id, email, password, position, course, club, name) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (user_id, email, hashed_password, position, course, club, name))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Registration sent for approval', 'user_id': user_id})
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


@app.route('/api/get_user/<string:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch from users table
        cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cur.fetchone()

        # If user is not found in users table, check admin table
        if not user:
            cur.execute("SELECT * FROM admin WHERE user_id = %s", (user_id,))
            user = cur.fetchone()

        cur.close()
        conn.close()

        # If user exists, remove password field before returning
        if user:
            user = dict(user)  # Convert to dictionary (for pop to work)
            user.pop("password", None)
            return jsonify(user), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        logging.error(f"Error fetching user data: {str(e)}")
        return jsonify({"error": "Something went wrong"}), 500


@app.route('/api/approvals/<string:position>', methods=['GET'])
def get_approvals(position):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Normalize position for case-insensitive comparison
        position = position.lower()

        # Define the valid approval hierarchy
        approval_hierarchy = {
            'admin': 'veteran-coordinator',
            'veteran-coordinator': 'assistant-coordinator',
            'assistant-coordinator': 'student-coordinator'
        }
        print(approval_hierarchy[position])
        # Validate position
        if position not in approval_hierarchy:
            return jsonify({"error": "Invalid position"}), 400

        # Fetch approvals based on hierarchy
        cur.execute(
            "SELECT * FROM approval WHERE position = %s",
            (approval_hierarchy[position],)
        )

        pending = cur.fetchall()
        print(pending)
        # Fetch processed requests
        cur.execute("SELECT * FROM users")
        processed = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({"pending": pending, "processed": processed})

    except Exception as e:
        logging.error(f"Error fetching approvals: {str(e)}")
        return jsonify({"error": "Something went wrong"}), 500


# Changed int:id to string:user_id
@app.route('/api/approve/<string:user_id>', methods=['POST'])
def approve_request(user_id):
    """
    Approve a pending approval request and move it to the users table.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch the approval request
    cur.execute("SELECT * FROM approval WHERE user_id = %s", (user_id,))
    approval = cur.fetchone()
    

    if approval is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Approval not found"}), 404

    try:
        # Move the approved request to the users table
        cur.execute('''
            INSERT INTO users (user_id, email, password, position, course, club, name)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (   approval["user_id"],
                approval["email"],
                approval["password"],
                approval["position"],
                approval["course"],
                approval["club"],
                approval["name"]))
        # Delete from approval table after successful insertion
        cur.execute("DELETE FROM approval WHERE user_id = %s", (user_id,))

        conn.commit()

        return jsonify({"message": "User approved and moved to users table"}), 200

    except Exception as e:
        conn.rollback()  # Rollback in case of error
        logging.error(f"Error approving request: {
                      str(e)}")  # Log the real error
        return jsonify({"error": f"Failed to approve request: {str(e)}"}), 500

    finally:
        cur.close()
        conn.close()


@app.route('/api/reject/<int:id>', methods=['POST'])
def reject_request(id):
    """
    Reject a pending approval request and move it to the rejected table.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch the approval request
    cur.execute("SELECT * FROM approval WHERE user_id = %s", (str(id),))
    approval = cur.fetchone()

    if approval is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Approval not found"}), 404

    try:
        # Move the rejected request to the rejected table
        cur.execute('''
            INSERT INTO rejected (user_id, email, password, position, course, club, name)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (   approval["user_id"],
                approval["email"],
                approval["password"],
                approval["position"],
                approval["course"],
                approval["club"],
                approval["name"]))

        # Delete from approval table after moving it to rejected
        cur.execute("DELETE FROM approval WHERE user_id = %s", (str(id),))

        conn.commit()

        return jsonify({"message": "User rejected and moved to rejected table"}), 200

    except Exception as e:
        conn.rollback()  # Rollback in case of error
        logging.error(f"Error rejecting request: {str(e)}")
        return jsonify({"error": "Failed to reject request"}), 500

    finally:
        cur.close()
        conn.close()


@app.route('/api/get_all_users', methods=['GET'])
def get_all_users():
    """
    Fetches all approved and rejected users.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Fetch approved users
        cur.execute(
            "SELECT id, user_id, email, position, course, club, name, 'approved' AS status FROM users")
        approved_users = cur.fetchall()

        # Fetch rejected users
        cur.execute(
            "SELECT id, user_id, email, position, course, club, name, 'rejected' AS status FROM rejected")
        rejected_users = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({"approved": approved_users, "rejected": rejected_users}), 200
    except Exception as e:
        logging.error(f"Error fetching users: {str(e)}")
        return jsonify({"error": "Something went wrong"}), 500


@app.route('/api/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user from the 'users' table only if they are approved.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if user exists in 'users' (approved users)
        cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cur.fetchone()

        if user:
            # Delete the user
            cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            conn.commit()
            cur.close()
            conn.close()

            return jsonify({"message": "User deleted successfully"}), 200
        else:
            cur.close()
            conn.close()
            return jsonify({"error": "User not found or not approved"}), 404
    except Exception as e:
        logging.error(f"Error deleting user: {str(e)}")
        return jsonify({"error": "Something went wrong"}), 500


# ----------------- Initialize Database -----------------
init_db()

# ----------------- Run the Flask App -----------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
