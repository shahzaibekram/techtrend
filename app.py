import sqlite3
import logging
from flask import Flask, jsonify, render_template, request, url_for, redirect, flash
from prometheus_flask_exporter import PrometheusMetrics

# Function to get a database connection.
# This function connects to the database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define metrics for Prometheus
metrics = PrometheusMetrics(app)

# Define the main route of the web application
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    
    # Log event when existing articles are retrieved
    for post in posts:
        logger.info(f"Article '{post['title']}' retrieved!")

    return render_template('index.html', posts=posts)

# ... (other routes remain the same)

# Health check endpoint
@app.route('/healthz')
def healthz():
    return jsonify({"status": "ok", "message": "OK healthy"})

# Metrics endpoint
@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    post_count = len(connection.execute('SELECT * FROM posts').fetchall())
    connection.close()

    return jsonify({"db_connection_count": 1, "post_count": post_count})

# Start the application on port 3111
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3111')
