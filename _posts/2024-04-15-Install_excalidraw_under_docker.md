---
layout:     post
title:      "Install excalidraw under docker"
subtitle:   "Install excalidraw under docker"
date:       2024-04-15
author:     "Gavin Wang"
catalog:    true
img: "/img/docker/docker2.jpg"
summary: Install excalidraw under docker
categories:
    - [excalidraw]
    - [Docker]
tags:
    - excalidraw
    - Docker
---

# Overview

Install excalidraw under docker.


# 

# Install Excalidraw using Docker

Now that Docker is installed, you can pull the Excalidraw Docker image and run it as a container.

`docker pull docker.io/excalidraw/excalidraw:latest`

Run the Excalidraw container in detached mode (-d) and map port 8080 on your host to port 80 on the container using the following command:

docker run -p 8080:80 -d docker.io/excalidraw/excalidraw:latest


# Check excalidraw service

```shell
root@Service:~# docker ps -a
CONTAINER ID   IMAGE                          COMMAND                  CREATED              STATUS                        PORTS                                   NAMES
abe9fa359013   excalidraw/excalidraw:latest   "/docker-entrypoint.…"   About a minute ago   Up About a minute (healthy)   0.0.0.0:8080->80/tcp, :::8080->80/tcp   keen_pasteur
085bdc5ed931   redis:alpine                   "docker-entrypoint.s…"   4 days ago           Exited (0) 2 days ago                                                 composetest-redis-1
32c88ec9f1f6   composetest-web                "flask run"              4 days ago           Exited (1) 4 days ago                                                 composetest-web-1
45b89e827bc5   ubuntu                         "/bin/bash"              4 days ago           Exited (137) 2 hours ago                                              heuristic_feistel
ca0493c84c48   dokken/centos-8                "/bin/bash"              4 days ago           Exited (0) 4 days ago                                                 quizzical_hodgkin
root@Service:~#
```

CONTAINER ID of `abe9fa359013` which status is 'UP' and healthy.

# Access Excalidraw

Now that Excalidraw is running as a Docker container, you can access it through a web browser by navigating to http://your_vps_ip:8080.

`http://your_vps_ip:8080`

Replace your_vps_ip with the actual IP address of your VPS.


# Previews

<img class="shadow" src="/img/in-post/excalidraw.png" width="600">

