from unittest.mock import patch

import responses

from websitechecker.main import producer


@patch("websitechecker.main.sleep")
@responses.activate
def test_producer_happy_case(kafka, response_list):

    for item in response_list:
        responses.add(item)

    producer(kafka_producer=kafka, n_iterations=2)

    assert kafka.n_messages_were_sent(topic="websitechecker", n_messages=4)
