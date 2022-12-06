
"""
THIS CODE TAKES ALL THE DATA FROM THE BOOKMARKS DB

CREATES A STATIC HTML PAGE AT ROOT DIRECTORY CALLED _bookmarks.html

THIS ALLOWS ME TO REFERENCE IT WITHOUT OPENING THE FLASK APP

"""

import sqlite3
import os
from pathlib import Path

BASEPATH       = str(Path(os.getcwd()).parent.absolute()) + '/'

import sqlite3
import requests

# create a connection to the database
conn = sqlite3.connect(BASEPATH + "bookmarks.db")

# create a cursor to execute SQL commands
cursor = conn.cursor()

# create a dictionary to store the bookmarks by category
bookmarks = {}

# execute a SQL command to get all the rows from the bookmarks table
cursor.execute("SELECT * FROM bookmarks")

# iterate through the rows in the result set
for row in cursor:
    # get the category for the current bookmark
    category = row[2]

    # check if the category is already in the dictionary
    if category not in bookmarks:
        # if it's not, add it to the dictionary
        bookmarks[category] = []

    # add the current bookmark to the list of bookmarks for the current category
    bookmarks[category].append({
        "id": row[0],
        "name": row[1],
        "url": row[3]
    })

# create a string to hold the HTML code for the bookmarks
html = "<html>\n <head><link rel='stylesheet' href='scripts/style.css'></head>\n<body class='dracula' > \n"
html += "<center><h1>Adams BookMarks</h1></center> <br> \n"
html += "<center>Go to this directory to make changes /Users/adammcmurchie/code/tools/bookmarks</center> \n <br>"


# iterate through the categories in the dictionary
for category in bookmarks:
    # add the category name to the HTML string
    html += "<h2>" + category + "</h2>\n"

    # iterate through the bookmarks in the current category
    for bookmark in bookmarks[category]:
        
        if('https' in bookmark['url']):
            subURL = bookmark['url'].split('https://')[1:][0]
        elif('http' in bookmark['url']):
            subURL = bookmark['url'].split('http://')[1:][0]
        else:
            subURL = 'static.vecteezy.com/system/resources/previews/004/639/366/original/error-404-not-found-text-design-vector.jpg'

        print('getting url for ' + str(bookmark["url"]) + ' which is ' + str(subURL))

        image_url = requests.get("https://shot.screenshotapi.net/screenshot?token=" + TOKEN + "&url=https%3A%2F%2F" + subURL + "&output=image&file_type=png&wait_for_event=load")
        image_url = image_url.url
        # add the bookmark name, url, and preview image to the HTML string
        html += "<a href='" + bookmark["url"] + "'><h3>" + bookmark["name"] + "</h3> <br><img src='" + image_url + "'></a><br>\n\n"

# close the HTML body and document
html += "</body>\n</html>"

# write the HTML string to a file
with open(BASEPATH + "_bookmarks.html", "w") as file:
    file.write(html)

# close the database connection
conn.close()
