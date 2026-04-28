#!/bin/bash
# Start the simulation in the background
python3 start_simulation.py &

# Wait for simulation to warm up
sleep 10

# Start the CORS proxy in the foreground (Hugging Face expects this to stay running)
python3 proxy.py
