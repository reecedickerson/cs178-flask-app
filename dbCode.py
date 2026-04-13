# dbCode.py
# Author: Your Name
# Helper functions for database connection and queries

import pymysql
import creds

def get_conn():
    """Returns a connection to the MySQL RDS instance."""
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
    )
    return conn

def execute_query(query, args=()):
    """Executes a SELECT query and returns all rows as dictionaries."""
    cur = get_conn().cursor(pymysql.cursors.DictCursor)
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

# Function added with help from VSCode's copilot
def execute_insert(query, args=()):
    """Executes an INSERT query and commits the changes."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()
    conn.close()

def execute_delete(query, args=()):
    """Executes a DELETE query and commits the changes."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()
    conn.close()

# Function added with help from VSCode's copilot
def execute_update(query, args=()):
    """Executes an UPDATE query and commits the changes."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    cur.close()
    conn.close()

# The following functions were added with help from VSCode's copilot to support the update movie functionality in flaskapp.py
def get_movie_id_by_title(title):
    """Gets movie_id by title."""
    query = "SELECT movie_id FROM movie WHERE title = %s"
    result = execute_query(query, (title,))
    return result[0]['movie_id'] if result else None

def update_movie_genres(movie_id, genre_names):
    """Updates genres for a movie. genre_names should be a list of genre names."""
    if not genre_names:
        return
    
    # First, delete existing genres for this movie
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM movie_genres WHERE movie_id = %s", (movie_id,))
    
    # Then insert new genres
    for genre_name in genre_names:
        genre_name = genre_name.strip()
        if genre_name:
            # Get genre_id
            cur.execute("SELECT genre_id FROM genre WHERE genre_name = %s", (genre_name,))
            genre_result = cur.fetchone()
            if genre_result:
                genre_id = genre_result[0]
                cur.execute("INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s)", (movie_id, genre_id))
    
    conn.commit()
    cur.close()
    conn.close()

def update_movie_languages(movie_id, language_names):
    """Updates languages for a movie. language_names should be a list of language names."""
    if not language_names:
        return
    
    # First, delete existing languages for this movie
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM movie_languages WHERE movie_id = %s", (movie_id,))
    
    # Then insert new languages
    for language_name in language_names:
        language_name = language_name.strip()
        if language_name:
            # Get language_id
            cur.execute("SELECT language_id FROM language WHERE language_name = %s", (language_name,))
            language_result = cur.fetchone()
            if language_result:
                language_id = language_result[0]
                cur.execute("INSERT INTO movie_languages (movie_id, language_id) VALUES (%s, %s)", (movie_id, language_id))
    
    conn.commit()
    cur.close()
    conn.close()