import sqlite3


class Database:

    db_name = "dbequipo.db"

    def run_query(self, db_name, query, parameters = ()):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
        return result

    