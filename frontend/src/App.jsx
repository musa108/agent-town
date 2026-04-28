import React, { useState, useEffect, useRef } from 'react';

// Use environment variable for production, fallback to proxy for local dev
const OBSERVER_API = import.meta.env.VITE_AXL_API_URL || '/axl';

const AgentTown = () => {
  const [agents, setAgents] = useState({});
  const [logs, setLogs] = useState([]);
  const canvasRef = useRef(null);

  // Poll logic update for social bubbles
  useEffect(() => {
    const pollInterval = setInterval(async () => {
      try {
        const response = await fetch(`${OBSERVER_API}/recv`, { cache: 'no-store' });
        if (response.status === 200) {
          const text = await response.text();
          if (!text) return;
          try {
            const data = JSON.parse(text);
            console.log("Mesh Data Received:", data);
            
            if (data.type === 'status_update') {
              setAgents(prev => ({
                ...prev,
                [data.agent.id]: { ...data.agent, lastUpdate: Date.now() }
              }));
            } else if (data.type === 'chat' || data.type === 'payment') {
              // Social & Economic Feed
              const isPayment = data.type === 'payment';
              const content = isPayment 
                ? `Paid ${data.amount} AXL for ${data.item}`
                : data.content;

              setLogs(prev => [{
                id: Date.now(),
                from: data.from,
                content: content,
                isPayment: isPayment,
                timestamp: new Date().toLocaleTimeString()
              }, ...prev].slice(0, 50));

              // Speech Bubble Logic
              setAgents(prev => {
                const next = { ...prev };
                Object.keys(next).forEach(id => {
                  if (next[id].name === data.from) {
                    next[id].message = content;
                    next[id].msgTime = Date.now();
                  }
                });
                return next;
              });
            }
          } catch (e) {
            console.warn("Malformed mesh packet:", text, e);
          }
        }
      } catch {
        /* Ignore connection timeouts during polling */
      }
    }, 800);
    return () => clearInterval(pollInterval);
  }, []);

  // Cleanup inactive agents (stale for 15s)
  useEffect(() => {
    const cleanup = setInterval(() => {
      const now = Date.now();
      setAgents(prev => {
        const next = { ...prev };
        let changed = false;
        Object.keys(next).forEach(id => {
          if (now - next[id].lastUpdate > 15000) {
            delete next[id];
            changed = true;
          }
        });
        return changed ? next : prev;
      });
    }, 5000);
    return () => clearInterval(cleanup);
  }, []);

  // Canvas Rendering (Upgraded for "Wow" factor)
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    
    const render = () => {
      const w = canvas.width;
      const h = canvas.height;
      ctx.clearRect(0, 0, w, h);
      
      // Draw Tech Grid
      ctx.strokeStyle = 'rgba(0, 242, 255, 0.03)';
      ctx.lineWidth = 1;
      for(let x=0; x<w; x+=40) { ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,h); ctx.stroke(); }
      for(let y=0; y<h; y+=40) { ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(w,y); ctx.stroke(); }

      const agentList = Object.values(agents);

      // Draw Agent Entities
      agentList.forEach(agent => {
        const x = agent.x * w;
        const y = agent.y * h;
        const isMuted = Date.now() - agent.lastUpdate > 8000;
        
        ctx.save();
        ctx.globalAlpha = isMuted ? 0.3 : 1;

        // Shadow/Glow
        ctx.shadowBlur = 20;
        ctx.shadowColor = 'rgba(0, 242, 255, 0.5)';
        
        // Agent Icon
        ctx.font = '36px serif';
        ctx.fillText(agent.emoji, x - 18, y + 10);

        // Name & Personality
        ctx.shadowBlur = 0;
        ctx.font = 'bold 12px Inter';
        ctx.fillStyle = '#fff';
        ctx.textAlign = 'center';
        ctx.fillText(agent.name.toUpperCase(), x, y + 35);
        ctx.fillStyle = 'var(--accent-color)';
        ctx.font = '9px Inter';
        ctx.fillText(agent.personality, x, y + 46);

        // Balance Display
        ctx.fillStyle = '#FFD700'; // Gold color for balance
        ctx.font = 'bold 10px Inter';
        ctx.fillText(`${agent.balance || 0} AXL`, x, y + 58);

        // Speech Bubble
        if (agent.message && Date.now() - agent.msgTime < 4000) {
          const padding = 10;
          ctx.font = '11px Inter';
          const textWidth = ctx.measureText(agent.message).width;
          
          ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
          ctx.beginPath();
          ctx.roundRect(x - (textWidth/2) - padding, y - 60, textWidth + (padding*2), 24, 8);
          ctx.fill();
          
          ctx.fillStyle = '#000';
          ctx.fillText(agent.message, x, y - 44);
        }

        ctx.restore();
      });

      requestAnimationFrame(render);
    };

    const handleResize = () => {
      canvas.width = canvas.parentElement.clientWidth;
      canvas.height = canvas.parentElement.clientHeight;
    };
    window.addEventListener('resize', handleResize);
    handleResize();
    const frame = requestAnimationFrame(render);
    return () => { window.removeEventListener('resize', handleResize); cancelAnimationFrame(frame); };
  }, [agents]);

  return (
    <div className="app-container">
      <div className="sidebar glass">
        <div>
          <h1 style={{ fontFamily: 'Outfit', fontSize: '2rem', marginBottom: '0.5rem', background: 'linear-gradient(45deg, #00f2ff, #7000ff)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
            AXL Agent Town
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            A sovereign multi-agent mesh powered by Gensyn AXL.
          </p>
        </div>

        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '15px', overflow: 'hidden' }}>
          <h3 style={{ fontSize: '1rem', color: 'var(--accent-color)', textTransform: 'uppercase', letterSpacing: '1px' }}>Town Activity</h3>
          <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '10px', paddingRight: '10px' }}>
            {logs.length === 0 ? (
              <p style={{ color: 'var(--text-secondary)', fontStyle: 'italic', fontSize: '0.85rem' }}>Waiting for mesh...</p>
            ) : (
              logs.map(log => (
                <div key={log.id} className="glass" style={{ padding: '10px', fontSize: '0.85rem', borderLeft: log.isPayment ? '3px solid #ffd700' : '1px solid var(--glass-border)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                    <span style={{ fontWeight: '600', color: log.isPayment ? '#ffd700' : 'var(--accent-color)' }}>{log.from}</span>
                    <span style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>{log.timestamp}</span>
                  </div>
                  <p style={{ color: '#eee', lineHeight: '1.4' }}>{log.content}</p>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="glass" style={{ padding: '15px', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
          <strong>P2P Mesh Status:</strong><br />
          {Object.keys(agents).length} Active Autonomous Peers
        </div>
      </div>

      <div className="map-view glass">
        <canvas ref={canvasRef} style={{ width: '100%', height: '100%', display: 'block' }} />
        <div style={{ position: 'absolute', bottom: '20px', right: '20px', fontSize: '10px', opacity: 0.5 }}>
          AXL Node: {OBSERVER_API}
        </div>
      </div>
    </div>
  );
};

export default AgentTown;
