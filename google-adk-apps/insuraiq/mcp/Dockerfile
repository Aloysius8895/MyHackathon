FROM ghcr.io/astral-sh/uv:bookworm

ADD . /app

WORKDIR /app
RUN uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uv", "run", "main.py"]