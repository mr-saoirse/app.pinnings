# this docker image is for the main service that does some things with K8s outside of the normal stuffFROM python:3.10-slim as base
FROM python:3.10-slim as base
RUN apt update && apt install -y curl gpg
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg;
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null;
RUN apt install -y git gh
RUN pip install -U pip poetry

WORKDIR /app

COPY pyproject.toml ./
RUN poetry install --no-dev --no-root --no-interaction --no-ansi

COPY ./apin /app/apin
COPY ./README.md /app/README.md
RUN poetry build
RUN poetry install

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PYTHONUNBUFFERED=0

ENTRYPOINT [ "poetry", "run", "apin", "scheduler", "start"  ]
#docker build --platform linux/amd64 -t monologue:latest . 
#docker run  --platform linux/amd64 -t monologue

#https://github.com/pola-rs/polars/issues/540


##aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 286292902993.dkr.ecr.us-east-1.amazonaws.com
#docker build --pull --rm -f "Dockerfile" -t infra-test:apin-latest --platform linux/amd64 . 
#docker tag infra-test:apin-latest 286292902993.dkr.ecr.us-east-1.amazonaws.com/infra-test:apin-latest & docker push 286292902993.dkr.ecr.us-east-1.amazonaws.com/infra-test:apin-latest
