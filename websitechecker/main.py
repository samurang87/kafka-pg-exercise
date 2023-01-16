import argparse
import json
import logging
from dataclasses import asdict
from time import sleep
from typing import Any

import psycopg2
from kafka import KafkaConsumer, KafkaProducer

import websitechecker.config as config
from websitechecker.clients import KafkaClient, PostgresClient
from websitechecker.healthchecker import healthcheck

LOG = logging.getLogger("websitechecker")
LOG.setLevel(logging.DEBUG)
CH = logging.StreamHandler()
CH.setLevel(logging.DEBUG)
LOG.addHandler(CH)


def producer(kafka_producer: Any, n_iterations: int | None = None) -> None:
    """
    Runs healthchecks on a list of urls provided in a configuration files and sends
    the results to a Kafka topic.

    Args:
        kafka_producer (Any): Kafka producer client
        n_iterations (int | None, optional): Optional number of iterations to run the
            healthchecks for. Defaults to None (running forever).
    """
    LOG.info("Producer started")

    kafka = KafkaClient(client=kafka_producer)

    counter = 0

    while counter != n_iterations:
        counter += 1

        for item in config.to_check:

            url, match = item

            check = healthcheck(url=url, match=match)

            payload = {"url": url, "pattern": match, **asdict(check)}
            kafka.send("websitechecker", json.dumps(payload).encode())

        sleep(2)


def consumer(
    kafka_consumer: Any, postgres_client: Any, n_iterations: int | None = None
) -> None:
    """
    Fetches messages with healthcheck data from a Kafka topic and saves them to a
       Postgres table.

    Args:
        kafka_consumer (Any): Kafka consumer client
        postgres_client (Any): Postgres client
        n_iterations (int | None, optional): Optional number of iterations to fetch data
            for. Defaults to None (run forever).
    """
    LOG.info("Consumer started")

    kafka = KafkaClient(kafka_consumer)

    counter = 0

    while counter != n_iterations:

        counter += 1
        for msg in kafka.get_messages():

            try:
                raw = json.loads(msg[0].value.decode("utf-8"))

                to_write = [
                    raw["url"],
                    raw["timestamp"],
                    raw["status_code"],
                    raw["pattern"],
                    raw["pattern_found"],
                    raw["time_elapsed"],
                ]

            except Exception:
                LOG.exception(f"Unexpected error while parsing message {msg[0]}")
                continue

            postgres_client.write(data=to_write)

        sleep(1)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("type", choices=["consumer", "producer"])
    args = parser.parse_args()

    if args.type == "producer":
        client = KafkaProducer(
            bootstrap_servers=config.KAFKA_ADDRESS,
            security_protocol="SSL",
            ssl_cafile=config.SSL_CAFILE,
            ssl_certfile=config.SSL_CERTFILE,
            ssl_keyfile=config.SSL_KEYFILE,
        )
        producer(kafka_producer=client)
        client.close()

    if args.type == "consumer":
        conn = psycopg2.connect(config.PG_ADDRESS)
        client = KafkaConsumer(
            "websitechecker",
            bootstrap_servers=config.KAFKA_ADDRESS,
            client_id="CONSUMER_CLIENT_ID",
            group_id="CONSUMER_GROUP_ID",
            security_protocol="SSL",
            ssl_cafile=config.SSL_CAFILE,
            ssl_certfile=config.SSL_CERTFILE,
            ssl_keyfile=config.SSL_KEYFILE,
        )

        consumer(kafka_consumer=client, postgres_client=PostgresClient(conn))
