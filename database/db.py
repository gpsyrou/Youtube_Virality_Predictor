import sqlite3

db_name = 'TubeDB.sqlite'
metadata_table_name = 'TubeMetadata'
header_table_name = 'TubeMetadataHeader'
lines_table_name = 'TubeMetadataLines'

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
             {0}ID INTEGER PRIMARY KEY AUTOINCREMENT,
             ChannelID TEXT NOT NULL,
             VideoID TEXT NOT NULL,
             Title TEXT NOT NULL,
             Description TEXT NOT NULL,
             Thumbnail TEXT NOT NULL,
             Duration DECIMAL(10,5) NOT NULL,
             Genre TEXT NOT NULL,
             Regions TEXT NOT NULL,
             PublishedDate DATETIME NOT NULL,
             UploadDate DATETIME NOT NULL,
             NumberOfViews BIGINT NULL,
             NumberOfLikes BIGINT NULL,
             VideoUrl TEXT NOT NULL,
             CreatedDate DATE,
             CreatedDatetime DATETIME,

             CONSTRAINT uc_video_day UNIQUE (VideoId, CreatedDate)
        )
    '''.format(table_name)

    c.execute(metadata_create_table_q)
    conn.commit()

# create_target_table(table_name=metadata_table_name)


# Insert into target table query
insert_into_q = '''
    INSERT INTO {0} (
        ChannelID,
        VideoID,
        Title,
        Description,
        Thumbnail,
        Duration,
        Genre,
        Regions,
        PublishedDate,
        UploadDate,
        NumberOfViews,
        NumberOfLikes,
        VideoUrl,
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
         {12},
        '{13}',
        DATE(),
        DATETIME()
    )
'''


# Header
def create_video_header_table(table_name: str):
    videos_header_create_table_q = '''
        CREATE TABLE {0}
        (
             {0}ID INTEGER PRIMARY KEY AUTOINCREMENT,
             ChannelID TEXT NOT NULL,
             VideoID TEXT NOT NULL,
             Title TEXT NOT NULL,
             Description TEXT NOT NULL,
             Thumbnail TEXT NOT NULL,
             Duration DECIMAL(10,5) NOT NULL,
             Genre TEXT NOT NULL,
             Regions TEXT NOT NULL,
             PublishedDate DATETIME NOT NULL,
             UploadDate DATETIME NOT NULL,
             VideoUrl TEXT NOT NULL,
             CreatedDate DATE,
             CreatedDatetime DATETIME,

             CONSTRAINT uc_header_video_day UNIQUE (VideoId, CreatedDate)
        )
    '''.format(table_name)

    c.execute(videos_header_create_table_q)
    conn.commit()


insert_into_video_header_q = '''
    INSERT INTO {0} (
        ChannelID,
        VideoID,
        Title,
        Description,
        Thumbnail,
        Duration,
        Genre,
        Regions,
        PublishedDate,
        UploadDate,
        VideoUrl,
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
         {9},
         {10},
        '{11}',
        DATE(),
        DATETIME()
    )
'''

# create_video_header_table(table_name=header_table_name)


# Lines
def create_video_lines_table(table_name: str):
    videos_lines_create_table_q = '''
        CREATE TABLE {0}
        (
             {0}ID INTEGER PRIMARY KEY AUTOINCREMENT,
             ChannelID TEXT NOT NULL,
             VideoID TEXT NOT NULL,
             NumberOfViews BIGINT NULL,
             NumberOfLikes BIGINT NULL,
             CreatedDate DATE,
             CreatedDatetime DATETIME,

             CONSTRAINT uc_lines_video_day UNIQUE (VideoId, CreatedDate)
        )
    '''.format(table_name)

    c.execute(videos_lines_create_table_q)
    conn.commit()


insert_into_video_lines_q = '''
    INSERT INTO {0} (
        ChannelID,
        VideoID,
        NumberOfViews,
        NumberOfLikes,
        CreatedDate,
        CreatedDatetime
    )
    VALUES
    (
        '{1}',
        '{2}',
         {3},
         {4},
        DATE(),
        DATETIME()
    )
'''

# create_video_lines_table(table_name=lines_table_name)
