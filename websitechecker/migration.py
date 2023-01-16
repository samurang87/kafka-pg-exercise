import psycopg2

from websitechecker import config

migration = """
CREATE TABLE IF NOT EXISTS website_requests (
  url TEXT NOT NULL,
  timestamp BIGINT NOT NULL,
  status_code INTEGER NOT NULL,
  pattern TEXT,
  matched_pattern BOOLEAN,
  time_elapsed BIGINT NOT NULL,
  PRIMARY KEY (url, timestamp)
);
"""


def main():
    conn = psycopg2.connect(config.PG_ADDRESS)

    cur = conn.cursor()
    cur.execute(migration)
    cur.execute("commit")


if __name__ == "__main__":
    main()
