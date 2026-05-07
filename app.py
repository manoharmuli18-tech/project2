from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', "secret123")   # Use environment variable in production

# Dummy user (you can later store in DB)
USERNAME = "Manohar"
PASSWORD = "Manohar"

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        if user == USERNAME and pwd == PASSWORD:
            session['user'] = user
            return redirect(url_for('index'))
        else:
            return "Invalid credentials"

    return render_template('login.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ---------------- HOME ----------------
def get_db_connection():
    database_url = os.environ.get('DATABASE_URL', "postgresql://neondb_owner:npg_BdnzA6xCYO1i@ep-muddy-dust-aqjnbq3g.c-8.us-east-1.aws.neon.tech/neondb?sslmode=require")
    return psycopg2.connect(database_url)

def create_posts_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    create_posts_table()

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('index.html', posts=posts)

# ---------------- CREATE POST ----------------
# Use the same connection function everywhere
@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            return "Form not submitted properly"

        # Switch to PostgreSQL to match the index route
        create_posts_table()
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # PostgreSQL uses %s as placeholders, not ?
        cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('index'))

    return render_template('create.html')

# ---------------- EDIT POST ----------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            return "Form not submitted properly"

        create_posts_table()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s", (title, content, id))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('index'))

    # GET request - fetch post
    create_posts_table()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cur.fetchone()
    cur.close()
    conn.close()

    if post is None:
        return "Post not found", 404

    return render_template('edit.html', post=post)

# ---------------- DELETE POST ----------------
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    create_posts_table()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM posts WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)