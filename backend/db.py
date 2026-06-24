import psycopg2


def get_connection():

    conn = psycopg2.connect(
        dbname='Osman_kp',
        user='postgres',
        password='100Osman_@',
        host='localhost',
        port='5432'
    )

    return conn