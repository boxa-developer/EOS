from django.db import connection


def query_one(query_str):
    with connection.cursor() as cursor:
        cursor.execute(
            query_str
        )
        row = cursor.fetchone()
    return row


def query_many(query_str):
    with connection.cursor() as cursor:
        cursor.execute(
            query_str
        )
        rows = cursor.fetchall()
    return rows
