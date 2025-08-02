import sqlite3


class Database:
    def __init__(self, db_name: str = "cashcounter.db") -> None:
        self.db_name = db_name

    def query(self, sql: str, params: tuple = tuple()) -> list[tuple] | int | None:
        with sqlite3.connect(self.db_name) as conn:
            sql = sql.strip().lower()  # Cleaning up the query
            conn.row_factory = (
                sqlite3.Row
            )  # Ensuring the column names are returned in the result
            cur = conn.cursor()
            cur.execute(sql, params)

            if sql.startswith("select"):
                return cur.fetchall()  # Returning the results for SELECT queries
            elif sql.startswith("insert"):
                conn.commit()
                return (
                    cur.lastrowid
                )  # Returning the ID of the last row inserted for INSERT queries
            else:
                conn.commit()  # For all other queries, returning None

        return None
