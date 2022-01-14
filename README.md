# hellocompose
Multiple docker containers managed by Docker Compose

## Related

- [Connect 2 compose images in docker | Docker](https://www.youtube.com/watch?v=8jVnEZPNom0)

## Notes

- Initially, I had to set up the repo

`python3 -m venv .venv`
`source .venv/bin/activate`
`python -m pip install --upgrade pip`

- And then create Dockerfiles for the ElasticMQ container, ...

- Use the following to up and build:

`docker-compose up --build`

- Which will display something like:

```
elasticmq_1  | 22:07:30.046 [main] INFO  org.elasticmq.server.Main$ - === ElasticMQ server (0.15.8) started in 1727 ms ===
```

- You can issue the following command to check on the containers from the root of the repo:

```
(.venv) allendavidsnook@Lamia hellocompose % docker-compose ps
          Name                        Command               State    Ports
----------------------------------------------------------------------------
hellocompose_elasticmq_1   java -Djava.net.preferIPv4 ...   Up      9324/tcp
```

- And the following to tear it all down:

```
(.venv) allendavidsnook@Lamia hellocompose % docker-compose down
Stopping hellocompose_elasticmq_1 ... done
Removing hellocompose_elasticmq_1 ... done
Removing network hellocompose_default
```

- Remember that things like connection strings should reference the name of the container for the resource.

