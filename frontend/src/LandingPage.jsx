import { useEffect, useRef } from 'react';

export default function LandingPage({ onLaunchDashboard }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    function syncSize() {
      const w = canvas.clientWidth || window.innerWidth;
      const h = canvas.clientHeight || window.innerHeight;
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
        
        float t = u_time * 0.2;
        for(float i = 1.0; i < 4.0; i++){
            p.x += 0.3 / i * sin(i * 3.0 * p.y + t);
            p.y += 0.3 / i * cos(i * 3.0 * p.x + t);
        }
        
        vec3 color1 = vec3(0.02, 0.03, 0.05);
        vec3 color2 = vec3(0.0, 0.94, 1.0);
        
        float mask = sin(p.x + p.y + t) * 0.5 + 0.5;
        vec3 finalColor = mix(color1, color2 * 0.1, mask);
        
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
    <div className="bg-[#111318] text-[#e2e2e8] min-h-screen selection:bg-[#00f0ff] selection:text-[#006970]">
      {/* TopAppBar */}
      <nav className="fixed top-0 w-full z-50 bg-[#111318]/70 backdrop-blur-md border-b border-white/10 shadow-none">
        <div className="flex items-center justify-between px-6 md:px-12 py-4 max-w-7xl mx-auto">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-[#00f0ff]" style={{fontVariationSettings: "'FILL' 1"}}>verified</span>
            <span className="text-2xl font-bold tracking-tight text-[#00f0ff] font-['Manrope']">VeriLift</span>
          </div>
          <button 
            onClick={onLaunchDashboard}
            className="bg-[#00f0ff] text-[#006970] px-6 py-2 text-sm rounded-full font-bold active:scale-95 transition-all duration-300 hover:brightness-110 shadow-[0_0_20px_rgba(0,240,255,0.3)]">
            Launch Dashboard
          </button>
        </div>
      </nav>

      <main>
        {/* Hero Section */}
        <section className="relative h-screen flex flex-col items-center justify-center text-center px-4 overflow-hidden">
          <div className="absolute inset-0 w-full h-full block">
            <canvas ref={canvasRef} className="block w-full h-full"></canvas>
          </div>
          <div className="relative z-10 max-w-3xl animate-[fadeInUp_0.8s_ease-out_forwards]">
            <div className="inline-flex items-center gap-2 bg-white/5 border border-white/10 px-4 py-1 rounded-full mb-6">
              <span className="w-1.5 h-1.5 rounded-full bg-[#00f0ff] animate-pulse"></span>
              <span className="text-[#dbfcff] text-xs font-semibold tracking-widest uppercase font-['Inter']">Verified Accuracy</span>
            </div>
            <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight font-['Manrope']">
              Truth in Lift. <span className="text-[#00f0ff]">Precision in Performance.</span>
            </h1>
            <p className="text-lg text-[#b9cacb] mb-10 max-w-2xl mx-auto leading-relaxed font-['Inter']">
              Stop paying for self-reported ROAS. VeriLift provides independent, rigorous verification of incremental lift.
            </p>
            <div className="flex flex-col gap-4 items-center">
              <button 
                onClick={onLaunchDashboard}
                className="bg-[#00f0ff] text-[#006970] px-10 py-4 text-xl font-bold rounded-lg shadow-[0_0_20px_rgba(0,240,255,0.3)] hover:scale-105 transition-transform active:scale-95 font-['Manrope']">
                Get Verified
              </button>
              <span className="text-sm text-[#dbfcff]/60 font-['JetBrains_Mono']">Independent Protocol v2.4.0</span>
            </div>
          </div>
          {/* Scroll Indicator */}
          <div className="absolute bottom-10 left-1/2 -translate-x-1/2 animate-bounce opacity-50">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-white"><path d="m6 9 6 6 6-6"/></svg>
          </div>
        </section>

        {/* Problem Section */}
        <section className="py-24 px-4 bg-[#111318]">
          <div className="max-w-7xl mx-auto">
            <div className="mb-12">
              <h2 className="text-3xl text-white mb-4 font-semibold font-['Manrope']">The Self-Reporting Trap</h2>
              <div className="w-12 h-1 bg-[#00f0ff]"></div>
            </div>
            <div className="bg-[#161b22]/70 backdrop-blur-xl border border-white/10 p-8 rounded-xl transition-transform duration-500 hover:scale-[1.02] shadow-[inset_0_1px_1px_rgba(255,255,255,0.05)]">
              <div className="grid md:grid-cols-2 gap-12 items-center">
                <div>
                  <p className="text-lg text-[#b9cacb] leading-relaxed font-['Inter']">
                    Retail Media Networks (RMNs) are <span className="text-white font-semibold">grading their own homework</span>. When networks report their own ROAS, brands pay for performance that might have happened anyway.
                  </p>
                  <div className="mt-8 space-y-4">
                    <div className="flex items-start gap-4">
                      <span className="material-symbols-outlined text-[#ffb4ab] mt-1">warning</span>
                      <span className="text-base text-[#b9cacb] font-['Inter']">Over-attribution of organic sales to adspend.</span>
                    </div>
                    <div className="flex items-start gap-4">
                      <span className="material-symbols-outlined text-[#ffb4ab] mt-1">warning</span>
                      <span className="text-base text-[#b9cacb] font-['Inter']">Conflicting metrics across siloed platforms.</span>
                    </div>
                    <div className="flex items-start gap-4">
                      <span className="material-symbols-outlined text-[#ffb4ab] mt-1">warning</span>
                      <span className="text-base text-[#b9cacb] font-['Inter']">Lack of true holdout group integrity.</span>
                    </div>
                  </div>
                </div>
                <div className="relative aspect-video rounded-lg overflow-hidden bg-[#282a2e] group">
                  <img alt="Dashboard" className="w-full h-full object-cover opacity-60 mix-blend-luminosity group-hover:scale-110 transition-transform duration-1000" src="https://lh3.googleusercontent.com/aida-public/AB6AXuBAhWya5RZDFeqIe__hrAs8h3YD6UAl1OJqlTYs8W1SjetQ_5aOrlTl1VcnxvoyVY7eelNr21Ye-lW1oZ9r5Fdw17gOiwrePcKTT17E-geHfKAoA4qxeSJQRGP-da7wQBMhaz-7ryZ7_piKmbhGHbBRkMT03-oLN1b86yZZnlJBklkTYQWvsUE1qyKUrrp_n9FOMzHxqDeWjxxmexk4RXmQtLxRJd3ow3kszmE6xGHsHqUaeddY8NiXaUli-EEebIc7zHEC3aihFdgj" />
                  <div className="absolute inset-0 bg-gradient-to-t from-[#111318] via-transparent to-transparent"></div>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="bg-[#111318]/80 backdrop-blur-md border border-white/10 px-6 py-4 rounded-xl text-center">
                      <span className="text-3xl font-semibold text-[#00f0ff] block font-['Manrope']">64%</span>
                      <span className="text-xs font-semibold text-[#b9cacb] font-['Inter']">Average ROAS Inflation</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Solution Section */}
        <section className="py-24 px-4 bg-[#111318]">
          <div className="max-w-7xl mx-auto">
            <div className="mb-12 text-right">
              <h2 className="text-3xl text-white mb-4 font-semibold font-['Manrope']">Independent Verification</h2>
              <div className="w-12 h-1 bg-[#00f0ff] ml-auto"></div>
            </div>
            <div className="bg-[#161b22]/70 backdrop-blur-xl border border-white/10 p-8 rounded-xl transition-transform duration-500 hover:scale-[1.02] shadow-[inset_0_1px_1px_rgba(255,255,255,0.05)]">
              <div className="grid md:grid-cols-2 gap-12 items-center">
                <div className="order-2 md:order-1 relative aspect-video rounded-lg overflow-hidden bg-[#282a2e] group">
                  <img alt="Circuit" className="w-full h-full object-cover opacity-60 mix-blend-screen group-hover:scale-110 transition-transform duration-1000" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDKPh3Wfgf0S878zfgDVaAgMWL3XEHioDRoIWseWkJ54lEvuECFt5NO4cIYL7pzI5FduvmcB3oOMnLHWZ9ViZkaI3c7bOMMkScVlPVm824M0SIz5C1HlZ2TaVzw1oD1w0gEd4c_0Ctek5oH8o4kNzvFZKTcTCeXgpdh1FrHTKVVexmXaL_9soU3cH3A7xmWOAK8kb-z0_pUdp5bsHJF49U3GydV6t3cESaH9y140Kl6Z4CapmSghZmZraQKCPsIH9T-hwODFKm3Yu6O" />
                  <div className="absolute inset-0 bg-gradient-to-tr from-[#00f0ff]/10 to-transparent"></div>
                  <div className="absolute bottom-6 right-6 flex flex-col gap-2">
                    <div className="bg-[#00f0ff]/20 backdrop-blur-lg border border-[#00f0ff]/30 px-4 py-2 rounded-full inline-flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-[#00f0ff]"></span>
                      <span className="text-xs font-semibold text-[#00f0ff] font-['Inter']">Real-time Analysis</span>
                    </div>
                  </div>
                </div>
                <div className="order-1 md:order-2">
                  <p className="text-lg text-[#b9cacb] leading-relaxed mb-8 font-['Inter']">
                    VeriLift independently verifies incremental lift by comparing exposed vs holdout groups in real-time. We adjust your performance payments based on <span className="text-[#00f0ff] font-semibold">verified lift</span>, not self-reported claims.
                  </p>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 border border-white/5 rounded-lg bg-white/5">
                      <span className="text-xs font-semibold text-[#00f0ff] block mb-1 font-['Inter']">Exposure</span>
                      <p className="text-sm text-[#b9cacb] font-['Inter']">Multi-touch causal modeling</p>
                    </div>
                    <div className="p-4 border border-white/5 rounded-lg bg-white/5">
                      <span className="text-xs font-semibold text-[#00f0ff] block mb-1 font-['Inter']">Holdout</span>
                      <p className="text-sm text-[#b9cacb] font-['Inter']">Synthetic & ghost control groups</p>
                    </div>
                    <div className="p-4 border border-white/5 rounded-lg bg-white/5">
                      <span className="text-xs font-semibold text-[#00f0ff] block mb-1 font-['Inter']">Delta</span>
                      <p className="text-sm text-[#b9cacb] font-['Inter']">Verified incremental conversion</p>
                    </div>
                    <div className="p-4 border border-white/5 rounded-lg bg-white/5">
                      <span className="text-xs font-semibold text-[#00f0ff] block mb-1 font-['Inter']">Settlement</span>
                      <p className="text-sm text-[#b9cacb] font-['Inter']">Pay only for true performance</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Final CTA */}
        <section className="py-24 px-4 text-center relative overflow-hidden bg-[#111318]">
          <div className="absolute inset-0 bg-[#00f0ff]/5 blur-[120px] rounded-full scale-150"></div>
          <div className="relative z-10 max-w-2xl mx-auto">
            <h2 className="text-5xl font-bold text-white mb-6 font-['Manrope']">Ready for Absolute Clarity?</h2>
            <p className="text-lg text-[#b9cacb] mb-10 font-['Inter']">
              Join the world's most sophisticated retail brands using VeriLift to reclaim their media efficiency.
            </p>
            <button 
              onClick={onLaunchDashboard}
              className="bg-white text-black px-12 py-4 text-xl font-bold rounded-lg hover:bg-[#00f0ff] hover:text-[#006970] transition-all duration-300 font-['Manrope']">
              Enter Platform
            </button>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="w-full py-12 bg-[#0c0e12] border-t border-white/5">
        <div className="flex flex-col md:flex-row justify-between items-center px-6 md:px-12 gap-8 max-w-7xl mx-auto">
          <div className="flex flex-col items-center md:items-start gap-2">
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-[#00f0ff]" style={{fontVariationSettings: "'FILL' 1"}}>verified</span>
              <span className="text-lg font-bold text-[#00f0ff] font-['Manrope']">VeriLift</span>
            </div>
            <p className="text-sm text-[#b9cacb] opacity-60 font-['Inter']">© 2024 VeriLift. Precision Verified.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
