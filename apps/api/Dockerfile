FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
# Install uv (Astral) and add to PATH
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    echo 'export PATH="/root/.local/bin:$PATH"' >> /root/.profile
ENV PATH="/root/.local/bin:${PATH}"
COPY pyproject.toml ./
RUN uv sync --no-dev
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:${PATH}"
COPY app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


