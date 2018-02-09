#!/usr/bin/env python
import sys, sqlite3, os

list_args = '--save -s'

# Open Connection
mydirs_directory = os.environ['OKANE_DIR']
conn = sqlite3.connect(mydirs_directory + 'mydirs.sqlite');

# Creating cursor
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE IF NOT EXISTS Categories (
        id_category INTEGER,
        category_name TEXT,
        PRIMARY KEY (id_category)
    )
''')
