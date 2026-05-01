import { useEffect, useState } from 'react';
import { Shield, ShieldAlert, Activity, Cpu } from 'lucide-react';

function App() {
  const [stats, setStats] = useState({ total_packets: 0, total_alerts: 0, active_threats: 0 });
  const [alerts, setAlerts] = useState([]);
  const [traffic, setTraffic] = useState([]);

  useEffect(() => {
    const fetchData = () => {
      fetch('http://localhost:8000/api/stats')
        .then(res => res.json())
        .then(data => setStats(data))
        .catch(console.error);
        
      fetch('http://localhost:8000/api/alerts?limit=10')
        .then(res => res.json())
        .then(data => setAlerts(data))
        .catch(console.error);

      fetch('http://localhost:8000/api/traffic?limit=10')
        .then(res => res.json())
        .then(data => setTraffic(data))
        .catch(console.error);
    };

    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex items-center justify-between border-b border-slate-700 pb-6">
          <div className="flex items-center space-x-3">
            <ShieldAlert className="w-10 h-10 text-red-500" />
            <div>
              <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-red-500 to-orange-400">
                Nexus Security
              </h1>
              <p className="text-slate-400 text-sm">Hybrid IDS/IPS Dashboard</p>
            </div>
          </div>
          <div className="flex items-center space-x-2 text-sm">
            <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-green-400 font-medium">System Active</span>
          </div>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 flex items-center shadow-lg">
            <Activity className="w-12 h-12 text-blue-400 mr-4" />
            <div>
              <p className="text-slate-400 text-sm uppercase tracking-wider">Packets Analyzed</p>
              <p className="text-3xl font-bold">{stats.total_packets.toLocaleString()}</p>
            </div>
          </div>
          
          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 flex items-center shadow-lg">
            <Shield className="w-12 h-12 text-yellow-400 mr-4" />
            <div>
              <p className="text-slate-400 text-sm uppercase tracking-wider">Total Alerts</p>
              <p className="text-3xl font-bold">{stats.total_alerts.toLocaleString()}</p>
            </div>
          </div>

          <div className="bg-slate-800 p-6 rounded-xl border border-red-900/50 flex items-center shadow-lg shadow-red-900/20">
            <Cpu className="w-12 h-12 text-red-500 mr-4" />
            <div>
              <p className="text-red-400 text-sm uppercase tracking-wider">Active Threats</p>
              <p className="text-3xl font-bold text-red-500">{stats.active_threats}</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Threats Table */}
          <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
            <div className="p-4 border-b border-slate-700 bg-slate-800/50">
              <h2 className="text-xl font-semibold text-red-400 flex items-center">
                <ShieldAlert className="w-5 h-5 mr-2" /> Recent Threats
              </h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-900/50 text-slate-400">
                  <tr>
                    <th className="p-4">Time</th>
                    <th className="p-4">Source</th>
                    <th className="p-4">Type</th>
                    <th className="p-4">Severity</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700">
                  {alerts.map((alert) => (
                    <tr key={alert.id} className="hover:bg-slate-700/50 transition-colors">
                      <td className="p-4 text-slate-300">{new Date(alert.timestamp).toLocaleTimeString()}</td>
                      <td className="p-4 font-mono text-xs">{alert.src_ip}</td>
                      <td className="p-4">{alert.threat_type}</td>
                      <td className="p-4">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                          alert.severity === 'HIGH' ? 'bg-red-500/20 text-red-400 border border-red-500/30' :
                          alert.severity === 'MEDIUM' ? 'bg-yellow-500/20 text-yellow-400 border border-yellow-500/30' :
                          'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                        }`}>
                          {alert.severity}
                        </span>
                      </td>
                    </tr>
                  ))}
                  {alerts.length === 0 && (
                    <tr>
                      <td colSpan="4" className="p-8 text-center text-slate-500">No recent threats detected.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          {/* Traffic Table */}
          <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
            <div className="p-4 border-b border-slate-700 bg-slate-800/50">
              <h2 className="text-xl font-semibold text-blue-400 flex items-center">
                <Activity className="w-5 h-5 mr-2" /> Live Traffic Feed
              </h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-900/50 text-slate-400">
                  <tr>
                    <th className="p-4">Time</th>
                    <th className="p-4">Source</th>
                    <th className="p-4">Dest</th>
                    <th className="p-4">Proto</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700">
                  {traffic.map((pkt) => (
                    <tr key={pkt.id} className="hover:bg-slate-700/50 transition-colors">
                      <td className="p-4 text-slate-400">{new Date(pkt.timestamp).toLocaleTimeString()}</td>
                      <td className="p-4 font-mono text-xs text-slate-300">{pkt.src_ip}:{pkt.src_port}</td>
                      <td className="p-4 font-mono text-xs text-slate-300">{pkt.dst_ip}:{pkt.dst_port}</td>
                      <td className="p-4">
                        <span className="px-2 py-1 rounded bg-slate-700 text-slate-300 text-xs font-semibold">
                          {pkt.protocol}
                        </span>
                      </td>
                    </tr>
                  ))}
                  {traffic.length === 0 && (
                    <tr>
                      <td colSpan="4" className="p-8 text-center text-slate-500">No traffic captured yet.</td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;
