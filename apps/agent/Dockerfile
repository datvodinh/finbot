FROM python:3.11-slim-bookworm AS base

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc build-essential libevent-2.1-7t64 libavif16 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY ./requirements.txt .
RUN pip install uv
RUN uv pip install --system -r requirements.txt --no-cache-dir
RUN playwright install


# Copy the application code
COPY . .
RUN pip install -e .

EXPOSE 7860

CMD ["python", "src/main.py"]
