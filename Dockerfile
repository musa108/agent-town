# STAGE 1: Build the AXL Go binary
FROM golang:1.24-bookworm AS builder

WORKDIR /app
COPY axl-source/ ./axl-source/
WORKDIR /app/axl-source
# Fix dependencies and Build the Linux binary
RUN go mod tidy && go build -o node ./cmd/node

# STAGE 2: Run the Python simulation
FROM python:3.10-slim-bookworm

# Install basic requirements
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy python dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files (including the binary from the builder stage)
COPY . .
COPY --from=builder /app/axl-source/node ./axl-source/node

# Expose the Observer API port (Hugging Face default)
EXPOSE 7860

# Set permissions
RUN chmod +x run.sh

# Start the simulation and proxy
CMD ["./run.sh"]
