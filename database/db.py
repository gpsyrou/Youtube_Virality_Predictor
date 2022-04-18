import sqlite3
import os

if os.path.exists('TubeDB.sqlite'):
    os.remove('TubeDB.sqlite')

db_name = 'TubeDB.sqlite'
metadata_table_name = 'TubeMetadata'

conn = sqlite3.connect(db_name)
c = conn.cursor()

# Create target table query
metadata_create_table_q = '''
    CREATE TABLE {0}
    (
         {0}Id INTEGER PRIMARY KEY AUTOINCREMENT,
         Channel_id TEXT NOT NULL,
         Video_id TEXT NOT NULL,
         Title TEXT NOT NULL,
         Description TEXT NOT NULL,
         Thumbnail TEXT NOT NULL,
         Duration DECIMAL(10,5) NOT NULL,
         Genre TEXT NOT NULL,
         Regions TEXT NOT NULL,
         Published_Date DATETIME NOT NULL,
         Upload_Date DATETIME NOT NULL,
         Number_Of_Views BIGINT NOT NULL
    )
'''.format(metadata_table_name)

c.execute(metadata_create_table_q)
conn.close()

# Insert into target table query
insert_into_q = '''
    INSERT INTO {0} (
        Channel_id,
        Video_id,
        Title,
        Description,
        Thumbnail,
        Duration,
        Genre,
        Regions,
        Published_Date,
        Upload_Date,
        Number_Of_Views
    )
    VALUES
    (
        '{1}',
        '{2}',
        '{3}',
        '{4}',
        '{5}',
         {6},
        '{7}',
        '{8}',
        '{9}',
        '{10}',
         {11}
    )
'''
