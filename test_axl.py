import subprocess
import time
import requests
import os
import signal
import sys

AXL_BINARY = r"c:\Users\sysadmin\gensyn-project\axl-source\node.exe"

def test_communication():
    # Clear old configs
    for f in ["config-a.json", "config-b.json"]:
        if os.path.exists(f): os.remove(f)

    # 1. Start Node A
    # Virtual tcp_port MUST be the same across the mesh for default routing
    config_a = {
        "api_port": 9002, 
        "tcp_port": 7000, 
        "router_port": 9003,
        "a2a_port": 9004,
        "Listen": ["tls://127.0.0.1:8002"] # Host mesh port
    }
    with open("config-a.json", "w") as f:
        import json
        json.dump(config_a, f)
    
    print("Starting Node A...")
    node_a = subprocess.Popen([AXL_BINARY, "-config", "config-a.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 2. Start Node B
    config_b = {
        "api_port": 9012, 
        "tcp_port": 7000, 
        "router_port": 9013,
        "a2a_port": 9014,
        "Listen": ["tls://127.0.0.1:8012"],
        "Peers": ["tls://127.0.0.1:8002"]
    }
    with open("config-b.json", "w") as f:
        json.dump(config_b, f)
    
    print("Starting Node B...")
    node_b = subprocess.Popen([AXL_BINARY, "-config", "config-b.json"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print("Waiting for nodes to connect (20s)...")
    time.sleep(20)
    
    try:
        # Get Node A's public key
        resp_a = requests.get("http://localhost:9002/topology", timeout=5)
        key_a = resp_a.json().get("our_public_key")
        print(f"Node A Key: {key_a}")
        
        # Get Node B's public key and check if it sees Node A
        resp_b = requests.get("http://localhost:9012/topology", timeout=5)
        data_b = resp_b.json()
        key_b = data_b.get("our_public_key")
        print(f"Node B Key: {key_b}")
        
        # Check if B sees A in tree or peers
        tree = data_b.get("tree", [])
        print(f"Node B Tree size: {len(tree)}")
        
        # Send from B -> A
        print("Sending message from B to A (with retries)...")
        success = False
        for i in range(10):
            try:
                time.sleep(2)
                send_resp = requests.post(
                    "http://localhost:9012/send",
                    headers={"X-Destination-Peer-Id": key_a},
                    data="Hello A! I am B.",
                    timeout=10
                )
                print(f"Send attempt {i+1} status: {send_resp.status_code}")
                if send_resp.status_code == 200:
                    success = True
                    break
            except Exception as e:
                print(f"Send attempt {i+1} failed: {e}")
        
        if success:
            # Recv on A
            print("Receiving on A...")
            recv_resp = requests.get("http://localhost:9002/recv", timeout=12)
            print(f"Recv response: {recv_resp.text}")
            if "Hello A!" in recv_resp.text:
                print("SUCCESS: Message received!")
            else:
                print("FAILURE: Message not received.")
        else:
            print("FAILURE: Could not send message after retries.")
            
    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        print("Cleaning up...")
        node_a.terminate()
        node_b.terminate()

if __name__ == "__main__":
    test_communication()
