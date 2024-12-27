FROM python:3.11-slim-bookworm AS base

RUN apt-get update && \
    apt-get install -y gcc build-essential curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY ./requirements.txt .
RUN pip install uv
RUN uv pip install --system -r requirements.txt --no-cache-dir


# Copy the application code
COPY . .
RUN pip install -e .

CMD ["python", "src/main.py"]
