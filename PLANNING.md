# AXL Agent Town: Decentralized Multi-Agent Simulation

Build a visual, decentralized simulation where multiple AI agents live and interact in a town powered by the AXL (Agent eXchange Layer) peer-to-peer mesh network.

## User Review Required

> [!IMPORTANT]
> To demonstrate "inter-node communication", the application will spin up multiple local AXL nodes on different ports. Each agent will be tied to its own AXL node, simulating a truly decentralized mesh.

> [!NOTE]
> We will use "Ephemeral Identities" for the AXL nodes to bypass the need for OpenSSL (which is not present in the current environment) while still maintaining full P2P functionality.

## Proposed Changes

### [Component] AXL Core
We will clone and build the AXL node from source.

#### [NEW] [axl_setup.py](file:///c:/Users/sysadmin/gensyn-project/axl_setup.py)
A helper script to clone, build, and manage the lifecycle of multiple AXL nodes.

### [Component] Agent Logic
Python-based agents with distinct personalities and goal-oriented behavior.

#### [NEW] [agent.py](file:///c:/Users/sysadmin/gensyn-project/agent.py)
The core agent logic. Each instance:
- Starts its own AXL node.
- Periodically broadcasts its location/status to the "Observer" node.
- Responds to messages from other agents.
- Moves according to its personality (e.g., "The Baker" stays near the bakery).

### [Component] Frontend (Observer)
A high-aesthetic React visualizer to watch the town unfold.

#### [NEW] [frontend/](file:///c:/Users/sysadmin/gensyn-project/frontend/)
- **Vite + React**: Modern, fast frontend.
- **Canvas/Fabric.js**: Visual representation of the town map.
- **AXL Integration**: The frontend will also run an AXL node to receive "Observer" updates from the mesh.

### [Component] Simulation Hub
#### [NEW] [start_simulation.py](file:///c:/Users/sysadmin/gensyn-project/start_simulation.py)
A master script to launch the entire simulation (4-5 agents + Frontend).

---

## Open Questions

- **Agent Personities**: Should I use a remote LLM API (requires key) or rule-based personalities for the demo? 
    - *Proposed*: Rule-based with "Rich Behavior" descriptions to ensure the demo works "out of the box" without external keys.
- **Network Topology**: Since they are all on localhost, we will use sequential ports (9002, 9012, etc.). AXL handles the mesh routing automatically.

## Verification Plan

### Automated Tests
- `python test_axl_msg.py`: A script to verify two AXL nodes can P2P message each other via the HTTP bridge.

### Manual Verification
- Launch `start_simulation.py`.
- Open the browser to the Vite dev server.
- Observe agents moving on the map and social interactions appearing in the "Global Chat/Log".
- Verify via logs that messages are indeed flowing through the `/send` and `/recv` endpoints of different AXL nodes.
