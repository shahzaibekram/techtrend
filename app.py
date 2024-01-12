import sqlite3
import logging
from flask import Flask, jsonify, render_template, request, url_for, redirect, flash

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
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)

# Define the main route of the web application
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered
# If the post ID is not found, a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        logger.warning(f"Requested post with ID {post_id} not found.")
        return render_template('404.html'), 404
    else:
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    return render_template('about.html')

# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            connection.commit()
            connection.close()

            logger.info(f"New post created: {title}")
            return redirect(url_for('index'))

    return render_template('create.html')

# Health check endpoint
@app.route('/healthz')
def healthz():
    return jsonify({"status": "ok"})

# Status endpoint
@app.route('/status')
def status():
    return jsonify({"status": "ok", "version": "1.0.0"})

# Start the application on port 3111
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3111')

