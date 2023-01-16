# Website Checker

This tool monitors website availability, sending healthcheck data to a Kafka stream and storing them in a Postgres database after reading them from a Kafka consumer.


## Requirements

First of all, you need:
- a running Kafka instance
- a running Postgres instance

The service assumes that a `websitechecker` topic has been set up in Kafka.

In your .envrc (with [direnv](https://direnv.net/)):
```
export PG_ADDRESS=<your postgres connection string>
export KAFKA_ADDRESS=<your kafka connection string>
```

Create a `certs` folder:
```
mkdir certs
```

The following certificates for Kafka need to be placed in the `certs` folder:
- ca.pem
- service.cert
- service.key


## Database setup

A table needs to be create in the Postgres database. You can do so by running this script locally (see next section for the setup)
```
python websitechecker/migration.py
```
or with Docker
```
docker run \
    -e PG_ADDRESS=${PG_ADDRESS} \
    -v certs:/app/certs \
    websitechecker:latest python websitechecker/migration.py
```


## Try it out in your local environment

Poetry needs to be installed on your machine in order to run the code locally without Docker.

To install
```
poetry install
```

To run tests
```
poetry run pytest
```

Run the producer
```
python websitechecker/main.py producer
```

Run the consumer
```
python websitechecker/main.py consumer
```


## Run with Docker

Build the image

```
docker build -t websitechecker .
```

To run from two separate containers, you need to mount the `certs` directory as a volume
```
docker run \
    -e KAFKA_ADDRESS=${KAFKA_ADDRESS} \
    -e PG_ADDRESS=${PG_ADDRESS} \
    -v certs:/app/certs \
    websitechecker:latest python websitechecker/main.py <producer or consumer>
```
or more simply
```
docker-compose up
```


## Remarks

This is a coding challenge done for a job interview. All references to the company I interviewed with have been removed, as per company's request. Many thanks to this company for letting me publish this code!
