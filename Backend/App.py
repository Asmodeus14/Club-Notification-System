import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv
import os
from marshmallow import Schema, fields, ValidationError
import secrets
reset_token = secrets.token_urlsafe(32)

# Load environment variables
load_dotenv('API.env')

# Initialize Flask app
app = Flask(__name__)

# Configuration
class Config:
    DB_CONFIG = {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT")
    }
    CORS_ORIGINS = ["http://localhost:8080", "http://192.168.101.86:8080"]
    SECRET_KEY = os.getenv("SECRET_KEY")
    BREVO_API_KEY = os.getenv("BREVO_API_KEY")

app.config.from_object(Config)

# Enable CORS securely
CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Brevo API
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = app.config["BREVO_API_KEY"]
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

# Database Utility Functions
def get_db_connection():
    try:
        return psycopg2.connect(**app.config["DB_CONFIG"], cursor_factory=RealDictCursor)
    except psycopg2.Error as e:
        logging.error(f"Database connection error: {str(e)}")
        return None


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
            name TEXT NOT NULL,
            status TEXT DEFAULT 'Approved',
            reset_token TEXT
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

    cur.execute('''
        CREATE TABLE IF NOT EXISTS approval (
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
        CREATE TABLE IF NOT EXISTS rejected (
            id SERIAL PRIMARY KEY,
            user_id TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            position TEXT NOT NULL,
            course TEXT NOT NULL,
            club TEXT NOT NULL,
            name TEXT NOT NULL,
            status TEXT DEFAULT 'Rejected'
        )
    ''')

    # Insert admin if not exists
    cur.execute("SELECT * FROM admin WHERE user_id = 'Admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO admin (user_id, email, password, position, name) VALUES (%s, %s, %s, %s, %s)",
                    ('Admin', 'Singhabhay3145@gmail.com', generate_password_hash('admin12345', salt_length=5), 'Admin', 'Admin'))

    conn.commit()
    cur.close()
    conn.close()

# Initialize Database
init_db()

# Helper Functions
def error_response(message, status_code):
    return jsonify({"error": message}), status_code

def send_email(to_email, subject, content):
    sender = {"name": "SRMU Club Notices", "email": "srmu.clubnotices@gmail.com"}
    to = [{"email": to_email, "name": to_email}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        sender=sender, to=to, subject=subject, html_content=content
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        logging.info(f"Email sent to {to_email}")
    except ApiException as e:
        logging.error(f"Brevo API error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error sending email: {str(e)}")

# Schemas for Input Validation
class LoginSchema(Schema):
    user_id = fields.Str(required=True)
    password = fields.Str(required=True)

class RegisterSchema(Schema):
    user_id = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    position = fields.Str(required=True)
    course = fields.Str(required=True)
    club = fields.Str(required=True)
    name = fields.Str(required=True)

# API Routes
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = LoginSchema().load(request.form)
    except ValidationError as err:
        return error_response(err.messages, 400)

    user_id = data['user_id']
    password = data['password']

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
        return error_response("Invalid credentials", 401)

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = RegisterSchema().load(request.form)
    except ValidationError as err:
        return error_response(err.messages, 400)
    print(data)
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE user_id = %s", (data['user_id'],))
    if cur.fetchone():
        return error_response("User already exists", 400)

    hashed_password = generate_password_hash(data['password'], salt_length=5)
    cur.execute("INSERT INTO approval (user_id, email, password, position, course, club, name) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (data['user_id'], data['email'], hashed_password, data['position'].lower(), data['course'], data['club'], data['name']))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({'message': 'Registration sent for approval', 'user_id': data['user_id']}), 200

@app.route('/api/forgot', methods=['POST'])
def forgot_password():
    email= request.form.get('email')
    user_id= request.form.get('user_id')
    
    print(email, user_id)

    if not email:
        return error_response("Email is required", 400)

    conn = get_db_connection()
    if not conn:
        return error_response("Database connection failed", 500)

    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    print(user['email'],user['user_id'])

    if not user:
        return error_response("User not found", 404)
    if user['email'] != email:
        return error_response("Email does not match", 400)
    # Generate a secure reset token
    reset_token = secrets.token_urlsafe(32)
    
    cur.execute("UPDATE users SET reset_token = %s WHERE email = %s", (reset_token, user['email']))
    conn.commit()
    cur.close()
    conn.close()

    reset_link = f"http://localhost:8080/reset-password?token={reset_token}"
    send_email(email, "Password Reset", f"Click the link to reset your password: <a href='{reset_link}'>Reset Password</a>")

    return jsonify({"message": "Password reset email sent"}), 200

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


@app.route('/api/approvals/<string:position>-<string:club_name>', methods=['GET'])
def get_approvals(position,club_name):
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

        # Validate position
        if position not in approval_hierarchy:
            return jsonify({"error": "Invalid position"}), 400

        # Fetch approvals based on hierarchy
        if position == 'admin':
            print(0)
            cur.execute(
                "SELECT * FROM approval WHERE position = %s",
                (approval_hierarchy[position],)
            )
        else:
            cur.execute(
                "SELECT * FROM approval WHERE position = %s AND club = %s",
                (approval_hierarchy[position], club_name)
            )

        pending = cur.fetchall()

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
        ''', (approval["user_id"],
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


@app.route('/api/reject/<string:id>', methods=['POST'])
def reject_request(id):
    """
    Reject a pending approval request and move it to the rejected table.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch the approval request
    cur.execute("SELECT * FROM approval WHERE user_id = %s", (id,))
    approval = cur.fetchone()

    if approval is None:
        cur.close()
        conn.close()
        return jsonify({"error": "Approval not found"}), 404

    try:
        # Move the rejected request to the rejected table
        cur.execute('''
            INSERT INTO rejected (user_id, email, password, position, course, club, name)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        ''', (approval["user_id"],
              approval["email"],
              approval["password"],
              approval["position"],
              approval["course"],
              approval["club"],
              approval["name"]))

        # Delete from approval table after moving it to rejected
        cur.execute("DELETE FROM approval WHERE user_id = %s", (id,))

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


@app.route('/api/delete/<string:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a user from the 'users' table only if they are approved.
    """
    try:
        logging.info(f"Received request to delete user with ID: {user_id}")

        conn = get_db_connection()
        cur = conn.cursor()

        # Log the search for the user
        logging.info(f"Checking if user with ID {
                     user_id} exists in the 'users' table.")

        # Check if user exists in 'users' (approved users)
        cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cur.fetchone()

        if user:
            # Log that user was found
            logging.info(f"User with ID {
                         user_id} found. Proceeding with deletion.")

            # Delete the user
            cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            conn.commit()

            # Log successful deletion
            logging.info(f"User with ID {
                         user_id} has been successfully deleted.")
            cur.close()
            conn.close()

            return jsonify({"message": "User deleted successfully"}), 200
        else:
            # Log that the user was not found
            logging.warning(
                f"User with ID {user_id} not found or not approved.")
            cur.close()
            conn.close()

            return jsonify({"error": "User not found or not approved"}), 404
    except Exception as e:
        # Log the error in case of exception
        logging.error(f"Error deleting user with ID {user_id}: {str(e)}")
        return jsonify({"error": "Something went wrong"}), 500


# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True, port=5000)