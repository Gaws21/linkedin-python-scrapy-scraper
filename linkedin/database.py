#!/usr/bin/python
import psycopg2

class Storage():
    """ Connect to the PostgreSQL database server """
    
    def __init__(self):
        self._conn = psycopg2.connect(
            database="myjobs",
            user="username",
            port='5432',
            host='localhost',
            password="password")    
        
        self._cursor = self._conn.cursor()

    def execute_query(self, query): 
        self._cursor.execute(query)

        try:
            query_return = self._cursor.fetchall()
            return query_return
        except:
            print("Without fetchone")
    
    def close(self):
        self._conn.commit()
        self._conn.close()
        self._cursor.close()