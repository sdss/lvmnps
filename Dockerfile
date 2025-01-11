FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

LABEL org.opencontainers.image.authors="Jose Sanchez-Gallego, gallegoj@uw.edu"
LABEL org.opencontainers.image.source=https://github.com/sdss/lvmnps

WORKDIR /opt

COPY . lvmnps

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

ENV PATH="$PATH:/opt/lvmnps/.venv/bin"

# Sync the project
RUN cd lvmnps && uv sync --frozen --no-cache

ENTRYPOINT ["/opt/lvmnps/.venv/bin/lvmnps", "actor", "start", "--debug"]
