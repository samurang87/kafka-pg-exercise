from test.stubs import FakeKafkaClient, FakePostgresClient

import pytest
import responses


@pytest.fixture
def kafka():
    return FakeKafkaClient(topic="websitechecker")


@pytest.fixture
def url():
    return "https://www.githubstatus.com/"


@pytest.fixture
def response(url):
    return responses.Response(
        method="GET", url=url, json="All Systems Operational most likely"
    )


@pytest.fixture
def response_list():
    return [
        responses.Response(
            method="GET",
            url="https://www.githubstatus.com/",
            json="All Systems Operational most likely",
        ),
        responses.Response(
            method="GET",
            url="https://api.twitterstat.us/",
            json="All Systems Operational most likely",
        ),
    ]


@pytest.fixture
def postgres():
    return FakePostgresClient()
