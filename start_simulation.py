import subprocess
import time
import json
import os
import signal
import sys

# Configuration
NUM_AGENTS = 4
BASE_API_PORT = 9002
BASE_TCP_PORT = 7002
GENSYN_PROJECT_DIR = os.getcwd()
AXL_BINARY = os.path.join(GENSYN_PROJECT_DIR, "axl-source", "node.exe" if os.name == 'nt' else "node")

processes = []

def start_axl_node(api_port, mesh_port, config_name, peer_ports=None):
    config = {
        "api_port": api_port,
        "tcp_port": 7000, # Unified virtual port for mesh-wide A2A
        "Listen": [f"tls://127.0.0.1:{mesh_port}"],
        "Peers": []
    }
    if peer_ports:
        for p in peer_ports:
            config["Peers"].append(f"tls://127.0.0.1:{p}")
    
    config_path = os.path.join(GENSYN_PROJECT_DIR, config_name)
    with open(config_path, "w") as f:
        json.dump(config, f)
    
    print(f"[Sim] Starting AXL Node on API port {api_port} (Mesh port {mesh_port})...")
    proc = subprocess.Popen([AXL_BINARY, "-config", config_path], 
                            stdout=subprocess.DEVNULL, 
                            stderr=subprocess.DEVNULL)
    processes.append(proc)
    return proc

def start_agent(name, emoji, axl_port, observer_id=None):
    cmd = [sys.executable, "agent.py", name, emoji, str(axl_port)]
    if observer_id:
        cmd.append(observer_id)
    
    print(f"[Sim] Starting Agent {name} on AXL port {axl_port}...")
    proc = subprocess.Popen(cmd)
    processes.append(proc)
    return proc

def cleanup(sig, frame):
    print("\n[Sim] Cleaning up simulation...")
    for proc in processes:
        proc.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)

def main():
    if not os.path.exists(AXL_BINARY):
        print(f"Error: AXL binary not found at {AXL_BINARY}")
        print("Please wait for the build to complete.")
        return

    # 1. Start Observer AXL node
    obs_api_port = 9092
    obs_mesh_port = 8092
    start_axl_node(obs_api_port, obs_mesh_port, "config-observer.json")
    
    # Wait for observer to get its ID and the mesh to "warm up"
    print("[Sim] Waiting for Observer AXL node to initialize...")
    time.sleep(15)
    
    import requests
    observer_id = None
    try:
        resp = requests.get(f"http://localhost:{obs_api_port}/topology", timeout=5)
        observer_id = resp.json().get("our_public_key")
        print(f"[Sim] Observer ID: {observer_id}")
    except Exception as e:
        print(f"Error: Could not get Observer ID: {e}")
        cleanup(None, None)

    # 2. Start Agents
    agents_data = [
        ("Alice", "👩", 9002, 8002),
        ("Bob", "👨", 9012, 8012),
        ("Charlie", "🤵", 9022, 8022),
        ("Diana", "👩‍⚕️", 9032, 8032)
    ]

    for i, (name, emoji, api_port, mesh_port) in enumerate(agents_data):
        # Every node connects to the observer
        peers = [obs_mesh_port]
        # And let's connect every other node to the previous node to make a chain + hub mesh
        if i > 0:
            peers.append(agents_data[i-1][3])
            
        start_axl_node(api_port, mesh_port, f"config-agent-{i}.json", peer_ports=peers)
        time.sleep(3) 
        start_agent(name, emoji, api_port, observer_id)

    print("\n" + "="*40)
    print("  AXL AGENT TOWN IS NOW VIBRATING")
    print("="*40)
    print("Check your browser at http://localhost:5173 (or 5175)")
    print("Press Ctrl+C to end the simulation.")
    
    try:
        # Keep the simulation alive indefinitely
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Sim] Interrupted by user. Shutting down...")
        cleanup(None, None)
    except Exception as e:
        print(f"\n[Sim] Orchestrator error: {e}")
        cleanup(None, None)

if __name__ == "__main__":
    main()
