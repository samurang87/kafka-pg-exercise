import json
from dataclasses import asdict

from websitechecker.healthchecker import Health
from websitechecker.main import consumer


def test_consumer_happy_case(kafka, postgres, url):
    for i in range(3):
        health = Health(
            timestamp=1673023382577 + i,
            status_code=200,
            time_elapsed=50,
            pattern_found=True,
        )

        content = {"url": url, "pattern": "All Systems Operational", **asdict(health)}
        kafka.send(topic="websitechecker", value=json.dumps(content).encode())

    consumer(kafka, postgres, 1)

    assert postgres.n_messages_were_stored(3)


def test_consumer_malformed_data(kafka, postgres, url):

    wrong_content = {"url": url}
    kafka.send(topic="websitechecker", value=json.dumps(wrong_content).encode())

    for i in range(3):
        health = Health(
            timestamp=1673023382577 + i,
            status_code=200,
            time_elapsed=50,
            pattern_found=True,
        )

        content = {"url": url, "pattern": "All Systems Operational", **asdict(health)}
        kafka.send(topic="websitechecker", value=json.dumps(content).encode())

    consumer(kafka, postgres, 1)

    assert postgres.n_messages_were_stored(3)
