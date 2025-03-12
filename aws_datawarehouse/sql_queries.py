from configparser import ConfigParser

# Load config file
config = ConfigParser()
config.read("dwh.cfg")

# ==========================================
# SQL Queries for AWS Redshift ETL Pipeline
# ==========================================

# ==========================================
# 1. DROP TABLE QUERIES
# ==========================================
# These queries ensure that tables do not already exist before creating new ones.

drop_staging_events = "DROP TABLE IF EXISTS staging_events;"
drop_staging_songs = "DROP TABLE IF EXISTS staging_songs;"
drop_songplays = "DROP TABLE IF EXISTS songplays;"
drop_users = "DROP TABLE IF EXISTS users;"
drop_songs = "DROP TABLE IF EXISTS songs;"
drop_artists = "DROP TABLE IF EXISTS artists;"
drop_time = "DROP TABLE IF EXISTS time;"

drop_table_queries = [
    drop_staging_events, drop_staging_songs, drop_songplays,
    drop_users, drop_songs, drop_artists, drop_time
]

# ==========================================
# 2. CREATE STAGING TABLES
# ==========================================
# These tables hold raw JSON data from S3 before transformation.

create_staging_events = """
    CREATE TABLE IF NOT EXISTS staging_events (
        artist VARCHAR,
        auth VARCHAR,
        firstName VARCHAR,
        gender VARCHAR,
        itemInSession INT,
        lastName VARCHAR,
        length FLOAT,
        level VARCHAR,
        location VARCHAR,
        method VARCHAR,
        page VARCHAR,
        registration BIGINT,
        sessionId INT,
        song VARCHAR,
        status INT,
        ts BIGINT,
        userAgent VARCHAR,
        userId INT
    );
"""

create_staging_songs = """
    CREATE TABLE IF NOT EXISTS staging_songs (
        num_songs INT,
        artist_id VARCHAR,
        artist_latitude FLOAT,
        artist_longitude FLOAT,
        artist_location VARCHAR,
        artist_name VARCHAR,
        song_id VARCHAR,
        title VARCHAR,
        duration FLOAT,
        year INT
    );
"""

# ==========================================
# 3. CREATE FACT & DIMENSION TABLES (STAR SCHEMA)
# ==========================================
# FACT TABLE: songplays (Main table that contains user song activity)

create_songplays = """
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id INT IDENTITY(0,1) PRIMARY KEY,
        start_time TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        level VARCHAR,
        song_id VARCHAR,
        artist_id VARCHAR,
        session_id INT,
        location VARCHAR,
        user_agent VARCHAR
    );
"""

# DIMENSION TABLES
create_users = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INT PRIMARY KEY,
        first_name VARCHAR,
        last_name VARCHAR,
        gender VARCHAR,
        level VARCHAR
    );
"""

create_songs = """
    CREATE TABLE IF NOT EXISTS songs (
        song_id VARCHAR PRIMARY KEY,
        title VARCHAR,
        artist_id VARCHAR,
        year INT,
        duration FLOAT
    );
"""

create_artists = """
    CREATE TABLE IF NOT EXISTS artists (
        artist_id VARCHAR PRIMARY KEY,
        name VARCHAR,
        location VARCHAR,
        latitude FLOAT,
        longitude FLOAT
    );
"""

create_time = """
    CREATE TABLE IF NOT EXISTS time (
        start_time TIMESTAMP PRIMARY KEY,
        hour INT,
        day INT,
        week INT,
        month INT,
        year INT,
        weekday INT
    );
"""

# ==========================================
# 4. COPY COMMANDS (LOAD DATA FROM S3 TO STAGING)
# ==========================================
# These queries load raw JSON data from S3 into Redshift staging tables.

# Retrieve values from config file
IAM_ROLE_ARN = config.get("IAM", "role_arn")
LOG_DATA = config.get("S3", "log_data")
LOG_JSONPATH = config.get("S3", "log_jsonpath")
SONG_DATA = config.get("S3", "song_data")
REGION = config.get("AWS", "region")

# COPY Commands to Load Data into Staging Tables
copy_staging_events = f"""
    COPY staging_events FROM '{LOG_DATA}'
    CREDENTIALS 'aws_iam_role={IAM_ROLE_ARN}'
    FORMAT AS JSON '{LOG_JSONPATH}'
    REGION '{REGION}';
"""

copy_staging_songs = f"""
    COPY staging_songs FROM '{SONG_DATA}'
    CREDENTIALS 'aws_iam_role={IAM_ROLE_ARN}'
    FORMAT AS JSON 'auto'
    REGION '{REGION}';
"""

# ==========================================
# 5. INSERT COMMANDS (LOAD FINAL STAR SCHEMA TABLES)
# ==========================================
# These queries transform raw data from staging into final tables.

# FACT TABLE: songplays (Main user activity table)
insert_songplays = """
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT 
        TIMESTAMP 'epoch' + e.ts / 1000 * INTERVAL '1 second' AS start_time,
        e.userId, 
        e.level, 
        s.song_id, 
        s.artist_id, 
        e.sessionId, 
        e.location, 
        e.userAgent
    FROM staging_events e
    LEFT JOIN staging_songs s 
    ON e.song = s.title
    AND e.artist = s.artist_name
    WHERE e.page = 'NextSong';
"""

# DIMENSION TABLES: Users, Songs, Artists, Time

insert_users = """
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT userId, firstName, lastName, gender, level
    FROM staging_events
    WHERE userId IS NOT NULL;
"""

insert_songs = """
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT DISTINCT song_id, title, artist_id, year, duration
    FROM staging_songs
    WHERE song_id IS NOT NULL;
"""

insert_artists = """
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL;
"""

insert_time = """
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT 
        start_time, 
        EXTRACT(hour FROM start_time), 
        EXTRACT(day FROM start_time), 
        EXTRACT(week FROM start_time), 
        EXTRACT(month FROM start_time), 
        EXTRACT(year FROM start_time), 
        EXTRACT(weekday FROM start_time)
    FROM songplays;
"""

# ==========================================
# 6. LISTS OF QUERIES FOR EXECUTION IN `create_tables.py` & `etl.py`
# ==========================================
# These lists are used in `create_tables.py` and `etl.py` for execution.

create_table_queries = [
    create_staging_events, create_staging_songs, create_songplays,
    create_users, create_songs, create_artists, create_time
]

drop_table_queries = [
    drop_staging_events, drop_staging_songs, drop_songplays,
    drop_users, drop_songs, drop_artists, drop_time
]

copy_table_queries = [copy_staging_events, copy_staging_songs]

insert_table_queries = [insert_songplays, insert_users, insert_songs, insert_artists, insert_time]
