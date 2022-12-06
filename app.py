"""
A FLASK SQLITE BOOKMARKS APP

THE APP LETS YOU ADD NEW URLS WITH THE NAME AND CATEGORY TO THE DB

EACH ROW IN THE DB IS DISPLAYED ON THE PAGE, WITH A - SIGN TO DELETE IT 

IF YOU CLICK ON THE NAME IT WILL TAKE YOU TO THAT LINK

THERE IS ALSO A SEPARATE SCRIPT IN THE SCRIPTS FOLDER WHICH CREATS A STATIC HTML PAGE THAT INCLUDES

IMAGES AND DOESN'T REQUIRE THE SERVER TO RUN


"""


from flask import Flask, request, redirect, render_template
import sqlite3

# create the Flask app
app = Flask(__name__)

# connect to the SQLite database
def connect_db():
    return sqlite3.connect('bookmarks.db')

# create the bookmarks table in the database
def create_table():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE bookmarks (
            id INTEGER PRIMARY KEY,
            name TEXT,
            category TEXT,
            url TEXT
        )
    """)
    db.commit()

# add a new bookmark to the database
def add_bookmark(name, category, url):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO bookmarks (name, category, url)
        VALUES (?, ?, ?)
    """, (name, category, url))
    db.commit()

# delete a bookmark from the database
def delete_bookmark(id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        DELETE FROM bookmarks WHERE id = ?
    """, (id,))
    db.commit()

# get a list of all bookmarks from the database
def get_bookmarks():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT * FROM bookmarks
    """)
    return cursor.fetchall()

# handle requests to the homepage
@app.route('/')
def index():
    # get a list of all bookmarks
    bookmarks = get_bookmarks()

    # group bookmarks by category
    categories = {}
    for bookmark in bookmarks:
        id, name, category, url = bookmark
        if category not in categories:
            categories[category] = []
        categories[category].append((id, name, url))

    return render_template('index.html', categories=categories)

# handle requests to add a new bookmark
@app.route('/add', methods=['POST'])
def add():
    # get the user's input
    name = request.form['name']
    category = request.form['category']
    url = request.form['url']

    # add the bookmark to the database
    add_bookmark(name, category, url)

    # redirect the user back to the homepage
    return redirect('/')

@app.route('/style.css')
def css():
    return app.send_static_file('style.css')


# handle requests to delete a bookmark
@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    # delete the bookmark from the database
    delete_bookmark(id)

    # redirect the user back to the homepage
    return redirect('/')



# create the database and table if they don't exist
try:
    create_table()
except sqlite3.OperationalError:
    pass

# run the app
if __name__ == '__main__':
    app.run()
