#!/usr/bin/env python3
"""json data borrowed from https://github.com/joeltgray/HarryPotterAPI/tree/main"""

import sqlite3 as sql
import json
import uuid
from flask import Flask, render_template, request, redirect, abort
from db_builder import *

app= Flask(__name__)

# read in the JSON data from the local file
with open("files/quotes.json") as jsonfile:
    jsondata= json.load(jsonfile)

# use the imported db_builder script to re-build the database every time this code is run
db_builder(jsondata)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/addquote", methods=["POST"])
def addquote():
    try:
        quoteid = str(uuid.uuid4())
        quote   = request.form.get('quote')    
        speaker = request.form.get('speaker')
        story   = request.form.get('story')    
        source  = request.form.get('source')  

        # Connect to SQLite DB
        with sql.connect("files/harry_potter.db") as con:
            cur = con.cursor()
            
            # Insert the info from our form into the SQLite DB
            cur.execute("INSERT INTO quotes (id, quote, speaker, story, source) VALUES (?, ?, ?, ?, ?)", (quoteid, quote, speaker, story, source))
            
            # Commit the transaction to our SQLite DB
            con.commit()
        return redirect("/table")

    except Exception as err:
        return abort(err, 500)

@app.route("/json")
def data():
    return jsondata

@app.route('/table')
def list_students():
    # establishing connection to our db file
    con = sql.connect("files/harry_potter.db")

    # BEFORE ROW FACTORY
    # row= ["1", "Paul", 20000.00, "California"]
    con.row_factory = sql.Row
    # AFTER ROW FACTORY
    # row= {"id":"1", "name":"Paul", "salary":20000.00, "address":"California"}

    # creating "cursor object"
    cur = con.cursor()

    # use it to select (read out) the data that we want!
    cur.execute("SELECT * from quotes")           # pull all information from the table "students"

    # fetchall() collate all the data that our cursor grabbed into a single data object
    rows = cur.fetchall()

    # DEBUG LINES: I want to know what "rows" is and what it looks like!
    if app.debug:
                     # just the first three rows is fine
        for x in rows[:3]:
           print(dict(x))

                                     # feed the rows list into our jinja2 html template
    return render_template("list.html",rows = rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2224, debug = True)




