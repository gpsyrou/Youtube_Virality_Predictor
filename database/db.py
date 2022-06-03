import sqlite3
from typing import List

db_name = 'TubeDB.sqlite'
metadata_table_name = 'TubeMetadata'
header_table_name = 'TubeMetadataHeader'
lines_table_name = 'TubeMetadataLines'
channels_table_name = 'TubeChannels'

conn = sqlite3.connect(db_name)
c = conn.cursor()


def get_distinct_video_ids_from_db_table(table_name: str) -> List[str]:
    videos_lines_create_table_q = '''
        SELECT DISTINCT VideoID
        FROM {0}
    '''.format(table_name)

    result = c.execute(videos_lines_create_table_q)
    video_id_ls = []
    for row in result:
        video_id_ls.append(row[0])
    return list(set(video_id_ls))
