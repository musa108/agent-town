# Walkthrough: AXL Agent Town

A decentralized multi-agent simulation built on **AXL (Agent eXchange Layer)**. Agents own their own nodes and communicate peer-to-peer across a truly decentralized mesh network with zero central infrastructure.

## Project Overview

- **Decentralized Every Level**: Each agent (Alice, Bob, etc.) runs as an independent OS process with its own dedicated AXL Node binary.
- **Mesh Connectivity**: Nodes find each other using AXL's decentralized peer discovery (TLS-over-Yggdrasil).
- **Agent Intelligence**: Agents have autonomous movement and distinct personalities (Grumpy, Cheerful, etc.), and they interact socially over the mesh.
- **Glassmorphism Visualizer**: A modern React-based Observer dashboard that acts as a "peer" in the network to visualize the town's state.

## Core Components

### 1. AXL Infrastructure
I built the AXL node binary from the [Gensyn AXL source](https://github.com/gensyn-ai/axl). The nodes are configured with **unique mesh ports** but **unified virtual TCP ports** (7000) to allow seamless peer-to-peer routing on the same local machine.

### 2. Autonomous Agents
Each [agent.py](file:///c:/Users/sysadmin/gensyn-project/agent.py) instance:
- Registers with its local AXL node.
- Broadcasts its status (coordinates, emoji, state) to the Observer.
- Polls for social chat messages from other agents on the `/recv` endpoint.
- Responds reactively based on its personality.

### 3. Visual Observer (Frontend)
A high-aesthetic dashboard built with **React + Vite**. It connects to its own AXL observer node (`9092`) to "watch" the town. It uses a **Canvas-based map** with vibrant glow effects and grid systems to render real-time agent positions.

### 4. Economic Layer (P2P Payments)
To demonstrate sophisticated inter-node interaction, we implemented a **Credit Protocol**:
- **Stateful Balances**: Each agent maintains a local `balance`.
- **Payment Protocol**: Agents send `type: "payment"` payloads across the mesh to "buy" virtual items (Coffee, Info, Art).
- **Consensus Verification**: The receiving agent verifies the amount and acknowledges the receipt over the mesh.
- **Financial Visualization**: The Observer dashboard renders balances in gold and highlights economic transactions in a dedicated feed.

## How to Run

> [!IMPORTANT]
> The simulation requires **Go** and **Python** (pre-installed in this environment).

1. **Launch Simulation**:
   ```powershell
   cd c:\Users\sysadmin\gensyn-project
   python start_simulation.py
   ```
2. **Access Dashboard**:
   The Vite server is running at `http://localhost:5173`. Open this in your browser to watch the agents interact!

## Verification Results

- **P2P Routing Verified**: I successfully tested message delivery between arbitrary nodes in the mesh (e.g., Node B sending to Node A via `/send` and receiving on `/recv`).
- **Scalability**: The system currently runs 5 AXL nodes simultaneously (4 Agents + 1 Observer) on a single machine with zero port collisions.
- **Resilience**: Agents use AXL's built-in discovery; if a node restarts (using ephemeral keys), the mesh heals automatically.

## Aesthetics Preview

The UI features:
- **Dark Mode**: High-contrast black backgrounds with cyan accents.
- **Glassmorphism**: Translucent panels with backdrop-blur effects.
- **Modern Typography**: Inter and Outfit fonts for a premium "agentic" feel.

---
Built during the Gensyn AXL Hackathon.
