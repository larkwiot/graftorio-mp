# Graftorio Multiplayer

Inspired by the original Graftorio and Gratorio2 fork, this mod and docker container provide exporting of production statistics to Grafana via Prometheus.

At this time, this project is a **WORK IN PROGRESS**, so please bear with any issues you find and report them or submit a PR.

This mod is designed and intended for running on a Factorio server.

# Installation

This whole setup utilizes Docker Compose, and a template configuration for it is provided. If you already have a Factorio, Grafana, or Prometheus server, then feel free to remove those parts of the configuration and point everything at your own. If you go that route, I assume you know what you're doing.

First, install Docker Compose. Once you have it, do the following:

```shell
git clone https://github.com/larkwiot/graftorio-mp
cd graftorio-mp

# the network=host is for pip
docker build --network=host -t graftorio-mp:latest .

mkdir -p /opt/docker
cp docker-compose.yml /opt/docker
cd /opt/docker
docker compose up -d
```

Install the mod on your server either by grabbing a release, using your Factorio client, or by cloning and then zipping up this repository (remember to rename the zip appropriately with the version number).

You will also need to configure Prometheus to scrape the exporter. You can do that with a config that looks like this:

```yaml
# /opt/docker/prometheus/conf/prometheus.yml
global:
  scrape_interval: 15s
  scrape_timout: 10s
  evaluation_interval: 1m
  
  query_log_file: /opt/bitname/prometheus/data/prom.log

scrape_configs:
  - job_name: factorio
    static_configs:
      - targets:
          # or whatever port you specified in the docker-compose.yml
          - graftorio-mp:9102
```

Remember to restart Prometheus after changing the config:
```shell
docker compose restart prometheus
```

# How it Works

This setup is made up of two components:
1. A Factorio mod that periodically dumps statistics to a JSON file
2. A Dockerized Python Prometheus Client that reads the JSON when scraped by Prometheus and ships the data back

By default, the data is dumped for every item every 15 seconds to match Prometheus' default scrape interval. You could change that in `control.lua`.
