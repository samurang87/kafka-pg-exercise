from typing import Any


class KafkaClient:
    def __init__(self, client: Any) -> None:
        self.client = client

    def send(self, topic: str, value: bytes):
        self.client.send(topic=topic, value=value)

    def get_messages(self):
        return self.client.poll().values()


class PostgresClient:
    def __init__(self, connection: Any) -> None:
        self.conn = connection

    def write(self, data):
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO website_requests
            (url, timestamp, status_code, pattern, matched_pattern, time_elapsed)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """,
            (data[0], data[1], data[2], data[3], data[4], data[5]),
        )

        self.conn.commit()

        cur.close()
