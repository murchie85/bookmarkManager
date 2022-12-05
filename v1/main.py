import sqlite3
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

def init_db():
    # Connect to the database and create the bookmarks table if it does not exist
    conn = sqlite3.connect('bookmarks.db')
    conn.execute("CREATE TABLE IF NOT EXISTS bookmarks (name TEXT, url TEXT)")
    conn.commit()

@app.route('/')
def home():
    # Connect to the database and get the bookmark list
    conn = sqlite3.connect('bookmarks.db')
    cursor = conn.execute("SELECT name, url FROM bookmarks")
    bookmarks = [{'name': name, 'url': url} for name, url in cursor]

    # Render the bookmark list on the home page
    return render_template('home.html', bookmarks=bookmarks)

@app.route('/add', methods=['POST'])
def add_bookmark():
    # Get the name and URL of the bookmark from the form
    name = request.form['name']
    url = request.form['url']

    # Connect to the database and add the bookmark if it does not already exist
    conn = sqlite3.connect('bookmarks.db')
    cursor = conn.execute("SELECT * FROM bookmarks WHERE name=? AND url=?", (name, url))
    if cursor.fetchone() is None:
        conn.execute("INSERT INTO bookmarks VALUES (?, ?)", (name, url))
        conn.commit()

    # Redirect to the home page
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run()
