import requests
import time
import json
import random
import sys
import threading

class Agent:
    def __init__(self, name, emoji, personality, axl_port, observer_id=None):
        self.name = name
        self.emoji = emoji
        self.personality = personality
        self.axl_port = axl_port
        self.axl_url = f"http://localhost:{axl_port}"
        self.observer_id = observer_id
        self.x = random.random()
        self.y = random.random()
        self.node_id = None
        self.balance = 100 # Initial AXL Credits
        self.transactions = []
        self.running = True

    def get_node_id(self):
        try:
            response = requests.get(f"{self.axl_url}/topology", timeout=2)
            if response.status_code == 200:
                self.node_id = response.json().get("our_public_key")
                print(f"[{self.name}] Started with node ID: {self.node_id}")
                return True
        except Exception as e:
            print(f"[{self.name}] Error connecting to AXL node: {e}")
        return False

    def report_status(self):
        """Send current state to the observer node."""
        if not self.observer_id:
            return
            
        payload = {
            "type": "status_update",
            "agent": {
                "name": self.name,
                "emoji": self.emoji,
                "personality": self.personality,
                "x": self.x,
                "y": self.y,
                "id": self.node_id,
                "balance": self.balance
            }
        }
        try:
            requests.post(
                f"{self.axl_url}/send",
                headers={"X-Destination-Peer-Id": self.observer_id},
                data=json.dumps(payload),
                timeout=2
            )
        except:
            pass

    def socialize(self):
        """Find other agents in the mesh and send them a message."""
        try:
            resp = requests.get(f"{self.axl_url}/topology", timeout=2)
            nodes = resp.json().get("tree", [])
            # Filter for peers that aren't us or the observer
            peers = [n["public_key"] for n in nodes if n["public_key"] not in [self.node_id, self.observer_id]]
            
            if peers:
                target = random.choice(peers)
                messages = [
                    f"Hello! I'm feeling very {self.personality} today.",
                    "Have you seen the gardener?",
                    "The mesh is feeling quite strong today, don't you think?",
                    "I'm considering moving to the coordinates (0.5, 0.5).",
                    "Decentralization is the future!"
                ]
                msg_content = random.choice(messages)
                
                chat_payload = {
                    "type": "chat",
                    "from": self.name,
                    "content": msg_content
                }
                
                # Send to target
                requests.post(
                    f"{self.axl_url}/send",
                    headers={"X-Destination-Peer-Id": target},
                    data=json.dumps(chat_payload),
                    timeout=2
                )
                
                # CC the observer so the user can see the gossip
                if self.observer_id:
                    requests.post(
                        f"{self.axl_url}/send",
                        headers={"X-Destination-Peer-Id": self.observer_id},
                        data=json.dumps(chat_payload),
                        timeout=2
                    )
        except:
            pass

    def economic_interaction(self):
        """Simulate a P2P economic transaction across the mesh."""
        try:
            resp = requests.get(f"{self.axl_url}/topology", timeout=2)
            nodes = resp.json().get("tree", [])
            peers = [n["public_key"] for n in nodes if n["public_key"] not in [self.node_id, self.observer_id]]
            
            if peers and self.balance > 10:
                target = random.choice(peers)
                amount = random.randint(5, 15)
                items = ["Coffee ☕", "Information 📜", "Mesh-Key 🔑", "Digital Art 🎨", "Protection 🛡️"]
                item = random.choice(items)
                
                payment_payload = {
                    "type": "payment",
                    "from": self.name,
                    "amount": amount,
                    "item": item
                }
                
                # Execute payment
                self.balance -= amount
                requests.post(
                    f"{self.axl_url}/send",
                    headers={"X-Destination-Peer-Id": target},
                    data=json.dumps(payment_payload),
                    timeout=2
                )
                
                # CC the observer for visualization
                if self.observer_id:
                    requests.post(
                        f"{self.axl_url}/send",
                        headers={"X-Destination-Peer-Id": self.observer_id},
                        data=json.dumps(payment_payload),
                        timeout=2
                    )
                print(f"[{self.name}] Paid {amount} AXL to {target[:8]}... for {item}")
        except:
            pass

    def think_and_act(self):
        """Autonomous behavior loop."""
        # 1. Random movement
        self.x = max(0, min(1, self.x + random.uniform(-0.05, 0.05)))
        self.y = max(0, min(1, self.y + random.uniform(-0.05, 0.05)))
        
        # 2. Occasional socializing
        if random.random() < 0.2:
            self.socialize()
            
        # 3. Occasional economic activity
        if random.random() < 0.15:
            self.economic_interaction()
            
        # 4. Report to observer
        self.report_status()

    def send_message(self, target_id, content):
        payload = {
            "type": "chat",
            "from": self.name,
            "content": content
        }
        try:
            requests.post(
                f"{self.axl_url}/send",
                headers={"X-Destination-Peer-Id": target_id},
                data=json.dumps(payload),
                timeout=2
            )
        except Exception as e:
            print(f"[{self.name}] Failed to send message to {target_id}: {e}")

    def poll_messages(self):
        while self.running:
            try:
                # In AXL, /recv is usually a blocking call or returns immediately if nothing
                response = requests.get(f"{self.axl_url}/recv", timeout=5)
                if response.status_code == 200 and response.text.strip():
                    sender_id = response.headers.get("X-From-Peer-Id")
                    data = response.json()
                    print(f"[{self.name}] Received from {sender_id}: {data}")
                    self.handle_message(sender_id, data)
            except requests.exceptions.Timeout:
                pass
            except Exception as e:
                # print(f"[{self.name}] Poll error: {e}")
                time.sleep(1)
            time.sleep(0.5)

    def handle_message(self, sender_id, data):
        if data.get("type") == "chat":
            # Simple reactive logic: if someone chats, maybe say hi back occasionally
            if random.random() < 0.3:
                response_txt = f"Hi {data.get('from')}! I am {self.name}, and I'm currently feeling {self.personality}."
                self.send_message(sender_id, response_txt)
        
        elif data.get("type") == "payment":
            amount = data.get("amount", 0)
            item = data.get("item", "service")
            self.balance += amount
            print(f"[{self.name}] Received {amount} AXL from {data.get('from')} for {item}")
            
            # Thank them
            response_txt = f"Thanks for the {item}, {data.get('from')}! Payment of {amount} AXL received."
            self.send_message(sender_id, response_txt)

    def move(self):
        # Brownian motion or personality-based movement
        step = 0.02
        self.x = max(0, min(1, self.x + random.uniform(-step, step)))
        self.y = max(0, min(1, self.y + random.uniform(-step, step)))

    def run(self):
        # Start message polling in a separate thread
        threading.Thread(target=self.poll_messages, daemon=True).start()
        
        print(f"[{self.name}] Agent loop starting...")
        while self.running:
            self.think_and_act()
            time.sleep(3) # Lively town tick

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python agent.py <name> <emoji> <axl_port> [observer_id]")
        sys.exit(1)
    
    agent_name = sys.argv[1]
    agent_emoji = sys.argv[2]
    port = int(sys.argv[3])
    obs_id = sys.argv[4] if len(sys.argv) > 4 else None
    
    # Simple personalities based on names or random
    personalities = ["happy", "grumpy", "anxious", "excited", "sleepy", "mysterious"]
    personality = random.choice(personalities)
    
    agent = Agent(agent_name, agent_emoji, personality, port, obs_id)
    
    # Wait for AXL node to be ready
    print(f"[{agent_name}] Waiting for AXL node on port {port}...")
    attempts = 0
    while not agent.get_node_id() and attempts < 30:
        time.sleep(2)
        attempts += 1
    
    if agent.node_id:
        agent.run()
    else:
        print(f"[{agent_name}] Failed to connect to AXL node. Exiting.")
