import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { 
  ShieldCheck, 
  TrendingUp,
  AlertTriangle,
  CheckCircle2
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, Cell, ReferenceLine
} from 'recharts';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { Download, SlidersHorizontal, Cpu } from 'lucide-react';

const API_URL = "https://verilift-1.onrender.com/api"; 

// -----------------------------------------------------------------------------
// Global Shader Background
// -----------------------------------------------------------------------------
function BackgroundShader() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    function syncSize() {
      const w = window.innerWidth;
      const h = window.innerHeight;
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w;
        canvas.height = h;
      }
    }
    window.addEventListener('resize', syncSize);
    syncSize();

    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
    if (!gl) return;
    
    const vs = `attribute vec2 a_position;
    varying vec2 v_texCoord;
    void main() {
      v_texCoord = a_position * 0.5 + 0.5;
      gl_Position = vec4(a_position, 0.0, 1.0);
    }`;
    
    const fs = `precision highp float;
    uniform float u_time;
    uniform vec2 u_resolution;
    varying vec2 v_texCoord;

    void main() {
        vec2 uv = v_texCoord;
        vec2 p = (gl_FragCoord.xy * 2.0 - u_resolution.xy) / min(u_resolution.x, u_resolution.y);
        
        float t = u_time * 0.1; // Slowed down for global background
        for(float i = 1.0; i < 4.0; i++){
            p.x += 0.3 / i * sin(i * 3.0 * p.y + t);
            p.y += 0.3 / i * cos(i * 3.0 * p.x + t);
        }
        
        // Deep slate to Indigo/Sky professional glow
        vec3 color1 = vec3(0.01, 0.02, 0.06); 
        vec3 color2 = vec3(0.28, 0.3, 0.84); // Slightly darker indigo
        
        float mask = sin(p.x + p.y + t) * 0.5 + 0.5;
        vec3 finalColor = mix(color1, color2 * 0.15, mask);
        
        float noise = fract(sin(dot(uv, vec2(12.9898, 78.233))) * 43758.5453);
        finalColor += noise * 0.02;

        gl_FragColor = vec4(finalColor, 1.0);
    }`;
    
    function cs(type, src) {
      const s = gl.createShader(type);
      gl.shaderSource(s, src);
      gl.compileShader(s);
      return s;
    }
    
    const prog = gl.createProgram();
    gl.attachShader(prog, cs(gl.VERTEX_SHADER, vs));
    gl.attachShader(prog, cs(gl.FRAGMENT_SHADER, fs));
    gl.linkProgram(prog);
    gl.useProgram(prog);
    
    const buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, 1,1]), gl.STATIC_DRAW);
    
    const pos = gl.getAttribLocation(prog, 'a_position');
    gl.enableVertexAttribArray(pos);
    gl.vertexAttribPointer(pos, 2, gl.FLOAT, false, 0, 0);
    
    const uTime = gl.getUniformLocation(prog, 'u_time');
    const uRes = gl.getUniformLocation(prog, 'u_resolution');

    let animationFrameId;
    function render(t) {
      gl.viewport(0, 0, canvas.width, canvas.height);
      if (uTime) gl.uniform1f(uTime, t * 0.001);
      if (uRes) gl.uniform2f(uRes, canvas.width, canvas.height);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      animationFrameId = requestAnimationFrame(render);
    }
    render(0);

    return () => {
      window.removeEventListener('resize', syncSize);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <div className="fixed inset-0 z-0 bg-slate-950">
      <canvas ref={canvasRef} className="block w-full h-full opacity-80"></canvas>
    </div>
  );
}

// -----------------------------------------------------------------------------
// Main App Component
// -----------------------------------------------------------------------------
function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [campaigns, setCampaigns] = useState([]);
  const [settlement, setSettlement] = useState([]);
  const [reliability, setReliability] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [cRes, sRes, rRes] = await Promise.all([
          axios.get(`${API_URL}/campaigns`),
          axios.get(`${API_URL}/settlement`),
          axios.get(`${API_URL}/reliability`)
        ]);
        setCampaigns(cRes.data);
        setSettlement(sRes.data);
        setReliability(rRes.data);
      } catch (e) {
        console.error("Error fetching data:", e);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  return (
    <div className="min-h-screen w-full overflow-x-hidden font-sans text-slate-50 selection:bg-indigo-500/30 relative">
      
      {/* Global Animated Glassmorphism Background */}
      <BackgroundShader />
      
      {/* Persistent Top Navbar (Glassmorphic) */}
      <nav className="fixed top-0 w-full z-50 bg-slate-950/40 backdrop-blur-xl border-b border-white/5 shadow-sm">
        <div className="flex items-center justify-between px-6 md:px-12 py-4 max-w-7xl mx-auto">
          <div 
            className="flex items-center gap-2 cursor-pointer group"
            onClick={() => setActiveTab('home')}
          >
            <ShieldCheck size={28} className="text-indigo-400 group-hover:text-indigo-300 transition-colors drop-shadow-[0_0_8px_rgba(99,102,241,0.5)]" />
            <span className="text-2xl font-bold tracking-tight text-white font-display drop-shadow-md">VeriLift</span>
          </div>
          
          <div className="hidden md:flex items-center gap-1 bg-slate-900/40 backdrop-blur-md p-1.5 rounded-full border border-white/10 shadow-inner">
            <NavTab label="Home" id="home" active={activeTab} setActiveTab={setActiveTab} />
            <NavTab label="Verification" id="verification" active={activeTab} setActiveTab={setActiveTab} />
            <NavTab label="Settlement" id="settlement" active={activeTab} setActiveTab={setActiveTab} />
            <NavTab label="Leaderboard" id="reliability" active={activeTab} setActiveTab={setActiveTab} />
            <NavTab label="Insights" id="insights" active={activeTab} setActiveTab={setActiveTab} />
          </div>

          <button 
            onClick={() => setActiveTab('verification')}
            className="bg-indigo-600/80 backdrop-blur-md hover:bg-indigo-500 border border-indigo-400/30 text-white px-6 py-2 text-sm rounded-full font-bold active:scale-95 transition-all duration-300 shadow-[0_0_15px_rgba(99,102,241,0.4)]">
            Launch App
          </button>
        </div>
      </nav>

      {/* Main Content (Z-10 keeps it above the canvas) */}
      <main className="pt-24 pb-12 relative z-10">
        {activeTab === 'home' ? (
          <HomeView setActiveTab={setActiveTab} />
        ) : (
          <div className="max-w-7xl mx-auto px-6">
            {loading ? (
              <div className="flex h-[60vh] items-center justify-center flex-col gap-4">
                <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-indigo-500"></div>
                <p className="text-slate-300 font-medium drop-shadow-md">Connecting to VeriLift APIs...</p>
              </div>
            ) : campaigns.length === 0 ? (
              <div className="flex h-[60vh] items-center justify-center flex-col gap-4 glass-panel p-12 max-w-md mx-auto mt-20">
                <AlertTriangle size={48} className="text-amber-500 drop-shadow-md" />
                <h2 className="text-2xl font-bold font-display text-white">API Connection Failed</h2>
                <p className="text-slate-400 text-center">Make sure your backend is running on <code className="bg-slate-800/80 px-2 py-1 rounded text-sky-400">port 8001</code></p>
                <p className="text-slate-500 text-sm mt-2 text-center">Run: python -m uvicorn api:app --reload --port 8001</p>
              </div>
            ) : (
              <>
                {activeTab === 'verification' && <VerificationPage campaigns={campaigns} />}
                {activeTab === 'settlement' && <SettlementPage settlement={settlement} />}
                {activeTab === 'reliability' && <ReliabilityPage reliability={reliability} />}
                {activeTab === 'insights' && <InsightsPage campaigns={campaigns} />}
              </>
            )}
          </div>
        )}
      </main>
      
      {/* Footer */}
      <footer className="w-full py-8 bg-slate-950/40 backdrop-blur-md border-t border-white/5 mt-auto relative z-10">
        <div className="flex flex-col md:flex-row justify-between items-center px-6 md:px-12 gap-4 max-w-7xl mx-auto">
          <div className="flex items-center gap-2 opacity-60 hover:opacity-100 transition-opacity">
            <ShieldCheck className="text-indigo-400" size={20} />
            <span className="text-sm font-bold text-indigo-300 font-display">VeriLift</span>
          </div>
          <p className="text-xs text-slate-400 font-medium">© 2026 VeriLift. Precision Verified.</p>
        </div>
      </footer>
    </div>
  );
}

function NavTab({ label, id, active, setActiveTab }) {
  const isActive = active === id;
  return (
    <button
      onClick={() => setActiveTab(id)}
      className={`px-5 py-2.5 rounded-full text-sm font-medium transition-all duration-300 font-display tracking-wide ${
        isActive 
          ? 'bg-indigo-500/20 text-indigo-300 shadow-[inset_0_1px_1px_rgba(255,255,255,0.1)] border border-indigo-500/30' 
          : 'text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent'
      }`}
    >
      {label}
    </button>
  );
}

// -----------------------------------------------------------------------------
// Home View
// -----------------------------------------------------------------------------
function HomeView({ setActiveTab }) {
  return (
    <div className="animate-in fade-in duration-700 w-full">
      {/* Hero Section (Removed local canvas, using global BackgroundShader) */}
      <section className="relative min-h-[80vh] flex flex-col items-center justify-center text-center px-4 -mt-24 pt-32 pb-24">
        <div className="relative z-10 max-w-4xl mx-auto px-4 mt-12">
          <div className="inline-flex items-center gap-2 bg-indigo-500/10 border border-indigo-500/30 backdrop-blur-md px-5 py-2 rounded-full mb-8 shadow-xl">
            <span className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse shadow-[0_0_8px_rgba(99,102,241,1)]"></span>
            <span className="text-indigo-200 text-xs font-bold tracking-widest uppercase font-sans">Verified Accuracy</span>
          </div>
          <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-6 leading-tight tracking-tight font-display drop-shadow-2xl">
            Truth in Lift. <br/><span className="bg-gradient-to-r from-indigo-300 to-sky-300 bg-clip-text text-transparent drop-shadow-lg">Precision in Performance.</span>
          </h1>
          <p className="text-lg md:text-xl text-slate-200 mb-10 max-w-2xl mx-auto leading-relaxed drop-shadow-md font-medium">
            Stop paying for self-reported ROAS. VeriLift provides independent, rigorous verification of incremental lift using exposed vs holdout groups.
          </p>
          <div className="flex flex-col gap-4 items-center">
            <button 
              onClick={() => setActiveTab('verification')}
              className="bg-indigo-600/90 backdrop-blur-xl border border-indigo-400/40 hover:bg-indigo-500 text-white px-10 py-4 text-lg font-bold rounded-full shadow-[0_0_30px_rgba(99,102,241,0.5)] hover:scale-105 transition-transform active:scale-95 font-display tracking-wide">
              Enter Platform
            </button>
            <span className="text-sm text-slate-400 font-mono mt-2 drop-shadow-sm bg-slate-900/50 px-3 py-1 rounded-full border border-white/5">Independent Protocol v2.4.0</span>
          </div>
        </div>
      </section>

      {/* Overview Cards */}
      <section className="py-12 px-6 max-w-7xl mx-auto z-10 relative">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 -mt-16">
          <div className="glass-panel p-10 border-t-red-500/30 hover:border-red-500/40 hover:shadow-[0_10px_40px_rgba(239,68,68,0.15)]">
            <div className="flex items-center gap-4 mb-6">
              <div className="p-3 bg-red-500/20 backdrop-blur-md border border-red-500/20 rounded-xl shadow-[0_0_15px_rgba(239,68,68,0.2)]"><AlertTriangle className="text-red-300" size={28} /></div>
              <h2 className="text-3xl font-bold text-white font-display drop-shadow-sm">The Problem</h2>
            </div>
            <p className="text-slate-200 leading-relaxed text-lg mb-6 font-medium">
              Retail Media Networks are <span className="font-bold text-white">grading their own homework</span>. When networks report their own ROAS, brands pay for performance that might have happened anyway.
            </p>
            <div className="bg-red-500/10 border border-red-500/20 backdrop-blur-sm rounded-xl p-5 mb-6">
              <h4 className="text-red-300 font-bold mb-2 text-sm uppercase tracking-wider">Example</h4>
              <p className="text-slate-300 text-sm leading-relaxed">
                A network claims their ad drove 100 sales. But 90 of those customers were already searching for your brand and would have bought anyway. You just paid for 90 organic sales.
              </p>
            </div>
            <ul className="space-y-4">
              <li className="flex gap-3 text-slate-300 font-medium"><span className="text-red-400 drop-shadow-md">✗</span> Over-attribution of organic sales</li>
              <li className="flex gap-3 text-slate-300 font-medium"><span className="text-red-400 drop-shadow-md">✗</span> Conflicting metrics across platforms</li>
            </ul>
          </div>

          <div className="glass-panel p-10 border-t-emerald-500/30 hover:border-emerald-500/40 hover:shadow-[0_10px_40px_rgba(16,185,129,0.15)]">
            <div className="flex items-center gap-4 mb-6">
              <div className="p-3 bg-emerald-500/20 backdrop-blur-md border border-emerald-500/20 rounded-xl shadow-[0_0_15px_rgba(16,185,129,0.2)]"><CheckCircle2 className="text-emerald-300" size={28} /></div>
              <h2 className="text-3xl font-bold text-white font-display drop-shadow-sm">The Solution (Theme 02)</h2>
            </div>
            <p className="text-slate-200 leading-relaxed text-lg mb-6 font-medium">
              VeriLift independently verifies incremental lift by comparing exposed vs holdout groups in real-time. We adjust your performance payments based on <span className="font-bold text-emerald-300">verified lift</span>.
            </p>
            <div className="bg-emerald-500/10 border border-emerald-500/20 backdrop-blur-sm rounded-xl p-5 mb-6">
              <h4 className="text-emerald-300 font-bold mb-2 text-sm uppercase tracking-wider">Theme 02 Alignment</h4>
              <p className="text-slate-300 text-sm leading-relaxed">
                By defining <strong>clear measures of success</strong> (verified lift), we stop funding ads that merely retarget existing buyers. This protects your budget and creates a <strong>seamless customer experience</strong> by reducing ad fatigue.
              </p>
            </div>
            <ul className="space-y-4">
              <li className="flex gap-3 text-slate-300 font-medium"><span className="text-emerald-400 drop-shadow-md">✓</span> Multi-touch causal modeling</li>
              <li className="flex gap-3 text-slate-300 font-medium"><span className="text-emerald-400 drop-shadow-md">✓</span> Pay only for verified performance</li>
            </ul>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 px-6 max-w-7xl mx-auto z-10 relative">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-white font-display mb-4 drop-shadow-md">How VeriLift Works</h2>
          <p className="text-slate-300 max-w-2xl mx-auto text-lg font-medium drop-shadow-sm">A mathematically rigorous protocol that ensures you only pay for true incrementality.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
          {/* connecting line for desktop */}
          <div className="hidden md:block absolute top-12 left-0 w-full h-0.5 bg-indigo-500/30 shadow-[0_0_10px_rgba(99,102,241,0.5)] z-0"></div>
          
          <div className="glass-panel p-8 relative z-10 border-t-indigo-500/40 transform transition-all duration-300 hover:-translate-y-2 hover:shadow-[0_15px_30px_rgba(99,102,241,0.2)]">
            <div className="w-14 h-14 rounded-2xl bg-indigo-500/20 backdrop-blur-md border border-indigo-400/30 flex items-center justify-center text-indigo-300 font-bold text-2xl mb-6 shadow-[0_0_20px_rgba(99,102,241,0.4)] font-display">1</div>
            <h3 className="text-xl font-bold text-white font-display mb-3">Isolate the Holdout</h3>
            <p className="text-slate-300 leading-relaxed font-medium">We rigorously separate your audience into an exposed group (saw the ad) and a control group (did not see the ad).</p>
          </div>

          <div className="glass-panel p-8 relative z-10 border-t-sky-500/40 transform transition-all duration-300 hover:-translate-y-2 hover:shadow-[0_15px_30px_rgba(56,189,248,0.2)]">
            <div className="w-14 h-14 rounded-2xl bg-sky-500/20 backdrop-blur-md border border-sky-400/30 flex items-center justify-center text-sky-300 font-bold text-2xl mb-6 shadow-[0_0_20px_rgba(56,189,248,0.4)] font-display">2</div>
            <h3 className="text-xl font-bold text-white font-display mb-3">Calculate True Lift</h3>
            <p className="text-slate-300 leading-relaxed font-medium">We compare the conversion rates of both groups. The difference is your mathematically verified incremental lift.</p>
          </div>

          <div className="glass-panel p-8 relative z-10 border-t-emerald-500/40 transform transition-all duration-300 hover:-translate-y-2 hover:shadow-[0_15px_30px_rgba(16,185,129,0.2)]">
            <div className="w-14 h-14 rounded-2xl bg-emerald-500/20 backdrop-blur-md border border-emerald-400/30 flex items-center justify-center text-emerald-300 font-bold text-2xl mb-6 shadow-[0_0_20px_rgba(16,185,129,0.4)] font-display">3</div>
            <h3 className="text-xl font-bold text-white font-display mb-3">Adjust Settlement</h3>
            <p className="text-slate-300 leading-relaxed font-medium">If the network's self-reported ROAS is inflated, the settlement engine automatically reduces the performance payout to match reality.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

// -----------------------------------------------------------------------------
// Dashboard Components
// -----------------------------------------------------------------------------

function MetricCard({ title, value, subvalue, type = 'default' }) {
  const colors = {
    default: 'text-white border-indigo-500/20 bg-indigo-500/5',
    success: 'text-emerald-300 border-emerald-500/30 bg-emerald-500/10 shadow-[0_0_15px_rgba(16,185,129,0.1)]',
    warning: 'text-amber-300 border-amber-500/30 bg-amber-500/10 shadow-[0_0_15px_rgba(245,158,11,0.1)]',
    danger: 'text-red-300 border-red-500/30 bg-red-500/10 shadow-[0_0_15px_rgba(239,68,68,0.1)]'
  };
  
  return (
    <div className={`glass-panel p-6 ${colors[type]} hover:shadow-2xl hover:scale-[1.02] transition-all duration-300`}>
      <h3 className="text-sm font-semibold text-slate-300 mb-2 tracking-wide uppercase drop-shadow-sm">{title}</h3>
      <div className="text-4xl font-extrabold font-display tracking-tight drop-shadow-md">{value}</div>
      {subvalue && <div className="text-sm mt-3 font-medium opacity-90">{subvalue}</div>}
    </div>
  );
}

function VerificationPage({ campaigns }) {
  const [selectedIdx, setSelectedIdx] = useState(0);
  const [simulatedLift, setSimulatedLift] = useState(null);

  // Reset simulator when campaign changes
  useEffect(() => {
    if (campaigns[selectedIdx]) {
      setSimulatedLift(campaigns[selectedIdx].verified_lift_relative * 100);
    }
  }, [selectedIdx, campaigns]);

  if (!campaigns.length || simulatedLift === null) return null;
  
  const c = campaigns[selectedIdx];
  const claimed = (c.claimed_lift * 100).toFixed(1);
  const verified = simulatedLift.toFixed(1);
  const actualRatio = simulatedLift / (c.claimed_lift * 100);
  const ratio = (actualRatio).toFixed(2);
  
  // Re-calculate the chart roughly based on simulated lift
  const baseHoldout = c.holdout_cr * 100;
  const simulatedExposed = baseHoldout * (1 + (simulatedLift / 100));

  const chartData = [
    { name: 'Holdout Group', value: baseHoldout },
    { name: 'Exposed Group (Simulated)', value: simulatedExposed }
  ];

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="glass-panel p-8 border-t-indigo-500/30 bg-indigo-500/5">
        <h1 className="text-4xl font-extrabold text-white mb-3 font-display drop-shadow-md">Campaign Verification</h1>
        <p className="text-lg text-slate-300 font-medium">Compare claimed performance with independently verified lift.</p>
      </header>
      
      <div className="glass-panel p-6 flex flex-col md:flex-row items-center justify-between gap-4">
        <select 
          className="bg-slate-900/80 backdrop-blur-xl border border-indigo-500/30 text-white text-base rounded-xl focus:ring-indigo-500 focus:border-indigo-400 block w-full md:w-1/2 p-3 font-medium shadow-inner transition-colors"
          value={selectedIdx}
          onChange={(e) => setSelectedIdx(parseInt(e.target.value))}
        >
          {campaigns.map((camp, i) => (
            <option key={camp.campaign_id} value={i} className="bg-slate-900">
              {camp.campaign_name} ({camp.network_name})
            </option>
          ))}
        </select>
        <div className="text-sm font-bold px-6 py-2.5 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/30 shadow-[0_0_10px_rgba(99,102,241,0.2)]">
          Network: {c.network_name}
        </div>
      </div>

      <div className="glass-panel p-6 border-t-indigo-500/30">
        <div className="flex items-center gap-3 mb-4">
          <SlidersHorizontal className="text-indigo-400" size={20} />
          <h3 className="text-lg font-bold text-white font-display">Interactive Lift Simulator</h3>
        </div>
        <p className="text-sm text-slate-400 mb-6 font-medium">Drag the slider to simulate what happens if the true incremental lift drops. Notice how the verification ratio instantly recalculates.</p>
        <div className="flex items-center gap-6">
          <input 
            type="range" 
            min="0" 
            max={Math.max(c.claimed_lift * 100, 30)} 
            step="0.1" 
            value={simulatedLift} 
            onChange={(e) => setSimulatedLift(parseFloat(e.target.value))}
            className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-indigo-500"
          />
          <div className="text-xl font-bold font-mono text-indigo-300 w-24 text-right">{simulatedLift.toFixed(1)}%</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <MetricCard title="Claimed Lift" value={`${claimed}%`} />
        <MetricCard 
          title="Simulated Lift" 
          value={`${verified}%`} 
          subvalue={`${(verified - claimed).toFixed(1)}pp vs claimed`} 
          type={actualRatio < 0.6 ? 'danger' : actualRatio > 0.9 ? 'success' : 'warning'} 
        />
        <MetricCard title="Verification Ratio" value={ratio} />
        <MetricCard title="Overstatement" value={actualRatio > 0 ? (1 / actualRatio).toFixed(1) + 'x' : 'inf'} />
      </div>

      <div className="glass-panel p-8 border-t-sky-500/20">
        <h3 className="text-2xl font-bold text-white mb-8 font-display drop-shadow-md">Exposed vs Holdout Conversion Rate</h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
              <XAxis dataKey="name" stroke="#94a3b8" tick={{fill: '#cbd5e1', fontSize: 14, fontWeight: 500}} />
              <YAxis stroke="#94a3b8" tickFormatter={(val) => `${val.toFixed(1)}%`} tick={{fill: '#cbd5e1', fontWeight: 500}} />
              <RechartsTooltip cursor={{fill: 'rgba(255,255,255,0.05)'}} contentStyle={{backgroundColor: 'rgba(15,23,42,0.9)', backdropFilter: 'blur(12px)', borderColor: 'rgba(99,102,241,0.3)', borderRadius: '12px', fontWeight: 'bold', boxShadow: '0 10px 25px rgba(0,0,0,0.5)'}} />
              <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={index === 0 ? 'rgba(71,85,105,0.7)' : 'rgba(99,102,241,0.8)'} stroke={index === 0 ? '#64748b' : '#818cf8'} strokeWidth={2} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

function SettlementPage({ settlement }) {
  const [selectedIdx, setSelectedIdx] = useState(0);
  const receiptRef = useRef(null);

  if (!settlement.length) return null;

  const downloadReceipt = () => {
    const c = settlement[selectedIdx];
    const fmt = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val);

    const pdf = new jsPDF({ orientation: 'portrait', unit: 'pt', format: 'a4' });
    const W = pdf.internal.pageSize.getWidth();
    let y = 60;

    // Header background
    pdf.setFillColor(2, 6, 23);
    pdf.rect(0, 0, W, pdf.internal.pageSize.getHeight(), 'F');

    // Title
    pdf.setFont('helvetica', 'bold');
    pdf.setFontSize(28);
    pdf.setTextColor(255, 255, 255);
    pdf.text('VeriLift', 40, y);

    pdf.setFontSize(10);
    pdf.setTextColor(129, 140, 248);
    pdf.text('SMART CONTRACT SETTLEMENT RECEIPT', 40, y + 18);

    // Badge
    pdf.setFillColor(16, 185, 129, 30);
    pdf.setDrawColor(52, 211, 153);
    pdf.roundedRect(W - 190, y - 18, 150, 28, 4, 4, 'FD');
    pdf.setTextColor(52, 211, 153);
    pdf.setFontSize(9);
    pdf.text('VERIFIED & SETTLED', W - 180, y - 2);

    // Divider
    y += 40;
    pdf.setDrawColor(99, 102, 241);
    pdf.setLineWidth(1.5);
    pdf.line(40, y, W - 40, y);
    y += 30;

    // Campaign Details
    pdf.setTextColor(203, 213, 225);
    pdf.setFontSize(14);
    pdf.setFont('helvetica', 'bold');
    pdf.text('Campaign Details', 40, y);
    y += 8;
    pdf.setDrawColor(30, 41, 59);
    pdf.setLineWidth(0.5);
    pdf.line(40, y, W - 40, y);
    y += 20;

    pdf.setFillColor(15, 23, 42);
    pdf.setDrawColor(30, 41, 59);
    pdf.roundedRect(40, y, W - 80, 80, 4, 4, 'FD');

    pdf.setTextColor(100, 116, 139);
    pdf.setFontSize(8);
    pdf.setFont('helvetica', 'bold');
    pdf.text('CAMPAIGN NAME', 56, y + 18);
    pdf.text('NETWORK PROVIDER', W / 2 + 8, y + 18);
    pdf.text('CLAIMED LIFT', 56, y + 52);
    pdf.text('VERIFIED LIFT', W / 2 + 8, y + 52);

    pdf.setTextColor(255, 255, 255);
    pdf.setFontSize(13);
    pdf.setFont('helvetica', 'bold');
    pdf.text(c.campaign_name, 56, y + 32);
    pdf.text(c.network_name, W / 2 + 8, y + 32);
    pdf.text(`${(c.claimed_lift * 100).toFixed(1)}%`, 56, y + 66);

    pdf.setTextColor(52, 211, 153);
    pdf.text(`${(c.verified_lift_relative * 100).toFixed(1)}%`, W / 2 + 8, y + 66);
    y += 100;

    // Financial Breakdown
    pdf.setTextColor(203, 213, 225);
    pdf.setFontSize(14);
    pdf.setFont('helvetica', 'bold');
    pdf.text('Financial Breakdown', 40, y);
    y += 8;
    pdf.setDrawColor(30, 41, 59);
    pdf.setLineWidth(0.5);
    pdf.line(40, y, W - 40, y);
    y += 20;

    const rows = [
      ['Total Claimed Invoice', fmt(c.campaign_invoice), [203, 213, 225]],
      ['Guaranteed Base Payment', fmt(c.base_payment), [203, 213, 225]],
      ['At-Risk Performance Pool', fmt(c.performance_pool), [203, 213, 225]],
      ['Verification Ratio (Applied)', `${(c.verification_ratio_capped * 100).toFixed(0)}%`, [248, 113, 113]],
      ['Released Performance Payment', fmt(c.released_performance_payment), [203, 213, 225]],
    ];

    pdf.setFillColor(15, 23, 42);
    pdf.setDrawColor(30, 41, 59);
    pdf.roundedRect(40, y, W - 80, rows.length * 34 + 20, 4, 4, 'FD');
    y += 16;

    rows.forEach(([label, value, [r, g, b]], i) => {
      pdf.setFont('helvetica', 'normal');
      pdf.setFontSize(11);
      pdf.setTextColor(203, 213, 225);
      pdf.text(label, 56, y);
      pdf.setFont('helvetica', 'bold');
      pdf.setTextColor(r, g, b);
      pdf.text(value, W - 56, y, { align: 'right' });
      if (i < rows.length - 1) {
        y += 4;
        pdf.setDrawColor(30, 41, 59);
        pdf.setLineWidth(0.3);
        pdf.line(56, y, W - 56, y);
      }
      y += 30;
    });
    y += 10;

    // Final Payable
    pdf.setFillColor(16, 185, 129, 25);
    pdf.setDrawColor(52, 211, 153);
    pdf.setLineWidth(1);
    pdf.roundedRect(40, y, W - 80, 50, 6, 6, 'FD');
    pdf.setFont('helvetica', 'bold');
    pdf.setFontSize(16);
    pdf.setTextColor(255, 255, 255);
    pdf.text('FINAL PAYABLE', 56, y + 30);
    pdf.setTextColor(52, 211, 153);
    pdf.text(fmt(c.final_payable), W - 56, y + 30, { align: 'right' });
    y += 80;

    // Footer
    pdf.setDrawColor(30, 41, 59);
    pdf.setLineWidth(0.5);
    pdf.line(40, y, W - 40, y);
    y += 20;
    pdf.setTextColor(148, 163, 184);
    pdf.setFontSize(9);
    pdf.setFont('helvetica', 'normal');
    pdf.text('This document is a mathematically verified smart contract settlement receipt.', W / 2, y, { align: 'center' });
    pdf.setTextColor(100, 116, 139);
    pdf.text(`Generated by VeriLift Protocol · ${new Date().toLocaleDateString()}`, W / 2, y + 14, { align: 'center' });

    pdf.save(`VeriLift_Settlement_Receipt_${c.campaign_id}.pdf`);
  };
  
  const c = settlement[selectedIdx];
  const fmt = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val);

  const chartData = [
    { name: 'Invoice', value: c.campaign_invoice, fill: 'rgba(71,85,105,0.7)', stroke: '#64748b' },
    { name: 'Payable', value: c.final_payable, fill: 'rgba(16,185,129,0.7)', stroke: '#34d399' },
    { name: 'Adjusted', value: c.adjusted_amount, fill: 'rgba(239,68,68,0.7)', stroke: '#f87171' }
  ];

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="glass-panel p-8 border-t-indigo-500/30 bg-indigo-500/5 flex justify-between items-start">
        <div>
          <h1 className="text-4xl font-extrabold text-white mb-3 font-display drop-shadow-md">Settlement Engine</h1>
          <p className="text-lg text-slate-300 font-medium">Performance-linked payout adjusted based on verified lift.</p>
        </div>
        <button onClick={downloadReceipt} className="flex items-center gap-2 bg-slate-800/80 hover:bg-slate-700 text-white px-5 py-2.5 rounded-xl border border-slate-600 transition-colors shadow-lg group">
          <Download size={20} className="text-indigo-400 group-hover:scale-110 transition-transform" />
          <span className="font-bold text-sm tracking-wide">Download Receipt (PDF)</span>
        </button>
      </header>
      
      <div className="glass-panel p-6 flex flex-col md:flex-row items-center justify-between gap-4">
        <select 
          className="bg-slate-900/80 backdrop-blur-xl border border-indigo-500/30 text-white text-base rounded-xl focus:ring-indigo-500 focus:border-indigo-400 block w-full md:w-1/2 p-3 font-medium shadow-inner transition-colors"
          value={selectedIdx}
          onChange={(e) => setSelectedIdx(parseInt(e.target.value))}
        >
          {settlement.map((camp, i) => (
            <option key={camp.campaign_id} value={i} className="bg-slate-900">
              {camp.campaign_name} ({camp.network_name})
            </option>
          ))}
        </select>
        <div className={`text-sm font-bold px-6 py-2.5 rounded-full border shadow-lg ${c.settlement_status.includes('Full') ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30 shadow-emerald-500/20' : 'bg-amber-500/10 text-amber-300 border-amber-500/30 shadow-amber-500/20'}`}>
          {c.settlement_status}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <MetricCard title="Total Invoice" value={fmt(c.campaign_invoice)} />
        <MetricCard title="Base Payment (Guaranteed)" value={fmt(c.base_payment)} />
        <MetricCard title="Performance Pool (At-Risk)" value={fmt(c.performance_pool)} />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <MetricCard title="Released from Pool" value={fmt(c.released_performance_payment)} subvalue={`${(c.verification_ratio_capped * 100).toFixed(0)}% verified ratio`} />
        <MetricCard title="Final Payable" value={fmt(c.final_payable)} type="success" />
        <MetricCard title="Adjusted Amount" value={fmt(c.adjusted_amount)} type={c.adjusted_amount > 0 ? "danger" : "default"} />
      </div>

      <div className="glass-panel p-8 border-t-sky-500/20">
        <h3 className="text-2xl font-bold text-white mb-8 font-display drop-shadow-md">Settlement Breakdown</h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
              <XAxis dataKey="name" stroke="#94a3b8" tick={{fill: '#cbd5e1', fontSize: 14, fontWeight: 500}} />
              <YAxis stroke="#94a3b8" tick={{fill: '#cbd5e1', fontWeight: 500}} />
              <RechartsTooltip cursor={{fill: 'rgba(255,255,255,0.05)'}} contentStyle={{backgroundColor: 'rgba(15,23,42,0.9)', backdropFilter: 'blur(12px)', borderColor: 'rgba(99,102,241,0.3)', borderRadius: '12px', fontWeight: 'bold', boxShadow: '0 10px 25px rgba(0,0,0,0.5)'}} formatter={(val) => fmt(val)} />
              <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} stroke={entry.stroke} strokeWidth={2} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

    </div>
  );
}


function ReliabilityPage({ reliability }) {
  if (!reliability.length) return null;

  const chartData = [...reliability].reverse();

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="glass-panel p-8 border-t-indigo-500/30 bg-indigo-500/5">
        <h1 className="text-4xl font-extrabold text-white mb-3 font-display drop-shadow-md">Network Reliability Leaderboard</h1>
        <p className="text-lg text-slate-300 font-medium">Rank retail media networks by long-term trustworthiness.</p>
      </header>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {reliability.map((r, i) => {
          const medals = ['text-yellow-400 drop-shadow-[0_0_15px_rgba(250,204,21,0.5)]', 'text-slate-300 drop-shadow-[0_0_15px_rgba(203,213,225,0.5)]', 'text-amber-600 drop-shadow-[0_0_15px_rgba(217,119,6,0.5)]'];
          const color = r.risk_level === 'Low Risk' ? 'text-emerald-300 border-emerald-500/30 bg-emerald-500/10 shadow-[0_0_20px_rgba(16,185,129,0.15)]' : 
                        r.risk_level === 'Medium Risk' ? 'text-amber-300 border-amber-500/30 bg-amber-500/10 shadow-[0_0_20px_rgba(245,158,11,0.15)]' : 
                        'text-red-300 border-red-500/30 bg-red-500/10 shadow-[0_0_20px_rgba(239,68,68,0.15)]';
          return (
            <div key={r.network_name} className={`glass-panel p-10 relative overflow-hidden flex flex-col items-center border hover:-translate-y-2 transition-transform duration-300 ${color}`}>
              <div className={`text-6xl font-black mb-4 font-display ${i < 3 ? medals[i] : 'text-slate-500'}`}>#{i+1}</div>
              <div className="text-2xl font-bold text-white mb-2 font-display tracking-wide">{r.network_name}</div>
              <div className="text-6xl font-black my-5 text-white font-display drop-shadow-xl">{r.reliability_score.toFixed(1)}</div>
              <div className={`px-6 py-2.5 rounded-full text-xs font-bold border tracking-widest uppercase shadow-inner ${color.replace(/bg-.*?\s/, '')}`}>{r.risk_level}</div>
            </div>
          );
        })}
      </div>

      <div className="glass-panel p-8 border-t-sky-500/20">
        <h3 className="text-2xl font-bold text-white mb-8 font-display drop-shadow-md">Reliability Score (0-100)</h3>
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={false} />
              <XAxis type="number" domain={[0, 100]} stroke="#94a3b8" tick={{fill: '#cbd5e1'}} />
              <YAxis dataKey="network_name" type="category" stroke="#94a3b8" tick={{fill: '#f8fafc', fontSize: 15, fontWeight: 600}} />
              <RechartsTooltip cursor={{fill: 'rgba(255,255,255,0.05)'}} contentStyle={{backgroundColor: 'rgba(15,23,42,0.9)', backdropFilter: 'blur(12px)', borderColor: 'rgba(99,102,241,0.3)', borderRadius: '12px', fontWeight: 'bold'}} />
              <ReferenceLine x={85} stroke="#34d399" strokeDasharray="4 4" strokeWidth={2} />
              <ReferenceLine x={60} stroke="#fbbf24" strokeDasharray="4 4" strokeWidth={2} />
              <Bar dataKey="reliability_score" radius={[0, 8, 8, 0]}>
                {chartData.map((entry, index) => {
                  const fill = entry.risk_level === 'Low Risk' ? 'rgba(16,185,129,0.8)' : 
                               entry.risk_level === 'Medium Risk' ? 'rgba(245,158,11,0.8)' : 'rgba(239,68,68,0.8)';
                  const stroke = entry.risk_level === 'Low Risk' ? '#34d399' : 
                                 entry.risk_level === 'Medium Risk' ? '#fbbf24' : '#f87171';
                  return <Cell key={`cell-${index}`} fill={fill} stroke={stroke} strokeWidth={2} />;
                })}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

function InsightsPage({ campaigns }) {
  const [selectedIdx, setSelectedIdx] = useState(0);
  const [insight, setInsight] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!campaigns.length) return;
    async function loadInsight() {
      setLoading(true);
      try {
        const c = campaigns[selectedIdx];
        const res = await axios.get(`${API_URL}/insights/${c.campaign_id}`);
        setInsight(res.data);
      } catch (e) {
        console.error("Error fetching insight", e);
      } finally {
        setLoading(false);
      }
    }
    loadInsight();
  }, [selectedIdx, campaigns]);

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <header className="glass-panel p-8 border-t-indigo-500/30 bg-indigo-500/5">
        <h1 className="text-4xl font-extrabold text-white mb-3 font-display drop-shadow-md">AI Insights</h1>
        <p className="text-lg text-slate-300 font-medium">Executive summary powered by AI verification.</p>
      </header>

      <div className="glass-panel p-6">
        <select 
          className="bg-slate-900/80 backdrop-blur-xl border border-indigo-500/30 text-white text-base rounded-xl focus:ring-indigo-500 focus:border-indigo-400 block w-full md:w-1/2 p-3 font-medium shadow-inner transition-colors"
          value={selectedIdx}
          onChange={(e) => setSelectedIdx(parseInt(e.target.value))}
        >
          {campaigns.map((camp, i) => (
            <option key={camp.campaign_id} value={i} className="bg-slate-900">
              {camp.campaign_name} ({camp.network_name})
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <AILoadingSequence />
      ) : insight ? (
        <div className="space-y-6">
          <div className="flex gap-2">
            <span className="px-6 py-2.5 bg-indigo-500/20 text-indigo-200 rounded-full text-xs font-bold border border-indigo-500/40 tracking-widest uppercase shadow-[0_0_15px_rgba(99,102,241,0.2)]">
              Source: {insight.insight_source}
            </span>
          </div>

          <InsightBlock title="Discrepancy Explanation" content={insight.discrepancy_explanation} delay={100} />
          <InsightBlock title="Settlement Summary" content={insight.settlement_summary} delay={200} />
          <InsightBlock title="CX Impact" content={insight.cx_impact} delay={300} />
          <InsightBlock title="Recommended Action" content={insight.recommended_action} delay={400} />
          <InsightBlock title="Contract Recommendation" content={insight.contract_recommendation} delay={500} />
        </div>
      ) : null}
    </div>
  );
}

function InsightBlock({ title, content, delay }) {
  return (
    <div 
      className="glass-panel p-8 border-l-4 border-l-indigo-400 hover:-translate-y-1 hover:shadow-[0_15px_30px_rgba(99,102,241,0.15)] transition-all duration-300 animate-in fade-in slide-in-from-right-4"
      style={{ animationDelay: `${delay}ms`, animationFillMode: 'both' }}
    >
      <h3 className="text-sm font-bold text-indigo-300 uppercase tracking-widest mb-4 font-display">{title}</h3>
      <p className="text-slate-200 leading-relaxed text-lg font-medium">{content}</p>
    </div>
  );
}

function AILoadingSequence() {
  const steps = [
    "[12%] Initializing Groq LPU processing...",
    "[34%] Isolating holdout group data streams...",
    "[67%] Applying multi-touch causal inference models...",
    "[89%] Reconciling smart contract settlement triggers...",
    "[100%] Synthesizing executive insights..."
  ];
  
  const [stepIdx, setStepIdx] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setStepIdx(prev => {
        if (prev < steps.length - 1) return prev + 1;
        return prev;
      });
    }, 800);
    return () => clearInterval(timer);
  }, [steps.length]);

  return (
    <div className="glass-panel p-24 flex flex-col items-center justify-center border-t-indigo-500/30 shadow-[0_0_30px_rgba(99,102,241,0.15)] h-96">
      <Cpu size={64} className="text-indigo-400 mb-8 animate-pulse shadow-indigo-500/50 drop-shadow-[0_0_15px_rgba(99,102,241,0.8)]" />
      <div className="w-full max-w-lg bg-slate-900 rounded-full h-2 mb-8 overflow-hidden border border-slate-700 shadow-inner">
        <div 
          className="bg-indigo-500 h-2 rounded-full transition-all duration-700 ease-out shadow-[0_0_10px_rgba(99,102,241,0.8)]" 
          style={{ width: `${(stepIdx + 1) * 20}%` }}
        ></div>
      </div>
      <p className="text-indigo-300 font-mono text-lg drop-shadow-md tracking-wider h-8">
        {steps[stepIdx]}
      </p>
    </div>
  );
}

export default App;
