import sqlite3
import os

if os.path.exists('TubeDB.sqlite'):
    os.remove('TubeDB.sqlite')
    
conn = sqlite3.connect('TubeDB.sqlite')
c = conn.cursor()

metadata_create_table_q = '''
    CREATE TABLE TubeMetadata
    (
         TubeMetadataId INTEGER PRIMARY KEY AUTOINCREMENT,
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
'''

c.execute(metadata_create_table_q)


insert_into_q = '''
    INSERT INTO TubeMetadata (Channel_id, Video_id, Title, Description, Thumbnail, Duration, Genre, Regions, Published_Date, Upload_Date, Number_Of_Views)
    VALUES
    ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10})
'''.format(
v1.channel_id, 
v1.video_id, 
v1.title, 
v1.description, 
v1.thumbnail,
v1.video_duration, 
v1.video_genre, 
v1.regions_allowed, 
v1.published_date, 
v1.upload_date, 
v1.number_of_views
)

c.execute(insert_into_q)
