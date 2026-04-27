# AXL Agent Town 🏙️

A truly decentralized multi-agent simulation built on the **Gensyn AXL (Agent eXchange Layer)**. 

## 🌟 The Vision
Most "Agent Towns" are centralized simulations running on a single server. **AXL Agent Town** is different. Each agent in this town is a sovereign entity—owning its own AXL node, its own cryptographic identity, and its own communication stack. 

There is no central database. Agents find each other via the AXL spanning tree and communicate peer-to-peer using encrypted TLS tunnels.

## 🚀 Key Features
- **Sovereign Agency**: 1 Agent = 1 Dedicated AXL Node.
- **Mesh Socialization**: Agents autonomously discover peers and engage in P2P gossip across the mesh.
- **P2P Economy**: A simulated credit system where agents "buy" goods and services from each other over AXL, proving value transfer capabilities.
- **Glassmorphism Visualizer**: A premium React dashboard that connects to the mesh as a peer to visualize real-time socialization.
- **Zero-Infrastructure**: Runs entirely on a decentralized mesh; agents can be added to the town dynamically from anywhere in the world.

## 🏗️ Technical Architecture
Unlike typical "centralized" agent towns, our architecture ensures **Sovereign Agency**:
1. **The Agent**: A Python process running an autonomous personality engine.
2. **The Node**: A dedicated **Gensyn AXL Node** providing a private TLS tunnel for the agent.
3. **The Mesh**: A decentralized spanning tree (Yggdrasil-based) connecting nodes without a central server.
4. **The Observer**: A specialized node that acts as a P2P listener to visualize mesh traffic on the dashboard.

## 🛠️ Built With
- **Gensyn AXL**: The backbone for decentralized, encrypted, and peer-to-peer communication.
- **Python**: Powering the autonomous agent logic and personality engines.
- **React + Vite + Canvas**: Delivering a high-aesthetic, high-performance visual dashboard.
- **gVisor**: Providing the Userspace Network Stack for AXL connectivity.

## 🏃 Quick Start
### Prerequisites
- Python 3.10+
- Node.js & npm
- AXL Node Binary (Build provided in `/axl-source`)

### Launch Town
1. **Clone & Install**:
   ```bash
   git clone <your-repo>
   cd gensyn-project
   npm install
   ```
2. **Start Simulation**:
   ```bash
   npm run dev:sim
   ```
3. **Start Dashboard**:
   ```bash
   npm run dev:frontend
   ```
4. **Visit**: `http://localhost:5173`

## 📑 Technical Documentation
- [DIAGNOSTICS](./WALKTHROUGH.md): How we verified P2P mesh connectivity.
- [PARTNER FEEDBACK](./FEEDBACK_AXL.md): Our technical review of the Gensyn AXL stack.
- [AI ATTRIBUTION](./AI_ATTRIBUTION.md): Disclosure of AI-assisted development (Antigravity).
- [PLANNING](./PLANNING.md): Architectural goals and implementation strategy.

---
Built for the **Gensyn AXL Hackathon 2026**.
