FROM python:3.10-slim AS builder

ARG test

COPY pyproject.toml poetry.lock ./

RUN apt-get update \
    && apt-get install curl -y \
    && curl -sSL https://install.python-poetry.org | python3 - --version 1.3.2 \
    && export PATH="$HOME/.local/bin:$PATH" \
    && poetry export --without-hashes \
    $(if [ -n "${test}" ]; then echo --with test; fi)\
    -f requirements.txt -o requirements.txt

FROM python:3.10-slim

WORKDIR /your_salary

COPY --from=builder requirements.txt ./

RUN python -m pip install --no-cache-dir -r ./requirements.txt

COPY . .

CMD uvicorn app_run:app --host 0.0.0.0 --port 8000 --reload
