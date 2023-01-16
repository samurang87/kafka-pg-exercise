import responses

from websitechecker.healthchecker import Health, healthcheck


@responses.activate
def test_healthchecker_happy_case(response, url):

    responses.add(response)

    want = Health(
        timestamp=1673023382577, status_code=200, time_elapsed=50, pattern_found=True
    )

    got = healthcheck(
        url=url, match="All Systems Operational"
    )

    assert want.status_code == got.status_code
    assert got.pattern_found == got.pattern_found


@responses.activate
def test_healthchecker_no_match(response, url):

    responses.add(response)

    want = Health(
        timestamp=1673023382577, status_code=200, time_elapsed=50, pattern_found=False
    )

    got = healthcheck(url=url, match="Wrong Text")

    assert want.status_code == got.status_code
    assert got.pattern_found == got.pattern_found
