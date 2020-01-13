#!/bin/bash
# this script is used to boot a Postgres Docker container and start serving Flask app

docker pull postgres:12.1
docker run --rm   --name pg-docker -e POSTGRES_PASSWORD=pg#docker -d -p 5432:5432 -v $PWD/pgdata:/var/lib/postgresql/data  postgres

export DATABASE_URI="postgresql+psycopg2://postgres:pg#docker@localhost:5432/mvsimilarity"
export SECRET_KEY="a very very secret key very very well hidden"
export FLASK_DEBUG=1
flask run --host=0.0.0.0
