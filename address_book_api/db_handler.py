"""
For this library to work correctly, it is necessary to edit access
data according to the specifities of the SQL server of intended use.

:author: riccardo mei
:encoding: utf-8
"""

import pymysql

DB_ADDRESS = "127.0.0.1"
DB_PORT = 3306
DB_USER_NAME = "root"
DB_PASSWORD = "Password"


def get_connection():
    return pymysql.connect(
        host=DB_ADDRESS,
        port=DB_PORT,
        user=DB_USER_NAME,
        password=DB_PASSWORD,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


def _db_get_user_data(conn, list_user_id) -> None:
    row_ids = ", ".join(
        [str(user['utente_id']) for user in list_user_id]
    )
    sql = f"""
    SELECT utente_id
         , nome
         , cognome
         , email
         , telefono
      FROM class.rubrica
     WHERE utente_id IN ({row_ids});
    """
    print(sql)
    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def db_get_users(limit=10, offset=0):
    sql = """
    SELECT utente_id
      FROM class.rubrica
     LIMIT %s OFFSET %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (limit, offset))
            return _db_get_user_data(conn, cur.fetchall())


def db_delete_user(utente_id):
    sql = """
    DELETE
      FROM class.rubrica
     WHERE utente_id = %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            return cur.execute(sql, (utente_id, ))


def db_insert_user(dati_utente):
    placeholders = ", ".join(["%s" for _ in dati_utente])
    sql = f"""
    INSERT
    IGNORE
      INTO class.rubrica
        (nome, cognome, email, telefono)
    VALUES
        ({placeholders});
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, dati_utente)
            return cur.lastrowid


def db_exists_user(email, telefono):
    sql = """
    SELECT null
      FROM class.rubrica
     WHERE email = %s
        OR telefono = %s
     LIMIT 1;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (email, telefono))
            recordset = cur.fetchall()
            return bool(recordset)


def db_search_user(query, limit=10, offset=0):
    sql = """
    SELECT utente_id
         , nome
         , cognome
         , email
         , telefono
      FROM class.rubrica
     WHERE nome = %s
        OR cognome = %s
     LIMIT %s OFFSET %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (query, query, limit, offset))
            return cur.fetchall()


def db_update_user(utente):
    sql = """
    UPDATE class.rubrica
       SET nome = %s
         , cognome = %s
         , email = %s
         , telefono = %s
     WHERE utente_id = %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            return cur.execute(sql, utente)
