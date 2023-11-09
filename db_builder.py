#!/usr/bin/env python3
import json
import sqlite3

def db_builder(jsondata):
    # Establish a connection to the SQLite database
    conn = sqlite3.connect('files/harry_potter.db')

    # Create a cursor object using the cursor() method
    cursor = conn.cursor()

    # Drop the table if it exists to ensure idempotency
    cursor.execute('DROP TABLE IF EXISTS quotes')
    
    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS quotes
                  (id TEXT PRIMARY KEY,
                   quote TEXT,
                   speaker TEXT,
                   story TEXT,
                   source TEXT)''')

    # Insert data
    for quote_dict in jsondata:
        cursor.execute('''INSERT INTO quotes (id, quote, speaker, story, source) VALUES (:id, :quote, :speaker, :story, :source)''', quote_dict)

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()
