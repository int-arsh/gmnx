FROM python:3.12-slim

# Avoid interactive prompts during apt operations
ENV DEBIAN_FRONTEND=noninteractive

# Create work directory
WORKDIR /app

# Install system updates and any build tools only if needed later (kept minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Copy dependency list and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ask.py /app/ask.py

# Ensure the script is executable
RUN chmod +x /app/ask.py

# Default entrypoint executes the CLI; pass the question as args
ENTRYPOINT ["/usr/local/bin/python", "/app/ask.py"]

