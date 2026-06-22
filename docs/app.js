/* ═══════════════════════════════════════════════════════════════════════════
   Coding Agent Battles — Benchmark Briefing Room
   All data sourced from site-data.json. No hardcoded benchmark numbers.
   Null-safe throughout: if a field is null/undefined, gracefully degrade.
   ═══════════════════════════════════════════════════════════════════════════ */

'use strict';

/* ── Formatting helpers ─────────────────────────────────────────────────── */
const fmt    = new Intl.NumberFormat('en-US');
const pct    = (v) => (v == null) ? 'n/a' : `${Math.round(v * 100)}%`;
const money  = (v) => (v == null) ? 'n/a' : `$${Number(v).toFixed(v < 0.1 ? 4 : 2)}`;
const moneyFull = (v) => (v == null) ? 'n/a' : `$${Number(v).toFixed(v < 0.01 ? 6 : v < 1 ? 4 : 2)}`;
const sec    = (v) => (v == null) ? 'n/a' : `${Number(v).toFixed(1)}s`;
const toks   = (v) => (v == null) ? 'n/a' : fmt.format(v);
const safe   = (v, fallback = 'n/a') => (v == null || v === '' || v === 'n/a') ? fallback : v;
const escapeHtml = (v) => String(v ?? '')
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&#039;');

const AGENT_DISPLAY = {
  'opencode':   'OpenCode',
  'claude-code':'Claude',
  'mimo':       'MiMo',
  'pi':         'Pi',
  'codex-cli':  'Codex',
  'agy':        'agy',
};
const agentDisplay = (id) => AGENT_DISPLAY[id] || id;

function vendorCostNote(a) {
  if (!knownNumber(a?.vendorCost) || !knownNumber(a?.cost)) return '';
  if (Math.abs(Number(a.vendorCost) - Number(a.cost)) < 0.000001) return '';
  return `<span class="spa-metric-sub">native ${moneyFull(a.vendorCost)}</span>`;
}

const AGENT_COLORS = {
  'pi':         '#34d17a',
  'opencode':   '#4f8ef7',
  'claude-code':'#a78bfa',
  'mimo':       '#f5a623',
  'codex-cli':  '#f87171',
  'agy':        '#22d3ee',
};
const agentColor = (id) => AGENT_COLORS[id] || '#8a9ab8';

function knownNumber(v) {
  return typeof v === 'number' && Number.isFinite(v);
}

function renderEmptyState(containerId, title, body, meta = '') {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = `
    <div class="viz-empty" role="note">
      <div class="viz-empty-title">${safe(title)}</div>
      <div class="viz-empty-body">${safe(body)}</div>
      ${meta ? `<div class="viz-empty-meta">${safe(meta)}</div>` : ''}
    </div>
  `;
}

function bestProcessLabel(agents, fallbackId) {
  const known = (agents || []).filter(a => knownNumber(a.process));
  if (!known.length) return agentDisplay(fallbackId);
  const max = Math.max(...known.map(a => a.process));
  const tied = known.filter(a => a.process === max);
  if (tied.length > 1) return `${tied.length} tied (${max})`;
  return safe(tied[0].short, agentDisplay(tied[0].id));
}

function markdownToHtml(markdown) {
  const lines = String(markdown || '').split(/\r?\n/);
  const out = [];
  let inList = false;
  let inTable = false;
  const closeList = () => { if (inList) { out.push('</ul>'); inList = false; } };
  const closeTable = () => { if (inTable) { out.push('</tbody></table></div>'); inTable = false; } };
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (!line.trim()) { closeList(); closeTable(); continue; }
    if (/^\|.+\|$/.test(line.trim())) {
      closeList();
      const cells = line.trim().slice(1, -1).split('|').map(c => escapeHtml(c.trim()));
      const isSep = cells.every(c => /^:?-{3,}:?$/.test(c));
      if (isSep) continue;
      if (!inTable) { out.push('<div class="artifact-table-wrap"><table class="artifact-table"><tbody>'); inTable = true; }
      const tag = lines[i + 1] && /^\|\s*:?-{3,}:?/.test(lines[i + 1]) ? 'th' : 'td';
      out.push(`<tr>${cells.map(c => `<${tag}>${c}</${tag}>`).join('')}</tr>`);
      continue;
    }
    closeTable();
    const h = line.match(/^(#{1,3})\s+(.+)$/);
    if (h) { closeList(); out.push(`<h${h[1].length + 2}>${escapeHtml(h[2])}</h${h[1].length + 2}>`); continue; }
    const li = line.match(/^[-*]\s+(.+)$/);
    if (li) { if (!inList) { out.push('<ul>'); inList = true; } out.push(`<li>${escapeHtml(li[1])}</li>`); continue; }
    closeList();
    out.push(`<p>${escapeHtml(line)}</p>`);
  }
  closeList(); closeTable();
  return out.join('');
}

/* ── Data loader ────────────────────────────────────────────────────────── */
const BUILD_VERSION = (() => {
  try {
    return new URL(import.meta.url).searchParams.get('v') || 'dev';
  } catch (_) {
    return 'dev';
  }
})();

async function loadData() {
  const isScenarioPage = document.body.dataset.page === 'scenario';
  const dataPath = isScenarioPage ? '../site-data.json' : './site-data.json';
  const sep = dataPath.includes('?') ? '&' : '?';
  const res = await fetch(`${dataPath}${sep}v=${encodeURIComponent(BUILD_VERSION)}`, { cache: 'no-store' });
  if (!res.ok) throw new Error(`Failed to load site-data.json: ${res.status}`);
  return res.json();
}

/* ── DOM helpers ────────────────────────────────────────────────────────── */
function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

function setHTML(id, html) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = html;
}

/* ── KPI Strip ──────────────────────────────────────────────────────────── */
function renderKPIs(data) {
  const k = data.kpis || {};
  setText('kpi-scenarios', safe(k.scenarios));
  setText('kpi-runs',      safe(k.agentRuns));
  setText('kpi-pass',      pct(k.passRate));
  setText('kpi-cost',      money(k.normalizedPublicCost));
}

/* ── Above-the-fold verdict card ────────────────────────────────────────── */
function renderVerdict(data) {
  const k = data.kpis || {};
  setText('atf-dateline', `Generated ${data.generated || '—'} · ${data.repo || ''}`);
  setText('verdict-score', `${safe(k.passes, '?')}/${safe(k.agentRuns, '?')} PASS`);
  setText('verdict-sub',
    `${safe(k.scenarios, '?')} scenarios · ${safe(k.agentRuns, '?')} agent runs · ` +
    `${pct(k.costCoverage)} cost coverage from reliable token telemetry`
  );

  const profiles = data.agentProfiles || [];
  const fastest  = [...profiles].sort((a, b) => (a.avgWall || 9e9) - (b.avgWall || 9e9))[0];
  const cheapest = [...profiles].filter(a => a.avgCost != null).sort((a, b) => a.avgCost - b.avgCost)[0];
  const bestProc = [...profiles].sort((a, b) => (b.avgProcess || 0) - (a.avgProcess || 0))[0];

  const stats = [
    { label: 'Fastest avg',   value: fastest  ? fastest.short  : 'n/a' },
    { label: 'Cheapest avg',  value: cheapest ? cheapest.short : 'n/a' },
    { label: 'Best execution',  value: bestProc ? bestProc.short : 'n/a' },
    { label: 'Cost coverage', value: pct(k.costCoverage) },
  ];

  setHTML('verdict-stats', stats.map(s => `
    <div class="verdict-stat">
      <span class="verdict-stat-label">${s.label}</span>
      <span class="verdict-stat-value">${s.value}</span>
    </div>
  `).join(''));
}

/* ── Scenario Cards (Home Page) ────────────────────────────────────────── */
function renderScenarioCards(data) {
  const scenarios = data.scenarios || [];
  const html = scenarios.map(s => {
    return `
      <a href="./scenarios/${s.slug}.html" class="scenario-card-link">
        <div class="scenario-card">
          <div class="sp-meta">
            <div class="sp-id">${s.id} · ${safe(s.type)}</div>
            <div class="sp-name">${safe(s.name)}</div>
            <div class="sp-summary">${safe(s.summary)}</div>
          </div>
          <div class="scenario-card-footer">
            <span>View scenario details →</span>
          </div>
        </div>
      </a>
    `;
  }).join('');
  setHTML('scenario-cards', html);
}

/* ── Agent profiles table ──────────────────────────────────────────────── */
function renderAgentTable(data) {
  const profiles = data.agentProfiles || [];
  const maxWall  = Math.max(...profiles.map(a => a.avgWall  || 0), 1);
  const maxCost  = Math.max(...profiles.filter(a => a.avgCost  != null).map(a => a.avgCost),  1);
  const maxToks  = Math.max(...profiles.filter(a => a.totalTokens != null).map(a => a.totalTokens), 1);

  const rows = profiles.map(a => {
    const wallW  = ((a.avgWall     || 0) / maxWall) * 100;
    const procW  = (a.avgProcess   || 0);
    const costW  = a.avgCost  != null ? (a.avgCost  / maxCost) * 100 : 0;
    const toksW  = a.totalTokens != null ? (a.totalTokens / maxToks) * 100 : 0;
    const covClass = a.telemetryCoverage >= 1 ? 'coverage-full'
                   : a.telemetryCoverage  > 0 ? 'coverage-partial'
                   : 'coverage-none';
    const covLabel = a.telemetryCoverage >= 1 ? '100% telemetry'
                   : a.telemetryCoverage  > 0 ? `${pct(a.telemetryCoverage)} telemetry`
                   : 'no telemetry';
    const passRateW = knownNumber(a.passRate) ? a.passRate * 100 : 0;

    return `
      <tr>
        <td>
          <div class="at-name">${safe(a.short, a.id)}</div>
          <div class="at-model">${safe(a.label)}</div>
        </td>
        <td>
          <div class="bar-mini-wrap">
            <div class="bar-mini-track">
              <div class="bar-mini-fill bar-fill-process" style="width:${passRateW.toFixed(1)}%"></div>
            </div>
            <span class="bar-mini-value">${safe(a.passes, 0)}/${safe(a.runs, 0)} · ${pct(a.passRate)}</span>
          </div>
        </td>
        <td>
          <div class="bar-mini-wrap">
            <div class="bar-mini-track">
              <div class="bar-mini-fill bar-fill-speed" style="width:${wallW.toFixed(1)}%"></div>
            </div>
            <span class="bar-mini-value">${sec(a.avgWall)}</span>
          </div>
        </td>
        <td>
          <div class="bar-mini-wrap">
            <div class="bar-mini-track">
              <div class="bar-mini-fill bar-fill-process" style="width:${procW}%"></div>
            </div>
            <span class="bar-mini-value">${safe(a.avgProcess, 'n/a')}</span>
          </div>
        </td>
        <td>
          <div class="bar-mini-wrap">
            <div class="bar-mini-track">
              <div class="bar-mini-fill bar-fill-cost" style="width:${costW.toFixed(1)}%"></div>
            </div>
            <span class="bar-mini-value">${money(a.avgCost)}</span>
          </div>
        </td>
        <td>
          <div class="bar-mini-wrap">
            <div class="bar-mini-track">
              <div class="bar-mini-fill bar-fill-tokens" style="width:${toksW.toFixed(1)}%"></div>
            </div>
            <span class="bar-mini-value">${toks(a.totalTokens)}</span>
          </div>
        </td>
        <td><span class="coverage-badge ${covClass}">${covLabel}</span></td>
      </tr>
    `;
  }).join('');

  setHTML('agent-table', `
    <table class="agent-table">
      <thead>
        <tr>
          <th>Agent</th>
          <th>Pass rate</th>
          <th>Avg wall</th>
          <th>Avg execution</th>
          <th>Avg cost (est.)</th>
          <th>Total tokens</th>
          <th>Telemetry</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `);
}

/* ── D3 Scatter charts ──────────────────────────────────────────────────── */
function drawD3Scatter(svgId, points, xKey, yKey, opts = {}) {
  const container = document.getElementById(svgId);
  if (!container || !window.d3) return;
  
  // Clear previous
  container.innerHTML = '';

  const known = points.filter(p => knownNumber(p[xKey]) && knownNumber(p[yKey]));
  if (!known.length) {
    renderEmptyState(
      svgId,
      opts.emptyTitle || 'Telemetry unavailable',
      opts.emptyBody || `No reliable ${opts.yLabel || yKey} data is available for this scenario yet.`,
      opts.emptyMeta || 'The verified pass/fail and wall-clock evidence is still present in the cards and table.'
    );
    return;
  }

  const W = container.clientWidth || 820;
  const defaultHeight = svgId === 'frontierChart'
    ? Math.max(440, container.clientHeight || 0)
    : 360;
  const H = defaultHeight;
  const pad = svgId === 'frontierChart'
    ? { top: 22, right: 150, bottom: 68, left: 92 }
    : { top: 20, right: 145, bottom: 54, left: 68 };
  const innerW = W - pad.left - pad.right;
  const innerH = H - pad.top - pad.bottom;

  const svg = d3.select(container).append('svg')
    .attr('width', '100%')
    .attr('height', H)
    .attr('viewBox', `0 0 ${W} ${H}`)
    .style('overflow', 'visible');

  const maxX = known.length ? d3.max(known, d => d[xKey]) * 1.12 : 1;
  const maxY = known.length ? d3.max(known, d => d[yKey]) * 1.12 : 1;
  const minY = known.length ? Math.max(0, d3.min(known, d => d[yKey]) * 0.78) : 0;

  const xScale = d3.scaleLinear()
    .domain([0, maxX])
    .range([pad.left, pad.left + innerW]);

  const yScale = d3.scaleLinear()
    .domain([minY, maxY])
    .range([pad.top + innerH, pad.top]);

  const axisColor = '#2a3a58';
  const textColor = '#5a6a88';

  // Axes + grid
  const xAxis = d3.axisBottom(xScale).ticks(6).tickSizeOuter(0);
  const yAxis = d3.axisLeft(yScale).ticks(6).tickSizeOuter(0).tickFormat(d => d >= 1000 ? `${fmt.format(Math.round(d / 1000))}k` : fmt.format(d));

  svg.append('g')
    .attr('class', 'chart-grid')
    .attr('transform', `translate(0,${pad.top + innerH})`)
    .call(d3.axisBottom(xScale).ticks(6).tickSize(-innerH).tickFormat(''))
    .call(g => g.select('.domain').remove())
    .call(g => g.selectAll('line').attr('stroke', 'rgba(138,154,184,.10)'));

  svg.append('g')
    .attr('class', 'chart-grid')
    .attr('transform', `translate(${pad.left},0)`)
    .call(d3.axisLeft(yScale).ticks(6).tickSize(-innerW).tickFormat(''))
    .call(g => g.select('.domain').remove())
    .call(g => g.selectAll('line').attr('stroke', 'rgba(138,154,184,.10)'));

  svg.append('g')
    .attr('transform', `translate(0,${pad.top + innerH})`)
    .call(xAxis)
    .call(g => g.select('.domain').attr('stroke', axisColor))
    .call(g => g.selectAll('line').attr('stroke', axisColor))
    .call(g => g.selectAll('text').attr('fill', textColor).attr('font-family', 'var(--font-sans)').attr('font-size', '12px').attr('font-weight', '650'));

  svg.append('g')
    .attr('transform', `translate(${pad.left},0)`)
    .call(yAxis)
    .call(g => g.select('.domain').attr('stroke', axisColor))
    .call(g => g.selectAll('line').attr('stroke', axisColor))
    .call(g => g.selectAll('text').attr('fill', textColor).attr('font-family', 'var(--font-sans)').attr('font-size', '12px').attr('font-weight', '650'));

  // Labels
  svg.append('text')
    .attr('x', pad.left + innerW / 2)
    .attr('y', H - 10)
    .attr('fill', textColor)
    .attr('font-size', '12px')
    .attr('text-anchor', 'middle')
    .attr('font-family', 'var(--font-sans)')
    .text(opts.xLabel || xKey);

  svg.append('text')
    .attr('transform', `rotate(-90)`)
    .attr('x', -(pad.top + innerH / 2))
    .attr('y', 15)
    .attr('fill', textColor)
    .attr('font-size', '12px')
    .attr('text-anchor', 'middle')
    .attr('font-family', 'var(--font-sans)')
    .text(opts.yLabel || yKey);

  // Missing data points area
  const missingPoints = points.filter(p => !knownNumber(p[xKey]) || !knownNumber(p[yKey]));
  
  // Plot dots
  const allPoints = svg.selectAll('.dot')
    .data(points)
    .enter()
    .append('g')
    .attr('class', 'dot')
    .attr('transform', d => {
      const missing = !knownNumber(d[xKey]) || !knownNumber(d[yKey]);
      const missIndex = missingPoints.findIndex(p => p.id === d.id);
      const cx = missing ? pad.left + innerW + 15 : xScale(d[xKey]);
      const cy = missing ? pad.top + innerH - 20 - Math.max(0, missIndex) * 24 : yScale(d[yKey]);
      return `translate(${cx},${cy})`;
    });

  allPoints.append('circle')
    .attr('r', d => (!knownNumber(d[xKey]) || !knownNumber(d[yKey])) ? 7 : 10)
    .attr('fill', d => agentColor(d.id))
    .attr('opacity', d => (!knownNumber(d[xKey]) || !knownNumber(d[yKey])) ? 0.45 : 1)
    .attr('stroke', 'rgba(255,255,255,.25)')
    .attr('stroke-width', 1.5)
    // subtle hover effect
    .on('mouseover', function() { d3.select(this).attr('r', 12); })
    .on('mouseout', function(e, d) { d3.select(this).attr('r', (!knownNumber(d[xKey]) || !knownNumber(d[yKey])) ? 7 : 10); });

  allPoints.append('text')
    .attr('x', d => (!knownNumber(d[xKey]) || !knownNumber(d[yKey])) ? 12 : 15)
    .attr('y', 4)
    .attr('fill', '#e8edf8')
    .attr('font-size', '12px')
    .attr('font-weight', '700')
    .attr('font-family', 'var(--font-sans)')
    .text(d => {
      const missing = !knownNumber(d[xKey]) || !knownNumber(d[yKey]);
      return missing && opts.missingXLabel ? `${d.short} (${opts.missingXLabel})` : d.short;
    });
}

function drawPareto(data) {
  const points = (data.agentProfiles || []).map(a => ({
    id:      a.id,
    short:   a.short || a.id,
    cost:    a.avgCost,
    process: a.avgProcess || 0,
  }));
  drawD3Scatter('paretoChart', points, 'cost', 'process', {
    xLabel: 'Avg Normalized Public Cost (USD)',
    yLabel: 'Avg Execution Score (0–100)',
    missingXLabel: 'cost n/a',
  });
}

function drawLatencyProcessChart(data) {
  const points = (data.agentProfiles || []).map(a => ({
    id:      a.id,
    short:   a.short || a.id,
    wall:    a.avgWall,
    process: a.avgProcess || 0,
  }));
  drawD3Scatter('latencyProcessChart', points, 'wall', 'process', {
    xLabel: 'Avg Wall-Clock Time (s)',
    yLabel: 'Avg Execution Score (0–100)',
    missingXLabel: 'wall n/a',
  });
}

function renderScenarioNavigator(data, currentScenario) {
  const scenarios = data.scenarios || [];
  const idx = scenarios.findIndex(s => s.slug === currentScenario.slug || s.id === currentScenario.id);
  const prev = scenarios[(idx - 1 + scenarios.length) % scenarios.length];
  const next = scenarios[(idx + 1) % scenarios.length];
  const rel = (s) => `../scenarios/${s.slug}.html`;
  const status = (s) => `${safe(s.passCount, 0)}/${safe(s.agentCount, 0)} pass`;
  const chips = scenarios.map((s, i) => `
    <a class="scenario-rail-chip ${s.id === currentScenario.id ? 'is-active' : ''}" href="${rel(s)}" aria-label="Open ${s.id}: ${escapeHtml(s.name)}">
      <span class="scenario-rail-index">${String(i + 1).padStart(2, '0')}</span>
      <span class="scenario-rail-id">${s.id.replace('BB-', 'BB')}</span>
    </a>
  `).join('');
  const cards = scenarios.map(s => `
    <a class="scenario-map-card ${s.id === currentScenario.id ? 'is-active' : ''}" href="${rel(s)}">
      <div class="scenario-map-top">
        <span>${s.id}</span>
        <span>${safe(s.difficulty)}</span>
      </div>
      <strong>${safe(s.name)}</strong>
      <p>${safe(s.type)} · ${status(s)}</p>
    </a>
  `).join('');

  return `
    <nav class="scenario-switcher" aria-label="Scenario navigation">
      <a class="scenario-step" href="${rel(prev)}" aria-label="Previous scenario">
        <span class="scenario-step-kicker">← Previous</span>
        <strong>${prev.id}</strong>
      </a>
      <div class="scenario-rail-wrap">
        <div class="scenario-rail-head">
          <span>Scenario rail</span>
          <span>${idx + 1} / ${scenarios.length}</span>
        </div>
        <div class="scenario-rail" role="list">${chips}</div>
      </div>
      <a class="scenario-step scenario-step-next" href="${rel(next)}" aria-label="Next scenario">
        <span class="scenario-step-kicker">Next →</span>
        <strong>${next.id}</strong>
      </a>
      <details class="scenario-map">
        <summary>Browse all scenarios</summary>
        <div class="scenario-map-grid">${cards}</div>
      </details>
    </nav>
  `;
}

/* ── Scenario Detail (For scenario pages) ──────────────────────────────── */
function renderScenarioDetail(data, scenarioId) {
  const s = (data.scenarios || []).find(x => x.slug === scenarioId || x.id.toLowerCase() === scenarioId);
  if (!s) {
    setText('detail-title', 'Scenario not found');
    return;
  }

  setText('detail-title', `${s.id}: ${safe(s.name)}`);
  setText('detail-summary', safe(s.summary));

  const agents = s.agents || [];

  // Winners
  const winnersHtml = [
    { label: 'Fastest passing', value: agentDisplay(s.fastest) },
    { label: 'Cheapest passing', value: s.cheapest ? agentDisplay(s.cheapest) : 'n/a — no cost telemetry' },
    { label: 'Best execution', value: bestProcessLabel(agents, s.processBest) },
  ].map(w => `
    <div class="winner-badge">
      <span class="winner-badge-label">${w.label}</span>
      <span class="winner-badge-value">${safe(w.value)}</span>
    </div>
  `).join('');

  // Agent Cards
  const agentCardsHtml = agents.map(a => {
    const pills = [
      a.verdict ? `<span class="pill ${a.verdict === 'PASS' ? 'pill-pass' : 'pill-fail'}">${a.verdict}</span>` : '',
      a.red   ? `<span class="pill pill-red">red✓</span>` : '',
      a.smoke ? `<span class="pill pill-smoke">smoke✓</span>` : '',
    ].filter(Boolean).join('');

    return `
      <div class="sp-agent-card">
        <div class="spa-name">${safe(a.short, a.id)}</div>
        <div class="spa-model">${safe(a.model)}</div>
        <div class="spa-metrics">
          <div class="spa-metric">
            <span class="spa-metric-label">Wall</span>
            <span class="spa-metric-value">${sec(a.wall)}</span>
          </div>
          <div class="spa-metric">
            <span class="spa-metric-label">Execution</span>
            <span class="spa-metric-value">${safe(a.process, 'n/a')}</span>
          </div>
          <div class="spa-metric">
            <span class="spa-metric-label">Cost</span>
            <span class="spa-metric-value">${moneyFull(a.cost)}${vendorCostNote(a)}</span>
          </div>
          <div class="spa-metric">
            <span class="spa-metric-label">Tokens</span>
            <span class="spa-metric-value">${toks(a.tokens)}</span>
          </div>
        </div>
        <div class="spa-pills">${pills}</div>
      </div>
    `;
  }).join('');

  const links = s.links || {};
  const scenarioNavHtml = renderScenarioNavigator(data, s);
  const artifactButtons = [
    links.results ? { kind: 'results', label: 'Results', href: `../${links.results}` } : null,
    links.metrics ? { kind: 'metrics', label: 'Metrics', href: `../${links.metrics}` } : null,
    links.json    ? { kind: 'json',    label: 'JSON',    href: `../${links.json}` } : null,
  ].filter(Boolean);
  const linksHtml = artifactButtons.map((b, i) => `
    <button class="sp-link sp-link-button" type="button" data-artifact-kind="${b.kind}" data-artifact-href="${b.href}" aria-pressed="${i === 0 ? 'true' : 'false'}">${b.label}</button>
  `).join('');

  const warningsHtml = (s.provenanceWarnings || []).length
    ? `<div class="scenario-warnings">${s.provenanceWarnings.map(w => `<div class="scenario-warning"><strong>${safe(w.label || 'Provenance note')}</strong><span>${safe(w.detail || w)}</span></div>`).join('')}</div>`
    : '';

  setHTML('scenario-panel', `
    ${scenarioNavHtml}
    ${warningsHtml}
    <div class="sp-header">
      <div class="sp-meta">
        <div class="sp-id">${s.id} · ${safe(s.type)} · ${safe(s.difficulty)}</div>
        <div class="sp-name">${safe(s.name)}</div>
        <div class="sp-summary">${safe(s.summary)}</div>
        <div class="sp-method-note">Cost winners use each agent’s configured model price; this is scaffold+model economics, not a pure scaffold-only price comparison.</div>
      </div>
      <div class="sp-winners">${winnersHtml}</div>
    </div>
    <div class="sp-agents">${agentCardsHtml}</div>
    <div class="badge-legend" aria-label="Scenario badge legend">
      <span><b class="pill pill-red">red✓</b> agent captured failing baseline</span>
      <span><b class="pill pill-smoke">smoke✓</b> agent ran user-visible smoke</span>
    </div>
    <div class="sp-links" role="tablist" aria-label="Scenario evidence artifacts">${linksHtml}</div>
    <section class="artifact-viewer" id="artifactViewer" aria-live="polite" hidden>
      <div class="artifact-viewer-head">
        <span id="artifactViewerTitle">Evidence artifact</span>
        <a id="artifactViewerRaw" class="inline-link" href="#" target="_blank" rel="noopener">Open raw ↗</a>
      </div>
      <div class="artifact-viewer-body" id="artifactViewerBody"></div>
    </section>
  `);
  initArtifactViewer(artifactButtons);

  // Bar charts
  const maxWall  = Math.max(...agents.map(a => a.wall  || 0), 1);
  const maxCost  = Math.max(...agents.filter(a => a.cost != null).map(a => a.cost), 1);

  renderBarList('timeBars', agents,
    a => ({ label: safe(a.short, a.id), val: a.wall, max: maxWall, suffix: 's', colorClass: 'bar-fill-time' })
  );

  const knownProcess = agents.filter(a => knownNumber(a.process));
  const processValues = [...new Set(knownProcess.map(a => a.process))];
  renderBarList('qualityBars', [...agents].sort((a,b) => (b.process||0)-(a.process||0)),
    a => ({ label: safe(a.short, a.id), val: a.process, max: 100, suffix: '', colorClass: 'bar-fill-quality' }),
    {
      emptyTitle: 'Execution scores unavailable',
      emptyBody: 'No execution composite values were recorded for this scenario.',
      note: processValues.length === 1
        ? `All ${knownProcess.length} agents share the same execution score (${processValues[0]}). Compare wall-clock, tokens, and evidence links instead.`
        : ''
    }
  );

  renderBarList('costBars',
    agents.filter(a => knownNumber(a.cost)).sort((a,b) => a.cost - b.cost),
    a => ({ label: safe(a.short, a.id), val: a.cost, max: maxCost, suffix: '', colorClass: 'bar-fill-cost-d', format: moneyFull }),
    {
      emptyTitle: 'Cost telemetry not attributed yet',
      emptyBody: 'No reliable token/cost attribution exists for this scenario. Verified pass/fail and wall-clock evidence are still shown above.',
      emptyMeta: 'Next step: ccusage-first telemetry extraction, then normalized public cost calculation.'
    }
  );

  // Scatter (wall vs tokens)
  const scatterPoints = agents.map(a => ({
    id: a.id, short: safe(a.short, a.id), wall: a.wall, tokens: a.tokens
  }));
  drawD3Scatter('frontierChart', scatterPoints, 'wall', 'tokens', {
    xLabel: 'Wall-clock (s)',
    yLabel: 'Total Tokens',
    missingXLabel: 'tokens n/a',
    emptyTitle: 'Token telemetry not attributed yet',
    emptyBody: 'This scenario has verified wall-clock and pass/fail evidence, but no reliable per-agent token totals yet.',
    emptyMeta: 'The fake 0–1 axis has been removed; this panel will render a scatter plot once token data exists.',
  });

  // Score table
  renderScoreTable(agents, s.links || {});
}

async function loadArtifactIntoViewer(button) {
  const titleEl = document.getElementById('artifactViewerTitle');
  const rawEl = document.getElementById('artifactViewerRaw');
  const bodyEl = document.getElementById('artifactViewerBody');
  const viewer = document.getElementById('artifactViewer');
  if (!button || !titleEl || !rawEl || !bodyEl || !viewer) return;
  viewer.hidden = false;
  document.querySelectorAll('[data-artifact-href]').forEach(b => b.setAttribute('aria-pressed', b === button ? 'true' : 'false'));

  const href = button.dataset.artifactHref;
  const kind = button.dataset.artifactKind;
  if (titleEl) titleEl.textContent = `${button.textContent} artifact`;
  if (rawEl) rawEl.href = href;
  bodyEl.innerHTML = '<div class="viz-empty-body">Loading artifact…</div>';
  try {
    const res = await fetch(href, { cache: 'no-store' });
    if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
    const text = await res.text();
    if (kind === 'json') {
      const obj = JSON.parse(text);
      bodyEl.innerHTML = `<pre class="artifact-code">${escapeHtml(JSON.stringify(obj, null, 2))}</pre>`;
    } else {
      bodyEl.innerHTML = `<div class="artifact-markdown">${markdownToHtml(text)}</div>`;
    }
  } catch (err) {
    bodyEl.innerHTML = `<div class="viz-empty"><div class="viz-empty-title">Could not load artifact</div><div class="viz-empty-body">${escapeHtml(err.message || err)}</div></div>`;
  }
}

function initArtifactViewer(buttons) {
  const viewer = document.getElementById('artifactViewer');
  const nodes = [...document.querySelectorAll('[data-artifact-href]')];
  if (!viewer || !nodes.length) return;
  nodes.forEach(btn => btn.addEventListener('click', () => loadArtifactIntoViewer(btn)));
}

function renderBarList(containerId, agents, mapper, opts = {}) {
  const el = document.getElementById(containerId);
  if (!el) return;
  if (!agents.length) {
    renderEmptyState(
      containerId,
      opts.emptyTitle || 'No datapoints',
      opts.emptyBody || 'There are no reliable datapoints for this panel yet.',
      opts.emptyMeta || ''
    );
    return;
  }
  el.innerHTML = agents.map(a => {
    const m = mapper(a);
    const pct = (m.val == null || !m.max) ? 0 : Math.max(3, (m.val / m.max) * 100);
    const display = m.format ? m.format(m.val) : (m.val == null ? 'n/a' : `${m.val}${m.suffix}`);
    // Reuse some existing classes
    let colorCls = m.colorClass;
    if (colorCls === 'bar-fill-time') colorCls = 'bar-fill-speed';
    if (colorCls === 'bar-fill-quality') colorCls = 'bar-fill-process';
    if (colorCls === 'bar-fill-cost-d') colorCls = 'bar-fill-cost';

    return `
      <div class="bar-row">
        <span class="bar-row-label">${m.label}</span>
        <div class="bar-track">
          <div class="bar-fill ${colorCls}" style="width:${pct.toFixed(1)}%; height: 100%; border-radius: 999px;"></div>
        </div>
        <span class="bar-row-value">${display}</span>
      </div>
    `;
  }).join('') + (opts.note ? `<div class="bar-note">${safe(opts.note)}</div>` : '');
}

function renderScoreTable(agents, links) {
  const tbody = document.querySelector('#scoreTable tbody');
  if (!tbody) return;
  tbody.innerHTML = agents.map(a => {
    const pills = [
      `<span class="pill ${a.verdict === 'PASS' ? 'pill-pass' : 'pill-fail'}">${safe(a.verdict)}</span>`,
      a.red   ? `<span class="pill pill-red">red</span>` : '',
      a.smoke ? `<span class="pill pill-smoke">smoke</span>` : '',
    ].filter(Boolean).join(' ');

    return `
      <tr>
        <td>
          <strong>${safe(a.short, a.id)}</strong><br>
          <small style="font-family:var(--font-mono);color:var(--ink-dim);font-size:11px">${safe(a.model)}</small>
        </td>
        <td>${sec(a.wall)}</td>
        <td>${toks(a.tokens)}</td>
        <td>${moneyFull(a.cost)}</td>
        <td>${safe(a.patch, 'n/a')}</td>
        <td>${safe(a.process, 'n/a')}</td>
        <td>${pills}</td>
      </tr>
    `;
  }).join('');
}

/* ── ccusage / Method body ───────────────────────────────────────────────── */
function renderMethodBody(data) {
  const pb = data.pricingBasis || {};
  const tb = data.telemetryBasis || {};

  const formula = pb.normalized_public_estimate_formula || '';
  const models  = pb.models || {};
  const limits  = pb.limitations || [];

  const pricingCards = Object.entries(models).map(([model, m]) => `
    <div class="pricing-card">
      <div class="pricing-card-name">${model}</div>
      <dl>
        <dt>Source</dt><dd>${safe(m.source)}</dd>
        <dt>Input /MTok</dt><dd>$${m.input_per_mtok != null ? m.input_per_mtok.toFixed(2) : 'n/a'}</dd>
        <dt>Cached /MTok</dt><dd>$${m.cached_input_per_mtok != null ? m.cached_input_per_mtok.toFixed(2) : 'n/a'}</dd>
        <dt>Output /MTok</dt><dd>$${m.output_per_mtok != null ? m.output_per_mtok.toFixed(2) : 'n/a'}</dd>
      </dl>
      ${m.url ? `<a class="inline-link" href="${m.url}" style="font-size:12px;display:block;margin-top:8px;color:var(--accent)" target="_blank" rel="noopener">Pricing source ↗</a>` : ''}
    </div>
  `).join('');

  const limitsList = limits.map(l => `<li>${l}</li>`).join('');

  const ccusageCommands = (tb.commands || []).map(c =>
    `<div class="method-formula" style="margin:4px 0">${c}</div>`
  ).join('');

  setHTML('method-body', `
    <p style="font-size:14px;color:var(--ink-muted);margin-bottom:12px">
      <strong style="color:var(--ink)">Preferred collector:</strong> ${safe(tb.preferred_collector)}
      · ccusage v${safe(tb.verified_ccusage_version)}
    </p>
    <p style="font-size:13px;color:var(--ink-dim);margin-bottom:6px">Cost estimate formula:</p>
    <div class="method-formula">${formula}</div>
    <div class="pricing-grid">${pricingCards}</div>
    <div style="margin-top:16px">
      <p style="font-size:13px;color:var(--ink-dim);margin-bottom:8px">ccusage commands used:</p>
      ${ccusageCommands}
    </div>
    <div class="method-limitations">
      <p>Limitations & caveats:</p>
      <ul class="limitations-list">${limitsList}</ul>
    </div>
    ${tb.agy_note ? `<p style="margin-top:12px;font-size:13px;color:var(--ink-dim);border-left:2px solid var(--warn);padding-left:10px">${tb.agy_note}</p>` : ''}
  `);
}

/* ── Evidence artifacts ──────────────────────────────────────────────────── */
function renderArtifacts(data) {
  const isScenarioPage = document.body.dataset.page === 'scenario';
  const prefix = isScenarioPage ? '../' : './';
  const scenarios = data.scenarios || [];
  const links = scenarios.flatMap(s => {
    const l = s.links || {};
    return [
      l.results ? { id: s.id, title: `${s.id} Results`,      sub: s.name,                         href: `${prefix}${l.results}` } : null,
      l.json    ? { id: s.id, title: `${s.id} Metrics JSON`, sub: 'machine-readable run facts',    href: `${prefix}${l.json}` }    : null,
      l.metrics ? { id: s.id, title: `${s.id} Metrics MD`,   sub: 'human-readable run summary',   href: `${prefix}${l.metrics}` } : null,
    ].filter(Boolean);
  });

  setHTML('artifactGrid', links.map(l => `
    <a class="artifact-link" href="${l.href}" target="_blank" rel="noopener">
      <span class="artifact-link-id">${l.id}</span>
      <span class="artifact-link-title">${l.title}</span>
      <span class="artifact-link-sub">${l.sub}</span>
    </a>
  `).join(''));
}

/* ── Mobile nav toggle ──────────────────────────────────────────────────── */
function initMobileNav() {
  const toggle = document.querySelector('.nav-toggle');
  const mobileNav = document.getElementById('mobile-nav');
  if (!toggle || !mobileNav) return;

  toggle.addEventListener('click', () => {
    const expanded = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!expanded));
    mobileNav.hidden = expanded;
  });

  mobileNav.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      toggle.setAttribute('aria-expanded', 'false');
      mobileNav.hidden = true;
    });
  });
}

/* ── Resize handler for SVG charts ─────────────────────────────────────── */
function initResizeHandler(data, page) {
  let raf;
  window.addEventListener('resize', () => {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(() => {
      if (page === 'home') drawPareto(data);
      if (page === 'agents') drawLatencyProcessChart(data);
      if (page === 'scenario') {
        const scenarioId = document.body.dataset.scenarioId;
        const s = (data.scenarios || []).find(x => x.slug === scenarioId || x.id.toLowerCase() === scenarioId);
        if (s) {
          const agents = s.agents || [];
          drawD3Scatter('frontierChart', agents.map(a => ({
            id: a.id, short: safe(a.short, a.id), wall: a.wall, tokens: a.tokens
          })), 'wall', 'tokens', {
            xLabel: 'Wall-clock (s)',
            yLabel: 'Total Tokens',
            missingXLabel: 'tokens n/a',
            emptyTitle: 'Token telemetry not attributed yet',
            emptyBody: 'This scenario has verified wall-clock and pass/fail evidence, but no reliable per-agent token totals yet.',
            emptyMeta: 'The fake 0–1 axis has been removed; this panel will render a scatter plot once token data exists.',
          });
        }
      }
    });
  });
}

/* ── Main ────────────────────────────────────────────────────────────────── */
loadData()
  .then(data => {
    const page = document.body.dataset.page;
    
    if (page === 'home') {
      renderKPIs(data);
      renderVerdict(data);
      renderScenarioCards(data);
      drawPareto(data);
      renderMethodBody(data);
      renderArtifacts(data);
    } 
    else if (page === 'agents') {
      renderAgentTable(data);
      drawLatencyProcessChart(data);
    }
    else if (page === 'scenario') {
      const scenarioId = document.body.dataset.scenarioId;
      renderScenarioDetail(data, scenarioId);
    }

    initMobileNav();
    initResizeHandler(data, page);
  })
  .catch(err => {
    console.error('CAB dashboard failed to load:', err);
    ['verdict-score', 'kpi-scenarios', 'kpi-runs', 'kpi-pass', 'kpi-cost'].forEach(id => {
      setText(id, '—');
    });
    setText('verdict-sub', 'Failed to load benchmark data. Check console for details.');
  });
