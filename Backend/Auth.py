"""
====================================================
           Campus Connect Club Management System
====================================================

Created By: Team Heckers
Creation Date: InProgress
Last Updated: InProgress

Project: Campus Connect - College Club Coordination Platform
Version: 1.0.0
Status: Local

Team Members:
- Abhay Singh (Backend Architect + Frontend)
- Pratham Mohan (Frontend)
- Aayushman Saxsena (Database Engineer)
- Tarun Yadav (Dataflow Configurer)

Description:
A comprehensive platform for managing college club activities,
member coordination, and event notifications. Developed for
SRMU to streamline student organization operations.

Repository: [https://github.com/Asmodeus14/Club-Notification-System]
Contact: Singhabhay3145@gmail.com

Dependencies:
- Flask 3.0.2
- PostgreSQL 15
- Redis 7.2
- Socket.IO 5.3.3

License: MIT License
Copyright (c) 2024 Team Heckers

Configuration Requirements:
- PostgreSQL database
- Redis server
- Brevo API key
- Environment variables setup (API.env)

====================================================
            🚀 Powered by Flask & Vue.js 🛠️
====================================================
"""


from psycopg2 import pool
from flask import Flask, request, jsonify, g, session,render_template,abort
from flask_cors import CORS
import logging
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv
import os
from marshmallow import Schema, fields, ValidationError
import secrets
from Docker import send_single_email, send_notification
from Email_Limit import check_brevo_email_quota, add_to_email_queue
from datetime import datetime, timedelta
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_socketio import SocketIO, emit


reset_token = secrets.token_urlsafe(32)

# Load environment variables
load_dotenv('API.env')


# Configuration
class Config:
    DB_CONFIG = {
        # "dbname": os.getenv("DB_NAME"),
        # "user": os.getenv("DB_USER"),
        # "password": os.getenv("DB_PASSWORD"),
        # "host": os.getenv("DB_HOST"),
        # "port": os.getenv("DB_PORT"),
        #Neon Database
        "dbname": os.getenv("PGDATABASE"),
        "user": os.getenv("PGUSER"),
        "password": os.getenv("PGPASSWORD"),
        "host": os.getenv("PGHOST"),
        
    }
    CORS_ORIGINS = ["*"]
    SECRET_KEY = os.getenv("SECRET_KEY")
    BREVO_API_KEY = os.getenv("BREVO_API_KEY")
    PERMANENT_SESSION_LIFETIME = timedelta(
        hours=1)  # Set session lifetime to 1 hour


app = Flask(__name__,template_folder=os.path.join(os.getcwd(), 'template'))
app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origins="*",message_queue="redis://localhost:6379")


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379/1",
    default_limits=["200 per day", "50 per hour"]
)


Email_limit_API = app.config["BREVO_API_KEY"]

# Enable CORS securely
CORS(app, resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}})

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Error Handeling

@app.errorhandler(500)
def not_found(error):
    return render_template("500.html"), 500
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')
@app.errorhandler(401)
def no_user_found():
    return render_template('401.html')


# Add after app configuration:
connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=50,
    connect_timeout=10,
    **app.config["DB_CONFIG"]
)


def get_db_connection():
    return connection_pool.getconn()

# Add teardown to return connections


@app.teardown_request
def close_db_connection(exception=None):
    conn = getattr(g, '_database_connection', None)
    if conn is not None:
        connection_pool.putconn(conn)

@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    logging.error(f"404 Not Found: The requested API endpoint '{path}' does not exist")
    abort(404)


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
            reset_token TEXT,
            reset_token_expiry TIMESTAMP
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
    cur.execute('''
    CREATE TABLE IF NOT EXISTS student_club_subscriptions (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        student_id VARCHAR(255),
        email VARCHAR(255),
        year VARCHAR(50),
        club VARCHAR(255),
        notification_consent BOOLEAN,
        unsubscribe_token VARCHAR(255)
    )
    ''')
    cur.execute( '''
        CREATE TABLE IF NOT EXISTS club_messages (
            id SERIAL PRIMARY KEY,
            club_name VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
def delete_old_messages():
    try:
        conn=get_db_connection()
        cursor = conn.cursor()

        # Define the delete query (delete messages older than 7 days)
        delete_query = """
            DELETE FROM club_messages
            WHERE sent_at < %s;
        """

        # Calculate the date 7 days ago
        seven_days_ago = datetime.now() - timedelta(days=7)
        cursor.execute(delete_query, (seven_days_ago,))
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()


    except Exception as e:
        logging.info(f"Error deleting old messages: {e}")


def clear_rejected_table_if_full():
    """
    Clears the oldest entries from the `rejected` table if the number of rows exceeds 50.
    """
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Get the current count of rows in the `rejected` table
        cur.execute("SELECT COUNT(*) FROM rejected")
        count = cur.fetchone()['count']

        # If the count exceeds 50, delete the oldest entries
        if count > 50:
            # Delete the oldest entries, keeping only the latest 50
            cur.execute("""
                DELETE FROM rejected
                WHERE id IN (
                    SELECT id FROM rejected
                    ORDER BY id ASC
                    LIMIT (SELECT COUNT(*) - 50 FROM rejected)
                )
            """)
            conn.commit()
            logging.info(
                f"Cleared {count - 50} oldest entries from the `rejected` table.")

    except Exception as e:
        logging.error(f"Error clearing `rejected` table: {str(e)}")
        if conn:
            conn.rollback()

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def error_response(message, status_code):
    return jsonify({"error": message}), status_code



def send_emails_apart_from_admin(message, position, emails, club):
    """
    Send professional emails from a club representative to a list of users.
    """
    try:
        subject = f"Important Announcement from {club}"
        content = f"""
        <html>
            <body>
                <p>Dear Valued Member,</p>
                <p>We hope this message finds you well. Please be informed of the following update from {club}:</p>
                <p style="margin-left:20px;">{message}</p>
                <p>Sincerely,<br>{position}<br>{club}</p>
                <p>Thank you for your continued support.</p>
            </body>
        </html>
        """
        add_to_email_queue(emails, subject, content)
        logging.info("Successfully queued the emails.")
    except Exception as e:
        logging.error(f"Error sending emails: {str(e)}")


def send_emails_from_admin(message, position, emails):
    """
    Send professional emails from the ADMIN to a list of users.
    """
    try:
        subject = "Important Announcement from Administration"
        content = f"""
        <html>
            <body>
                <p>Dear Valued Member,</p>
                <p>We hope you are doing well. Please take note of the following announcement from our Administration:</p>
                <p style="margin-left:20px;">{message}</p>
                <p>Sincerely,<br>{position}<br>Administration</p>
                <p>Thank you for your attention.</p>
            </body>
        </html>
        """
        add_to_email_queue(emails, subject, content)
        logging.info("Successfully queued the emails.")
    except Exception as e:
        logging.error(f"Error sending emails: {str(e)}")


def send_approval_email(email, name, club, position,unsubscribe_token, isstudent):
    """
    Send a professional email notifying the user of their approval.
    """
    try:
        if isstudent is False:
            subject = "Application Approval Notification"
            content = f"""
            <html>
                <body>
                    <p>Dear {name},</p>
                    <p>We are pleased to inform you that your application has been approved.</p>
                    <p>Please find your details below:</p>
                    <ul>
                        <li><strong>Club:</strong> {club}</li>
                        <li><strong>Position:</strong> {position}</li>
                    </ul>
                    <p>We look forward to your contributions and are excited to welcome you aboard.</p>
                    <p>Sincerely,<br>The {club} Team</p>
                </body>
            </html>
            """
            # Example quota check; adjust the condition as needed.
            if check_brevo_email_quota(Email_limit_API) > 50:
                send_single_email.send(email, subject, content)
                logging.info(f"Approval email sent to {email}")
        else:
            unsubscribe_link=f"http://127.0.0.1:5000/Unsuscribe?token={unsubscribe_token}"
            subject = f"Stay Updated with the Latest News from Campus Connect : {club}"
            content = f"""
            <html>
            <body>
                <p>Dear {name},</p>
                <p>We hope this email finds you well! We're excited to have you as a part of our community here at <strong>Campus Connect</strong>. We’re committed to keeping you informed about the latest events, announcements, and activities within your college community.</p>

                <h3>Recent Updates:</h3>
                <ul>
                    <li><strong>Club Events:</strong> Stay up-to-date with various student club activities.</li>
                    <li><strong>College Announcements:</strong> Important news from your college campus.</li>
                    <li><strong>Opportunities:</strong> Get involved in upcoming student projects and initiatives.</li>
                </ul>

                <p>If you wish to unsubscribe from receiving these notifications, please click on the link below:</p>
                <p><a href="{unsubscribe_link}">Unsubscribe from Notifications</a></p>

                <p>Thank you for being a part of <strong>Campus Connect</strong>! If you have any questions or need assistance, feel free to reach out.</p>

                <p>Best regards,<br> The Campus Connect Team</p>
                
            </body>
            </html>
            """
            
            send_single_email.send(email,subject,content)
            logging.info(f"Joined {club} from {email}")

    except Exception as e:
        logging.error(f"Failed to send approval email to {email}: {str(e)}")


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


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/api/login', methods=['POST'])
@limiter.limit("5/minute")
def login():
    try:
        data = LoginSchema().load(request.form)
    except ValidationError as err:
        return error_response(err.messages, 400)

    user_id = data['user_id']
    password = data['password']

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Check user table
    cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()

    # Check admin table
    cur.execute("SELECT * FROM admin WHERE user_id = %s", (user_id,))
    admin = cur.fetchone()

    cur.close()
    conn.close()

    if user and check_password_hash(user['password'], password):
        # Mark session as permanent so it uses the lifetime defined in config
        session.permanent = True
        session['user_id'] = user_id
        session['role'] = user['position']  # or any other info you need
        return jsonify({"message": "Login successful", "user_id": user_id, "name": user['name'], "position": user['position'], "course": user['course'], "club": user['club']}), 200

    elif admin and check_password_hash(admin['password'], password):
        session.permanent = True
        session['user_id'] = user_id
        session['role'] = admin['position']
        return jsonify({"message": "Login successful", "user_id": user_id, "position": admin['position']}), 200
    else:
        return error_response("Invalid credentials", 401)


@app.route('/api/register', methods=['POST'])
@limiter.limit("3/minute")
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
    email = request.form.get('email')
    user_id = request.form.get('user_id')

    if not email:
        return error_response("Email is required", 400)

    conn = get_db_connection()
    if not conn:
        return error_response("Database connection failed", 500)

    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()

    if not user:
        return error_response("User not found", 404)
    if user['email'] != email:
        return error_response("Email does not match", 400)
    # Generate a secure reset token
    reset_token = secrets.token_urlsafe(32)
    expiry_time = datetime.utcnow() + timedelta(hours=1)  # <-- Add this

# Update the database
    cur.execute("""
        UPDATE users 
        SET reset_token = %s, reset_token_expiry = %s 
        WHERE email = %s
    """, (reset_token, expiry_time, user['email']))
    conn.commit()
    cur.close()
    conn.close()

    reset_link = f"http://localhost:8080/reset-password?token={reset_token}"
    content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <p>Dear Valued User,</p>
        <p>You recently requested to reset your password. To proceed with the password reset, please click the button below:</p>
        <p style="text-align: center;">
        <a href="{reset_link}" style="display: inline-block; padding: 10px 20px; background-color: #007BFF; color: #ffffff; text-decoration: none; border-radius: 4px;">
            Reset Your Password
        </a>
        </p>
        <p>If you did not request a password reset, please disregard this email or contact our support team immediately.</p>
        <p>Thank you for your prompt attention to this matter.</p>
        <p>Sincerely,<br>Your Support Team</p>
    </body>
    </html>
    """

    if check_brevo_email_quota(Email_limit_API) != 0:
        send_single_email(email, "Password Reset Request", content)
    else:
        return jsonify({"message": "Email was not sent due to email limit."})

    return jsonify({"message": "Password reset email sent."}), 200


@app.route('/api/get_user/<string:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

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
def get_approvals(position, club_name):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

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
            logging.info(f"Student-Coordinator of {club_name}")
            return jsonify({"Club Members are automaticaly approved "})

        # Fetch approvals based on hierarchy
        if position == 'admin':

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
    cur = conn.cursor(cursor_factory=RealDictCursor)

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
        send_approval_email(
            approval["email"],
            approval["name"],
            approval["club"],
            approval["position"],unsubscribe_token="",isstudent=False
        )
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
    cur = conn.cursor(cursor_factory=RealDictCursor)

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
        clear_rejected_table_if_full()
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
        cur = conn.cursor(cursor_factory=RealDictCursor)

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


@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    reset_token = data.get('token')
    new_password = data.get('new_password')

    if not reset_token or not new_password:
        return jsonify({"error": "Token and new password are required"}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # Check if the token is valid
        cur.execute("SELECT * FROM users WHERE reset_token = %s",
                    (reset_token,))
        user = cur.fetchone()

        if not user:
            return jsonify({"error": "Invalid or expired token"}), 400

        if datetime.utcnow() > user['reset_token_expiry']:
            return jsonify({"error": "Token expired"}), 400
        # Update the user's password and clear the reset token
        hashed_password = generate_password_hash(new_password, salt_length=5)
        cur.execute(
            "UPDATE users SET password = %s, reset_token = NULL WHERE reset_token = %s",
            (hashed_password, reset_token)
        )
        conn.commit()

        return jsonify({"message": "Password reset successfully"}), 200

    except Exception as e:
        conn.rollback()
        logging.error(f"Error during unsubscribe: {str(e)}")
        abort(500, description="Internal server error")

    finally:
        cur.close()
        conn.close()


@app.route('/api/send_message', methods=['POST'])
def send_message():
    """Sends a message to a user via email. And Emits Notiffication on Home-Page"""
    data = request.json
    role = data.get('role')
    message = data.get('message')
    position = data.get('postion')
    club = data.get('club')

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        emails = []
        if position == "student-coordinator":
            # student database isnt created
            cur.execute("SELECT email FROM student_club_subscriptions WHERE club = %s AND notification_consent = %s", (club, True))
            emails=cur.fetchall()
            emails = [dict(row) for row in emails]
            send_emails_apart_from_admin(message, position, emails, club)           
            logging.info(f"Email sent from {position} to members of {club}") 
            
            insert_query = """
            INSERT INTO club_messages (club_name, message, sent_at)
            VALUES (%s, %s, %s);
            """
            current_timestamp = datetime.now()
            cur.execute(insert_query, (club, message, current_timestamp))
            conn.commit()          
            send_notification.send(club, message)
            delete_old_messages()
            logging.info(f"Email sent to Students of{club}")

        elif position == "Admin":

            cur.execute(
                "SELECT email FROM users"
            )
            emails = cur.fetchall()
            emails = [dict(row) for row in emails]
            send_emails_from_admin(message, position, emails)
            logging.info(f"Email sent from ADMIN to {role} of all clubs")

        else:
            cur.execute(
                "SELECT email FROM users WHERE club = %s",
                (club,)
            )
            emails = cur.fetchall()
            emails = [dict(row) for row in emails]
            send_emails_apart_from_admin(message, position, emails, club)
            logging.info(f"Email sent from {position} to members of {club}")

        return jsonify({"message": "Message sent successfully"}), 200

    except:
        conn.rollback()
        logging.error(
            {"Error while sending message:Likely to be beacause REDIS or DRMATIQ"})
        return jsonify({"error": "Something went wrong"}), 500

    finally:
        cur.close()
        conn.close()
        
@app.route('/Unsuscribe', methods=['GET'])
def unsuscribe():
    # Retrieve the token from the query parameter
    token = request.args.get('token')
    
    if not token:
        abort(400, description="Token not provided")

    try:
        # Establish a database connection
        conn = get_db_connection()
        cur = conn.cursor()

        # Check if the token exists in the subscriptions table
        cur.execute("SELECT * FROM student_club_subscriptions WHERE unsubscribe_token = %s", (token,))
        user = cur.fetchone()

        if user is None:  # Check if no user was found
            abort(404, description="Invalid token")

        # Proceed with unsubscribing the user if the token is valid
        cur.execute("DELETE FROM student_club_subscriptions WHERE unsubscribe_token = %s", (token,))
        conn.commit()

        # Log the deletion with more specific details (e.g., user_id)
        logging.info(f"User with token {token} unsubscribed successfully")

        return jsonify({"message": "Successfully unsubscribed"}), 200
    except Exception as e:
        # Catch unexpected errors and log them
        if  '404 Not Found: Invalid token' in {str(e)}:
            abort(404, description="Invalid token")
        logging.error(f"Error during unsubscribe: {str(e)}")
        abort(500, description="Internal server error")
    
    finally:
        # Ensure the cursor and connection are closed
        cur.close()
        conn.close()
        
@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT id, message, sent_at, club_name 
            FROM club_messages  
            ORDER BY sent_at ASC
        ''')
        events = cur.fetchall()
        events_list = [
            {
                'id': event[0],
                'message': event[1],
                'date_time': event[2].isoformat(),
                'club': event[3]
            }
            for event in events
        ]
        return jsonify(events_list)
        
    except Exception as e:
        print(f"Error fetching events: {str(e)}")
        return jsonify({'error': 'Failed to fetch events'}), 500
    finally:
        cur.close()
        conn.close()
          
@app.route('/api/ClubForm', methods=['POST'])
def studentdata():
    try:
        data = request.get_json()
        unsuscribe_token = secrets.token_urlsafe(32)
        if not data:
            return jsonify({"error": "No data received"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        insert_query = '''
        INSERT INTO student_club_subscriptions (name, student_id, email, year, club, notification_consent, unsubscribe_token)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        '''

        data_tuple = (
            data['name'],
            data['studentId'],
            data['email'],
            data['year'],
            data['club'],
            data['notificationConsent'],
            unsuscribe_token
        )

        # Execute the query
        cursor.execute(insert_query, data_tuple)
        conn.commit()
        send_approval_email(data['email'],data['name'],data['club'],unsubscribe_token=unsuscribe_token,isstudent=True,position="")
        print("Data inserted successfully.")

        return jsonify({"message": "Successful"}), 200

    except Exception as e:
        print("Error:", e)
        
        return jsonify({"error": "Something went wrong"}), 500


# Run the Flask App
if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
