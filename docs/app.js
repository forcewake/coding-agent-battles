const fmt = new Intl.NumberFormat('en-US');
const money = (v) => v == null ? 'n/a' : `$${Number(v).toFixed(v < 0.1 ? 6 : 3)}`;
const tokenLabel = (v) => v == null ? 'n/a' : fmt.format(v);

async function loadData(){
  const res = await fetch('./site-data.json');
  return res.json();
}
function bar(container, data, key, max, suffix=''){
  container.innerHTML = data.map(a => {
    const value = a[key];
    const pct = value == null ? 0 : Math.max(3, (value/max)*100);
    const label = key === 'tokens' ? tokenLabel(value) : key === 'cost' ? money(value) : `${value}${suffix}`;
    return `<div class="bar-row"><span>${a.short}</span><div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div><div class="bar-value">${label}</div></div>`;
  }).join('');
}
function renderTable(data){
  const tbody = document.querySelector('#scoreTable tbody');
  tbody.innerHTML = data.map(a => `<tr>
    <td><strong>${a.short}</strong><br><small>${a.model}</small></td>
    <td>${a.wall.toFixed(3)}s</td>
    <td>${tokenLabel(a.tokens)}</td>
    <td>${a.costLabel}</td>
    <td>${a.patch}</td>
    <td>${a.process}</td>
    <td><span class="pill">${a.verdict}</span> ${a.red ? '<span class="pill">red</span>' : ''} ${a.smoke ? '<span class="pill">smoke</span>' : ''}</td>
  </tr>`).join('');
}
function renderTelemetry(data){
  const el = document.getElementById('telemetryCards');
  el.innerHTML = data.map(a => `<article class="tele-card">
    <h3>${a.short}</h3>
    <p>${a.notes}</p>
    <dl>
      <dt>Tokens</dt><dd>${tokenLabel(a.tokens)}</dd>
      <dt>Cost</dt><dd>${a.costLabel}</dd>
      <dt>Messages</dt><dd>${a.messageCount ?? 'n/a'}</dd>
      <dt>Red / green / smoke</dt><dd>${a.red ? '✓' : '—'} / ${a.green ? '✓' : '—'} / ${a.smoke ? '✓' : '—'}</dd>
    </dl>
  </article>`).join('');
}
function drawScatter(data){
  const svg = document.getElementById('frontierChart');
  const w = svg.clientWidth || 760, h = 430, pad = 56;
  svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
  const known = data.filter(d => d.tokens != null);
  const maxX = Math.max(...data.map(d => d.wall))*1.08;
  const maxY = Math.max(...known.map(d => d.tokens))*1.12;
  const x = v => pad + (v/maxX)*(w-pad*1.4);
  const y = v => h-pad - (v/maxY)*(h-pad*1.55);
  const grid = [0,.25,.5,.75,1].map(t => `<line x1="${pad}" x2="${w-pad/2}" y1="${pad+t*(h-pad*1.5)}" y2="${pad+t*(h-pad*1.5)}" stroke="#26324a"/><text x="14" y="${pad+t*(h-pad*1.5)+5}" fill="#7d8aa8" font-size="11">${tokenLabel(Math.round(maxY*(1-t)))}</text>`).join('');
  const circles = data.map((d,i)=>{
    const cx=x(d.wall), cy=d.tokens==null ? h-pad+4 : y(d.tokens);
    const color = d.id==='pi' ? '#88f7b0' : d.id==='opencode' ? '#6ee7ff' : d.id==='agy' ? '#ffbf69' : '#8aa7ff';
    const missing = d.tokens==null;
    const label = `${d.short}${missing?' (tokens n/a)':''}`;
    const nearRightEdge = cx > w - 155;
    const tx = nearRightEdge ? cx - 14 : cx + 14;
    const anchor = nearRightEdge ? 'end' : 'start';
    return `<g><circle cx="${cx}" cy="${cy}" r="${missing?8:11}" fill="${color}" opacity="${missing?0.55:0.95}" stroke="#fff" stroke-opacity=".35"/><text x="${tx}" y="${cy+4}" text-anchor="${anchor}" fill="#edf2ff" font-size="12" font-weight="800">${label}</text></g>`;
  }).join('');
  svg.innerHTML = `${grid}<line x1="${pad}" x2="${w-pad/2}" y1="${h-pad}" y2="${h-pad}" stroke="#53617f"/><line x1="${pad}" x2="${pad}" y1="${pad/2}" y2="${h-pad}" stroke="#53617f"/><text x="${w/2-50}" y="${h-14}" fill="#9aa8c7" font-size="12">wall-clock seconds →</text><text transform="translate(18 ${h/2+80}) rotate(-90)" fill="#9aa8c7" font-size="12">total tokens ↑</text>${circles}`;
}
loadData().then(data => {
  const agents = data.agents;
  bar(document.getElementById('timeBars'), agents, 'wall', Math.max(...agents.map(a=>a.wall)), 's');
  bar(document.getElementById('qualityBars'), [...agents].sort((a,b)=>b.process-a.process), 'process', 100, '');
  const costed = agents.filter(a => a.cost != null).sort((a,b)=>a.cost-b.cost);
  bar(document.getElementById('costBars'), costed, 'cost', Math.max(...costed.map(a=>a.cost)), '');
  renderTable(agents);
  renderTelemetry(agents);
  drawScatter(agents);
  window.addEventListener('resize', () => drawScatter(agents));
});