#!/bin/bash
# Install Go (if not present) and build the AXL binary for Linux
echo "Installing dependencies and building AXL node..."
pip install -r requirements.txt

# Navigate to AXL source and build
cd axl-source
if [ ! -f "node" ]; then
    echo "Building AXL binary..."
    go build -o node .
fi
cd ..

echo "Cloud setup complete."
