import os

KAFKA_ADDRESS = os.getenv("KAFKA_ADDRESS")
PG_ADDRESS = os.getenv("PG_ADDRESS")
SSL_CAFILE = "certs/ca.pem"
SSL_CERTFILE = "certs/service.cert"
SSL_KEYFILE = "certs/service.key"


to_check = [
    ("https://www.githubstatus.com/", "All Systems Operational"),
    ("https://api.twitterstat.us/", "All Systems Operational"),
]
