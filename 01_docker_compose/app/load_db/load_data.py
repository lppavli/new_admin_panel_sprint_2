import os
import sqlite3
import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor, execute_batch

from data_classes import Movie, Style, StyleMovie, People, PeopleMovie

PAGE_SIZE = 100


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""

    # получаем данные из Sqlite

    sqlite_conn.row_factory = sqlite3.Row
    curs = sqlite_conn.cursor()

    curs.execute("SELECT * FROM film_work")
    movies = []
    while True:
        movies_data = curs.fetchmany(PAGE_SIZE)
        if not movies_data:
            break
        else:
            movies_list = [Movie(*row) for row in movies_data]
            movies.extend(movies_list)

    curs.execute("SELECT * FROM genre")
    styles = []
    while True:
        styles_data = curs.fetchmany(PAGE_SIZE)
        if not styles_data:
            break
        else:
            styles_list = [Style(*row) for row in styles_data]
            styles.extend(styles_list)

    curs.execute("SELECT * FROM genre_film_work")
    styles_movies = []
    while True:
        styles_movies_data = curs.fetchmany(PAGE_SIZE)
        if not styles_movies_data:
            break
        else:
            styles_movies_list = [StyleMovie(*row) for row in styles_movies_data]
            styles_movies.extend(styles_movies_list)

    curs.execute("SELECT * FROM person")
    people = []
    while True:
        people_data = curs.fetchmany(PAGE_SIZE)
        if not people_data:
            break
        else:
            people_list = [People(*row) for row in people_data]
            people.extend(people_list)

    curs.execute("SELECT * FROM person_film_work")
    people_movie = []
    while True:
        people_movie_data = curs.fetchmany(PAGE_SIZE)
        if not people_movie_data:
            break
        else:
            people_movie_list = [PeopleMovie(*row) for row in people_movie_data]
            people_movie.extend(people_movie_list)
    curs.close()

    # загружаем данные в Postgres

    query = 'INSERT INTO content.film_work (id, title, description, creation_date, file_path, ' \
            'rating, type, created, modified)' \
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING'
    insert_data = [(movie.id, movie.title, movie.description, movie.creation_date, movie.file_path,
                    movie.rating, movie.type, movie.created_at, movie.updated_at) for movie in movies]
    execute_batch(pg_conn.cursor(), query, insert_data, page_size=PAGE_SIZE)
    pg_conn.commit()
    query = 'INSERT INTO content.genre (id, name, description, created, modified) ' \
            'VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING'
    insert_data = [(style.id, style.name, style.description, style.created_at, style.updated_at) for style in styles]
    execute_batch(pg_conn.cursor(), query, insert_data, page_size=PAGE_SIZE)
    pg_conn.commit()
    query = 'INSERT INTO content.genre_film_work (id, genre_id, film_work_id, created) ' \
            'VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING'
    insert_data = [(sm.id, sm.genre_id, sm.film_work_id, sm.created_at) for sm in styles_movies]
    execute_batch(pg_conn.cursor(), query, insert_data, page_size=PAGE_SIZE)
    pg_conn.commit()
    query = 'INSERT INTO content.person (id, full_name, created, modified) ' \
            'VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING'
    insert_data = [(man.id, man.full_name, man.created_at, man.updated_at) for man in people]
    execute_batch(pg_conn.cursor(), query, insert_data, page_size=PAGE_SIZE)
    pg_conn.commit()
    query = 'INSERT INTO content.person_film_work (id, film_work_id, person_id, role, created) ' \
            'VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING'
    insert_data = [(pm.id, pm.film_work_id, pm.person_id, pm.role, pm.created_at) for pm in people_movie]
    execute_batch(pg_conn.cursor(), query, insert_data, page_size=PAGE_SIZE)
    pg_conn.commit()
    pg_conn.cursor().close()


if __name__ == '__main__':
    load_dotenv()
    dsl = {
        'dbname': os.getenv('SQL_DATABASE', 'movies_database'),
        'user': os.getenv('SQL_USER', 'app'),
        'password': os.getenv('SQL_PASSWORD', '123qwe'),
        'host': os.getenv('SQL_HOST', "127.0.0.1"),
        'port': os.getenv('SQL_PORT', 5432),
    }
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
