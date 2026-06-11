# INTENTIONALLY VULNERABLE - DO NOT USE IN PRODUCTION
# This Dockerfile demonstrates common container anti-patterns
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    curl wget netcat nmap vim nano \
    python3 python3-pip \
    gcc make \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY main.go .

RUN apt-get update && apt-get install -y golang-go \
    && go build -o server main.go

EXPOSE 8080
USER root
CMD ["./server"]
