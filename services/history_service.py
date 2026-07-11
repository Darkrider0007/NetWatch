from database.database import get_connection
from models.connection import ConnectionInfo


class HistoryService:

    def save(self, connections: list[ConnectionInfo]):

        conn = get_connection()
        cur = conn.cursor()

        for c in connections:

            cur.execute(
                """
                INSERT INTO connections
                (
                    time,
                    process,
                    publisher,
                    pid,
                    protocol,
                    local_ip,
                    local_port,
                    remote_ip,
                    remote_port,
                    remote_host,
                    country,
                    status
                )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    c.time,
                    c.process,
                    c.publisher,
                    c.pid,
                    c.protocol,
                    c.local_ip,
                    c.local_port,
                    c.remote_ip,
                    c.remote_port,
                    c.remote_host,
                    c.country_name,
                    c.status,
                ),
            )

        conn.commit()
        conn.close()

    def clear(self):

        conn = get_connection()
        conn.execute(
            "DELETE FROM connections"
        )
        conn.commit()
        conn.close()