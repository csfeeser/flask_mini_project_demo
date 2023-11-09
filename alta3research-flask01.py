#!/usr/bin/env python3
"""json data borrowed from https://github.com/joeltgray/HarryPotterAPI/tree/main"""

import sqlite3 as sql
import json
import uuid
import random
from pprint import pprint
from flask import Flask, render_template, request, redirect, abort, make_response
from db_builder import *

app= Flask(__name__)

def db_reader():
    '''this is a 'helper' function; the database is read in many places
    so it is here to be re-used'''

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

    rows_as_dicts= []

    for row in rows:
        row_as_dict = dict(row)  # Convert the Row object to a dictionary
        rows_as_dicts.append(row_as_dict)  # Append the dictionary to the list

    # return the now-converted database data as a python list, which is returned by Flask as JSON. whew!
    
    if app.debug:
        pprint(rows_as_dicts[:2])

    return rows_as_dicts

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/random")
def randomquote():
    """returns a random quote; reads a cookie (if present) to see who was the last quote speaker.
    Will continue randomly pulling quotes until a new speaker is chosen."""

    rows= db_reader()
    
    if request.cookies.get("last_character"):
        while True:
            quote= random.choice(rows)
            if quote["speaker"] != request.cookies.get("last_character"):
                break

    else:
        quote= random.choice(rows)

    # add or update the cookie containing which quote speaker was recently chosen
    resp= make_response(render_template("random_quote.html", quotedict= quote))
    resp.set_cookie("last_character", quote["speaker"])

    return resp

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
    rows= db_reader()
    return rows

@app.route('/table')
def list_students():
    rows= db_reader()
    
    # feed the rows list into our jinja2 html template
    return render_template("list.html",rows = rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2224, debug = True)