# Use a base image with both Python and Go
FROM nikolaik/python-nodejs:python3.10-nodejs18

# Install Go
USER root
RUN apt-get update && apt-get install -y golang-go

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Build the AXL binary for Linux
RUN cd axl-source && go build -o node .

# Expose the Observer API port (Hugging Face default is 7860)
EXPOSE 7860

# Set permissions for the startup script
RUN chmod +x run.sh

# Command to run the simulation and proxy
CMD ["./run.sh"]
