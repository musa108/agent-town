# Partner Feedback: Gensyn AXL 🚀

**Project**: AXL Agent Town  
**Developer**: Antigravity (AI) & Human Partner

## 🟢 The Good
- **Zero-Config Encryption**: The fact that nodes establish TLS tunnels without manual certificate management is a huge win for decentralized applications.
- **P2P Discovery**: The spanning tree discovery worked flawlessly on localhost once the initial peers were connected.
- **HTTP Bridge**: The `/send` and `/recv` bridge makes it incredibly easy to integrate with non-Go languages like Python and React.

## 🟡 The Challenges
### 1. Networking Stack (gVisor/TUN)
- **Issue**: Running AXL on Windows/VSCode environments often requires specific Userspace Network configurations (gVisor).
- **Feedback**: A "Local Dev Mode" that falls back to standard TCP for local testing (without TUN/TAP) would drastically lower the barrier for hackathon participants.

### 2. Local Port Management
- **Issue**: Running multiple nodes on one machine required careful orchestration of unique mesh ports and virtual ports.
- **Feedback**: An automated port-assignment flag (e.g., `--auto-port`) would simplify multi-agent simulations.

### 3. Ephemeral Identities
- **Issue**: We used ephemeral keys to simplify the build, but this makes peer discovery less "sticky" across restarts.
- **Feedback**: A lightweight `axl-keytool` to generate and manage persistent identities for local dev would be helpful.

## 🔴 Feature Requests
- **WebSocket Support**: Currently, we have to poll `/recv` from the browser. Native WebSocket support on the HTTP bridge would enable much smoother real-time dashboards.
- **Pub/Sub Primitives**: Implementing a gossip-based Pub/Sub (e.g., agents subscribing to `#town-square`) would reduce the need for manual CC-ing of the Observer node.
- **Error Diagnostics**: More structured error codes (e.g., `AXL-E101: Handshake Timeout`) would make debugging distributed networks much faster.

---
*Submitted as part of the Gensyn AXL Hackathon 2026.*
