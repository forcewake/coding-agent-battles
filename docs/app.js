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

const AGENT_DISPLAY = {
  'opencode':   'OpenCode',
  'claude-code':'Claude',
  'mimo':       'MiMo',
  'pi':         'Pi',
  'codex-cli':  'Codex',
  'agy':        'agy',
};
const agentDisplay = (id) => AGENT_DISPLAY[id] || id;

/* ── Data loader ────────────────────────────────────────────────────────── */
async function loadData() {
  const res = await fetch('./site-data.json');
  if (!res.ok) throw new Error(`Failed to load site-data.json: ${res.status}`);
  return res.json();
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

  // compute winners from profiles
  const profiles = data.agentProfiles || [];
  const fastest  = [...profiles].sort((a, b) => (a.avgWall || 9e9) - (b.avgWall || 9e9))[0];
  const cheapest = [...profiles].filter(a => a.avgCost != null).sort((a, b) => a.avgCost - b.avgCost)[0];
  const bestProc = [...profiles].sort((a, b) => (b.avgProcess || 0) - (a.avgProcess || 0))[0];

  const stats = [
    { label: 'Fastest avg',   value: fastest  ? fastest.short  : 'n/a' },
    { label: 'Cheapest avg',  value: cheapest ? cheapest.short : 'n/a' },
    { label: 'Best process',  value: bestProc ? bestProc.short : 'n/a' },
    { label: 'Cost coverage', value: pct(k.costCoverage) },
  ];

  setHTML('verdict-stats', stats.map(s => `
    <div class="verdict-stat">
      <span class="verdict-stat-label">${s.label}</span>
      <span class="verdict-stat-value">${s.value}</span>
    </div>
  `).join(''));
}

/* ── Scenario tabs ─────────────────────────────────────────────────────── */
let currentScenarioIdx = 0;
let scenariosData = [];

function renderScenarioTabs(data) {
  scenariosData = data.scenarios || [];
  const tabBar = document.getElementById('scenario-tabs');
  if (!tabBar) return;

  tabBar.innerHTML = scenariosData.map((s, i) => `
    <button
      class="tab-btn"
      role="tab"
      id="tab-${s.id}"
      aria-selected="${i === 0 ? 'true' : 'false'}"
      aria-controls="scenario-panel"
      data-idx="${i}"
    >
      ${s.id}: ${s.name}
    </button>
  `).join('');

  tabBar.addEventListener('click', (e) => {
    const btn = e.target.closest('.tab-btn');
    if (!btn) return;
    const idx = parseInt(btn.dataset.idx, 10);
    activateScenarioTab(idx);
  });

  activateScenarioTab(0);
}

function activateScenarioTab(idx) {
  currentScenarioIdx = idx;
  // update aria-selected
  document.querySelectorAll('#scenario-tabs .tab-btn').forEach((btn, i) => {
    btn.setAttribute('aria-selected', i === idx ? 'true' : 'false');
  });
  renderScenarioPanel(scenariosData[idx]);
}

function renderScenarioPanel(s) {
  if (!s) return;
  const agents = s.agents || [];

  const winnersHtml = [
    { label: 'Fastest',      value: agentDisplay(s.fastest)     },
    { label: 'Cheapest',     value: agentDisplay(s.cheapest)    },
    { label: 'Best process', value: agentDisplay(s.processBest) },
  ].map(w => `
    <div class="winner-badge">
      <span class="winner-badge-label">${w.label}</span>
      <span class="winner-badge-value">${safe(w.value)}</span>
    </div>
  `).join('');

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
            <span class="spa-metric-label">Process</span>
            <span class="spa-metric-value">${safe(a.process, 'n/a')}</span>
          </div>
          <div class="spa-metric">
            <span class="spa-metric-label">Cost</span>
            <span class="spa-metric-value">${moneyFull(a.cost)}</span>
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
  const linksHtml = [
    links.results ? `<a class="sp-link" href="../${links.results}">Results →</a>` : '',
    links.metrics ? `<a class="sp-link" href="../${links.metrics}">Metrics →</a>` : '',
    links.json    ? `<a class="sp-link" href="../${links.json}">JSON →</a>` : '',
  ].filter(Boolean).join('');

  setHTML('scenario-panel', `
    <div class="sp-header">
      <div class="sp-meta">
        <div class="sp-id">${s.id} · ${safe(s.type)} · ${safe(s.difficulty)}</div>
        <div class="sp-name">${safe(s.name)}</div>
        <div class="sp-summary">${safe(s.summary)}</div>
      </div>
      <div class="sp-winners">${winnersHtml}</div>
    </div>
    <div class="sp-agents">${agentCardsHtml}</div>
    <div class="badge-legend" aria-label="Scenario badge legend">
      <span><b class="pill pill-red">red✓</b> agent captured failing baseline</span>
      <span><b class="pill pill-smoke">smoke✓</b> agent ran user-visible smoke</span>
    </div>
    <div class="sp-links">${linksHtml}</div>
  `);
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

    return `
      <tr>
        <td>
          <div class="at-name">${safe(a.short, a.id)}</div>
          <div class="at-model">${safe(a.label)}</div>
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
          <th>Avg wall</th>
          <th>Avg process</th>
          <th>Avg cost (est.)</th>
          <th>Total tokens</th>
          <th>Telemetry</th>
        </tr>
      </thead>
      <tbody>${rows}</tbody>
    </table>
  `);
}

/* ── Pareto scatter chart ───────────────────────────────────────────────── */
function drawPareto(data) {
  const points = (data.agentProfiles || []).map(a => ({
    id:      a.id,
    short:   a.short || a.id,
    cost:    a.avgCost,
    process: a.avgProcess || 0,
  }));
  drawScatter('paretoChart', points, 'cost', 'process', {
    xLabel: 'avg normalized public cost (USD)',
    yLabel: 'avg process score (0–100)',
    missingXLabel: 'cost n/a',
  });
}

/* ── Latest scenario detail ─────────────────────────────────────────────── */
function renderLatestDetail(data) {
  const latest = data.latestScenario;
  if (!latest) return;

  setText('detail-title',   `${latest.id}: ${safe(latest.name)}`);
  setText('detail-summary', safe(latest.summary));

  const agents = latest.agents || [];

  // Bar charts
  const maxWall  = Math.max(...agents.map(a => a.wall  || 0), 1);
  const maxCost  = Math.max(...agents.filter(a => a.cost != null).map(a => a.cost), 1);

  renderBarList('timeBars',    agents, a => ({ label: safe(a.short, a.id), val: a.wall,    max: maxWall,  suffix: 's',  colorClass: 'bar-fill-time'    }));
  renderBarList('qualityBars', [...agents].sort((a,b) => (b.process||0)-(a.process||0)),
                               a => ({ label: safe(a.short, a.id), val: a.process, max: 100,      suffix: '',   colorClass: 'bar-fill-quality' }));
  renderBarList('costBars',
    agents.filter(a => a.cost != null).sort((a,b) => a.cost - b.cost),
    a => ({ label: safe(a.short, a.id), val: a.cost,    max: maxCost,  suffix: '',   colorClass: 'bar-fill-cost-d', format: moneyFull })
  );

  // Scatter (wall vs tokens)
  const scatterPoints = agents.map(a => ({
    id: a.id, short: safe(a.short, a.id), wall: a.wall, tokens: a.tokens
  }));
  drawScatter('frontierChart', scatterPoints, 'wall', 'tokens', {
    xLabel: 'wall-clock (s)',
    yLabel: 'total tokens',
    missingXLabel: null,
  });

  // Score table
  renderScoreTable(agents, latest.links || {});
}

function renderBarList(containerId, agents, mapper) {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = agents.map(a => {
    const m = mapper(a);
    const pct = (m.val == null || !m.max) ? 0 : Math.max(3, (m.val / m.max) * 100);
    const display = m.format ? m.format(m.val) : (m.val == null ? 'n/a' : `${m.val}${m.suffix}`);
    return `
      <div class="bar-row">
        <span class="bar-row-label">${m.label}</span>
        <div class="bar-track">
          <div class="bar-fill ${m.colorClass}" style="width:${pct.toFixed(1)}%"></div>
        </div>
        <span class="bar-row-value">${display}</span>
      </div>
    `;
  }).join('');
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

/* ── Generic SVG scatter ─────────────────────────────────────────────────── */
const AGENT_COLORS = {
  'pi':         '#34d17a',
  'opencode':   '#4f8ef7',
  'claude-code':'#a78bfa',
  'mimo':       '#f5a623',
  'codex-cli':  '#f87171',
  'agy':        '#22d3ee',
};
const agentColor = (id) => AGENT_COLORS[id] || '#8a9ab8';

function drawScatter(svgId, points, xKey, yKey, opts = {}) {
  const svg = document.getElementById(svgId);
  if (!svg) return;
  const W = svg.clientWidth || 680;
  const H = parseInt(svg.getAttribute('height') || svg.style.height) || (svgId === 'frontierChart' ? 260 : 340);
  const pad = { top: 30, right: 30, bottom: 48, left: 64 };
  const innerW = W - pad.left - pad.right;
  const innerH = H - pad.top  - pad.bottom;

  svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  svg.style.height = `${H}px`;

  const known = points.filter(p => p[xKey] != null && p[yKey] != null);
  const maxX  = known.length ? Math.max(...known.map(p => p[xKey])) * 1.18 : 1;
  const maxY  = known.length ? Math.max(...known.map(p => p[yKey])) * 1.15 : 1;
  const minY  = known.length ? Math.min(...known.map(p => p[yKey])) * 0.9 : 0;

  const px = (v) => pad.left + (v / maxX) * innerW;
  const py = (v) => pad.top  + innerH - ((v - minY) / (maxY - minY || 1)) * innerH;

  /* axes */
  const axisColor = '#2a3a58';
  const textColor = '#5a6a88';
  const fontSize  = 11;

  let svgContent = `
    <line x1="${pad.left}" x2="${pad.left + innerW}" y1="${pad.top + innerH}" y2="${pad.top + innerH}" stroke="${axisColor}" stroke-width="1"/>
    <line x1="${pad.left}" x2="${pad.left}"           y1="${pad.top}"         y2="${pad.top + innerH}" stroke="${axisColor}" stroke-width="1"/>
    <text x="${pad.left + innerW / 2}" y="${H - 8}" fill="${textColor}" font-size="${fontSize}" text-anchor="middle" font-family="system-ui,sans-serif">${opts.xLabel || xKey}</text>
    <text transform="translate(${fontSize + 2} ${pad.top + innerH / 2}) rotate(-90)" fill="${textColor}" font-size="${fontSize}" text-anchor="middle" font-family="system-ui,sans-serif">${opts.yLabel || yKey}</text>
  `;

  /* x-axis ticks */
  const nTicks = 4;
  for (let i = 0; i <= nTicks; i++) {
    const val = (maxX / nTicks) * i;
    const tx  = px(val);
    const label = val < 0.01 ? val.toFixed(4) : val < 1 ? val.toFixed(2) : val.toFixed(1);
    svgContent += `
      <line x1="${tx}" x2="${tx}" y1="${pad.top + innerH}" y2="${pad.top + innerH + 4}" stroke="${axisColor}" stroke-width="1"/>
      <text x="${tx}" y="${pad.top + innerH + 14}" fill="${textColor}" font-size="${fontSize - 1}" text-anchor="middle" font-family="system-ui,sans-serif">${label}</text>
    `;
  }

  /* points */
  points.forEach(p => {
    const missing = p[xKey] == null || p[yKey] == null;
    const cx = missing ? pad.left + innerW + 16 : px(p[xKey]);
    const cy = missing ? pad.top + innerH - 20 : py(p[yKey]);
    const r  = missing ? 7 : 10;
    const color = agentColor(p.id);
    const opacity = missing ? 0.45 : 1;
    const labelText = missing && opts.missingXLabel
      ? `${p.short} (${opts.missingXLabel})`
      : p.short;

    svgContent += `
      <circle cx="${cx}" cy="${cy}" r="${r}" fill="${color}" opacity="${opacity}" stroke="rgba(255,255,255,.25)" stroke-width="1.5"/>
      <text x="${cx + r + 5}" y="${cy + 4}" fill="#e8edf8" font-size="12" font-weight="700" font-family="system-ui,sans-serif">${labelText}</text>
    `;
  });

  svg.innerHTML = svgContent;
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
  const scenarios = data.scenarios || [];
  const links = scenarios.flatMap(s => {
    const l = s.links || {};
    return [
      l.results ? { id: s.id, title: `${s.id} Results`,      sub: s.name,                         href: `../${l.results}` } : null,
      l.json    ? { id: s.id, title: `${s.id} Metrics JSON`, sub: 'machine-readable run facts',    href: `../${l.json}` }    : null,
      l.metrics ? { id: s.id, title: `${s.id} Metrics MD`,   sub: 'human-readable run summary',   href: `../${l.metrics}` } : null,
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

  // close on link click
  mobileNav.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      toggle.setAttribute('aria-expanded', 'false');
      mobileNav.hidden = true;
    });
  });
}

/* ── Resize handler for SVG charts ─────────────────────────────────────── */
function initResizeHandler(data) {
  let raf;
  window.addEventListener('resize', () => {
    cancelAnimationFrame(raf);
    raf = requestAnimationFrame(() => {
      drawPareto(data);
      const latest = data.latestScenario;
      if (latest) {
        const agents = latest.agents || [];
        drawScatter('frontierChart', agents.map(a => ({
          id: a.id, short: safe(a.short, a.id), wall: a.wall, tokens: a.tokens
        })), 'wall', 'tokens', {
          xLabel: 'wall-clock (s)',
          yLabel: 'total tokens',
        });
      }
    });
  });
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

/* ── Main ────────────────────────────────────────────────────────────────── */
loadData()
  .then(data => {
    renderKPIs(data);
    renderVerdict(data);
    renderScenarioTabs(data);
    renderAgentTable(data);
    renderLatestDetail(data);
    renderMethodBody(data);
    renderArtifacts(data);
    drawPareto(data);
    initMobileNav();
    initResizeHandler(data);
  })
  .catch(err => {
    console.error('CAB dashboard failed to load:', err);
    // Show graceful error in main areas
    ['verdict-score', 'kpi-scenarios', 'kpi-runs', 'kpi-pass', 'kpi-cost'].forEach(id => {
      setText(id, '—');
    });
    setText('verdict-sub', 'Failed to load benchmark data. Check console for details.');
  });
