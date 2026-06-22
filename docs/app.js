const fmt = new Intl.NumberFormat('en-US');
const pct = (v) => `${Math.round(v*100)}%`;
const money = (v) => v == null ? 'n/a' : `$${Number(v).toFixed(v < 0.1 ? 6 : 3)}`;
const tokenLabel = (v) => v == null ? 'n/a' : fmt.format(v);
const agentName = (id) => ({opencode:'OpenCode','claude-code':'Claude',mimo:'MiMo',pi:'Pi','codex-cli':'Codex',agy:'agy'}[id] || id);

async function loadData(){ return (await fetch('./site-data.json')).json(); }
function bar(container, data, key, max, suffix=''){
  container.innerHTML = data.map(a => {
    const value = a[key];
    const width = value == null || !max ? 0 : Math.max(3, (value/max)*100);
    const label = key === 'tokens' ? tokenLabel(value) : key === 'cost' ? money(value) : `${value}${suffix}`;
    return `<div class="bar-row"><span>${a.short}</span><div class="bar-track"><div class="bar-fill" style="width:${width}%"></div></div><div class="bar-value">${label}</div></div>`;
  }).join('');
}
function renderKPIs(data){
  kpiScenarios.textContent=data.kpis.scenarios; kpiRuns.textContent=data.kpis.agentRuns; kpiPass.textContent=pct(data.kpis.passRate); kpiCost.textContent=money(data.kpis.normalizedPublicCost);
  heroPass.textContent=`${data.kpis.passes}/${data.kpis.agentRuns} PASS`;
  heroSummary.textContent=`${data.kpis.scenarios} scenarios, ${data.kpis.agentRuns} agent runs, ${pct(data.kpis.costCoverage)} cost coverage from reliable token telemetry.`;
  const fastest = [...data.agentProfiles].sort((a,b)=>a.avgWall-b.avgWall)[0];
  const cheapest = [...data.agentProfiles].filter(a=>a.avgCost!=null).sort((a,b)=>a.avgCost-b.avgCost)[0];
  const proc = [...data.agentProfiles].sort((a,b)=>b.avgProcess-a.avgProcess)[0];
  heroMini.innerHTML=`<div><span>Fastest avg</span><strong>${fastest.short}</strong></div><div><span>Cheapest avg</span><strong>${cheapest.short}</strong></div><div><span>Best process</span><strong>${proc.short}</strong></div><div><span>Cost coverage</span><strong>${pct(data.kpis.costCoverage)}</strong></div>`;
}
function renderMatrix(data){
  const head=document.querySelector('#scenarioMatrix thead'); const body=document.querySelector('#scenarioMatrix tbody');
  const agents=data.agentProfiles.map(a=>a.id);
  head.innerHTML=`<tr><th>Scenario</th>${agents.map(a=>`<th>${agentName(a)}</th>`).join('')}<th>Fastest</th><th>Cheapest</th><th>Process</th></tr>`;
  body.innerHTML=data.scenarios.map(s=>`<tr><td><strong>${s.id}</strong><br><small>${s.name} · ${s.difficulty}</small></td>${agents.map(a=>{const r=s.agents.find(x=>x.id===a); return `<td><span class="cell-pass">${r.verdict}</span><br><small>${r.wall.toFixed(1)}s · ${r.cost==null?'cost n/a':money(r.cost)}</small></td>`}).join('')}<td>${agentName(s.fastest)}</td><td>${agentName(s.cheapest)}</td><td>${agentName(s.processBest)}</td></tr>`).join('');
  scenarioCards.innerHTML=data.scenarios.map(s=>`<article class="scenario-card"><div class="card-kicker">${s.type} · ${s.difficulty}</div><h3>${s.id}: ${s.name}</h3><p>${s.summary}</p><dl><dt>Passes</dt><dd>${s.passCount}/${s.agentCount}</dd><dt>Fastest</dt><dd>${agentName(s.fastest)}</dd><dt>Cheapest</dt><dd>${agentName(s.cheapest)}</dd><dt>Best process</dt><dd>${agentName(s.processBest)}</dd></dl><a href="../${s.links.results}">Open raw results</a></article>`).join('');
}
function renderProfiles(data){
  agentProfiles.innerHTML=data.agentProfiles.map(a=>`<article class="agent-profile"><h3>${a.short}</h3><div class="profile-score">${pct(a.passRate)}</div><p>${a.label}</p><dl><dt>Avg wall</dt><dd>${a.avgWall}s</dd><dt>Avg process</dt><dd>${a.avgProcess}</dd><dt>Avg cost</dt><dd>${money(a.avgCost)}</dd><dt>Telemetry</dt><dd>${pct(a.telemetryCoverage)}</dd></dl></article>`).join('');
}
function renderTable(agents){
  document.querySelector('#scoreTable tbody').innerHTML = agents.map(a => `<tr><td><strong>${a.short}</strong><br><small>${a.model}</small></td><td>${a.wall.toFixed(3)}s</td><td>${tokenLabel(a.tokens)}</td><td>${a.cost==null?'n/a':money(a.cost)}</td><td>${a.patch}</td><td>${a.process}</td><td><span class="pill">${a.verdict}</span> ${a.red ? '<span class="pill">red</span>' : ''} ${a.smoke ? '<span class="pill">smoke</span>' : ''}</td></tr>`).join('');
}
function drawScatter(svgId, data, xKey, yKey, opts={}){
  const svg=document.getElementById(svgId); const w=svg.clientWidth||760,h=420,pad=58;
  svg.setAttribute('viewBox',`0 0 ${w} ${h}`);
  const known=data.filter(d=>d[xKey]!=null && d[yKey]!=null);
  const maxX=Math.max(...known.map(d=>d[xKey]),1)*1.15; const maxY=Math.max(...known.map(d=>d[yKey]),1)*1.15;
  const x=v=>pad+(v/maxX)*(w-pad*1.5); const y=v=>h-pad-(v/maxY)*(h-pad*1.6);
  const points=data.map(d=>{ const missing=d[xKey]==null||d[yKey]==null; const cx=missing?w-pad*1.2:x(d[xKey]); const cy=missing?h-pad+8:y(d[yKey]); const color=d.id==='pi'?'#88f7b0':d.id==='opencode'?'#6ee7ff':d.id==='agy'?'#ffbf69':d.id==='codex-cli'?'#ff6ea8':'#8aa7ff'; return `<g><circle cx="${cx}" cy="${cy}" r="${missing?8:11}" fill="${color}" opacity="${missing?.5:.95}" stroke="#fff" stroke-opacity=".35"/><text x="${cx+13}" y="${cy+4}" fill="#edf2ff" font-size="12" font-weight="800">${d.short}${missing?' (n/a)':''}</text></g>`}).join('');
  svg.innerHTML=`<line x1="${pad}" x2="${w-pad/2}" y1="${h-pad}" y2="${h-pad}" stroke="#53617f"/><line x1="${pad}" x2="${pad}" y1="${pad/2}" y2="${h-pad}" stroke="#53617f"/><text x="${w/2-70}" y="${h-14}" fill="#9aa8c7" font-size="12">${opts.xLabel||xKey} →</text><text transform="translate(18 ${h/2+80}) rotate(-90)" fill="#9aa8c7" font-size="12">${opts.yLabel||yKey} ↑</text>${points}`;
}
function renderArtifacts(data){
  artifactGrid.innerHTML=data.scenarios.flatMap(s=>[
    `<a href="../${s.links.results}"><strong>${s.id} results</strong><span>${s.name}</span></a>`,
    `<a href="../${s.links.json}"><strong>${s.id} metrics JSON</strong><span>machine-readable run facts</span></a>`
  ]).join('');
}
loadData().then(data=>{
  renderKPIs(data); renderMatrix(data); renderProfiles(data); renderArtifacts(data);
  drawScatter('paretoChart', data.agentProfiles.map(a=>({id:a.id,short:a.short,cost:a.avgCost,process:a.avgProcess})), 'cost','process',{xLabel:'avg normalized public cost', yLabel:'avg process score'});
  const latest=data.latestScenario; detailTitle.textContent=`${latest.id}: ${latest.name}`; detailSummary.textContent=latest.summary;
  const agents=latest.agents; bar(timeBars, agents, 'wall', Math.max(...agents.map(a=>a.wall)), 's'); bar(qualityBars, [...agents].sort((a,b)=>b.process-a.process), 'process', 100, ''); const costed=agents.filter(a=>a.cost!=null).sort((a,b)=>a.cost-b.cost); bar(costBars, costed, 'cost', Math.max(...costed.map(a=>a.cost)), ''); renderTable(agents); drawScatter('frontierChart', agents, 'wall','tokens',{xLabel:'wall-clock seconds', yLabel:'total tokens'});
  window.addEventListener('resize',()=>{drawScatter('paretoChart', data.agentProfiles.map(a=>({id:a.id,short:a.short,cost:a.avgCost,process:a.avgProcess})), 'cost','process',{xLabel:'avg normalized public cost', yLabel:'avg process score'}); drawScatter('frontierChart', agents, 'wall','tokens',{xLabel:'wall-clock seconds', yLabel:'total tokens'});});
});
