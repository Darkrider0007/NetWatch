from database.database import get_connection


class HistorySearch:

    def search(self, text: str):

        conn = get_connection()

        cur = conn.cursor()

        cur.execute(
            """
            SELECT *
            FROM connections
            WHERE process LIKE ?
               OR publisher LIKE ?
               OR remote_host LIKE ?
               OR remote_ip LIKE ?
            ORDER BY id DESC
            LIMIT 500
            """,
            (
                f"%{text}%",
                f"%{text}%",
                f"%{text}%",
                f"%{text}%",
            ),
        )

        rows = cur.fetchall()

        conn.close()

        return rows