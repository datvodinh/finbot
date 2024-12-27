FROM python:3.11-slim-bookworm AS base

RUN apt-get update && \
    apt-get install -y gcc build-essential curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY ./requirements.txt .
RUN pip3 install uv
RUN uv pip install --system -r requirements.txt --no-cache-dir

# Copy the application code
COPY . .

CMD ["python", "src/main.py"]
