import sqlite3
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

def init_db():
    # Connect to the database and create the bookmarks table if it does not exist
    conn = sqlite3.connect('bookmarks.db')
    conn.execute("CREATE TABLE IF NOT EXISTS bookmarks (name TEXT, url TEXT, category TEXT)")
    conn.commit()

@app.route('/')
def home():
    # Connect to the database and get the bookmark list
    conn = sqlite3.connect('bookmarks.db')
    cursor = conn.execute("SELECT name, url, category FROM bookmarks")
    bookmarks = [{'name': name, 'url': url, 'category': category} for name, url, category in cursor]

    # Group the bookmarks by category
    categories = {}
    for bookmark in bookmarks:
        if bookmark['category'] not in categories:
            categories[bookmark['category']] = []
        categories[bookmark['category']].append(bookmark)

    # Render the bookmark list on the home page
    return render_template('home.html', categories=categories)

@app.route('/add', methods=['POST'])
def add_bookmark():
    # Get the name, URL, and category of the bookmark from the form
    name = request.form['name']
    url = request.form['url']
    category = request.form['category']

    # Connect to the database and add the bookmark if it does not already exist
    conn = sqlite3.connect('bookmarks.db')
    cursor = conn.execute("SELECT * FROM bookmarks WHERE name=? AND url=?", (name, url))
    if cursor.fetchone() is None:
        conn.execute("INSERT INTO bookmarks VALUES (?, ?, ?)", (name, url, category))
        conn.commit()

    # Redirect to the home page
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run()
