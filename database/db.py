import sqlite3
import os

#if os.path.exists('TubeDB.sqlite'):
#    os.remove('TubeDB.sqlite')

db_name = 'TubeDB.sqlite'
metadata_table_name = 'TubeMetadata'

conn = sqlite3.connect(db_name)
c = conn.cursor()


# Drop target table query
def drop_target_table(table_name: str):
    drop_table_q = '''DROP TABLE {0}'''.format(table_name)
    c.execute(drop_table_q)
    conn.commit()

# drop_target_table(table_name=metadata_table_name)


# Create target table query
def create_target_table(table_name: str):
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
             Number_Of_Views BIGINT NOT NULL,
             Video_Url TEXT NOT NULL,
             CreatedDate DATE,
             CreatedDatetime DATETIME,
             
             CONSTRAINT uc_video_day UNIQUE (Video_id, CreatedDate)
        )
    '''.format(table_name)

    c.execute(metadata_create_table_q)
    conn.commit()

# create_target_table(table_name=metadata_table_name)


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
        Number_Of_Views,
        Video_Url,
        CreatedDate,
        CreatedDatetime
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
         {11},
        '{12}',
        DATE(),
        DATETIME()
    )
'''
