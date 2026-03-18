'use client';
import React from 'react';
import { apiIngest, apiMetrics, apiHealth } from '@/lib/api';

export default function AdminPanel() {
  const [metrics, setMetrics] = React.useState<any>(null);
  const [busy, setBusy] = React.useState(false);
  const [health, setHealth] = React.useState<string|null>(null);
  const checkHealth = async () => {
    setHealth('Checking...');
    try {
      const h = await apiHealth();
      setHealth(h.status === 'ok' ? 'Healthy' : JSON.stringify(h));
    } catch (e) {
      setHealth('Unhealthy');
    }
  };

  const refresh = async () => {
    const m = await apiMetrics();
    setMetrics(m);
  };

  const ingest = async () => {
    setBusy(true);
    try {
      await apiIngest();
      await refresh();
    } finally {
      setBusy(false);
    }
  };

  React.useEffect(() => { refresh(); }, []);

  return (
    <div className="card">
      <h2>Admin</h2>
      <div style={{display:'flex', gap:8, marginBottom:8}}>
        <button onClick={ingest} disabled={busy} style={{padding:'8px 12px', borderRadius:8, border:'1px solid #111', background:'#fff'}}>
          {busy ? 'Indexing...' : 'Ingest sample docs'}
        </button>
        <button onClick={refresh} style={{padding:'8px 12px', borderRadius:8, border:'1px solid #111', background:'#fff'}}>Refresh metrics</button>
        <button onClick={checkHealth} style={{padding:'8px 12px', borderRadius:8, border:'1px solid #111', background:'#fff'}}>Health check</button>
      </div>
      {health && (
        <div style={{marginBottom:8}}>
          <b>Health:</b> {health}
        </div>
      )}
      {metrics && (
        <div className="code">
          <pre>{JSON.stringify(metrics, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
