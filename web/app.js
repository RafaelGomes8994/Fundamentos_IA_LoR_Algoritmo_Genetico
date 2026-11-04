const state = {
  champions: {},
  bosses: {},
  relics: {},
  stars: 3,
};

const els = {
  dbStatsPill: document.getElementById("dbStatsPill"),
  form: document.getElementById("optimizeForm"),
  championSelect: document.getElementById("championSelect"),
  championPreview: document.getElementById("championPreview"),
  starSelector: document.getElementById("starSelector"),
  starValueLabel: document.getElementById("starValueLabel"),
  starsInput: document.getElementById("starsInput"),
  bossSelect: document.getElementById("bossSelect"),
  bossPreview: document.getElementById("bossPreview"),
  banRelicSelect: document.getElementById("banRelicSelect"),
  topKInput: document.getElementById("topKInput"),
  popSizeInput: document.getElementById("popSizeInput"),
  generationsInput: document.getElementById("generationsInput"),
  runBtn: document.getElementById("runBtn"),
  runBtnText: document.getElementById("runBtnText"),
  metricScenario: document.getElementById("metricScenario"),
  metricBestFitness: document.getElementById("metricBestFitness"),
  metricTime: document.getElementById("metricTime"),
  metricConfig: document.getElementById("metricConfig"),
  buildsContainer: document.getElementById("buildsContainer"),
  cliOutputPre: document.getElementById("cliOutputPre"),
  terminalCmdPreview: document.getElementById("terminalCmdPreview"),
  copyCliBtn: document.getElementById("copyCliBtn"),
};

function escapeHtml(str) {
  return String(str ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function updateChampionPreview() {
  const name = els.championSelect.value;
  const champ = state.champions[name];
  if (!champ) return;

  els.championPreview.innerHTML = `
    <div><strong>${escapeHtml(champ.name)}</strong> • ${escapeHtml(champ.core_mechanic)}</div>
    <div class="context-tags">
      <span class="mini-badge tier">Tier ${escapeHtml(champ.tier)}</span>
      <span class="mini-badge">Arquétipo: ${escapeHtml(champ.archetype)}</span>
      <span class="mini-badge">Dificuldade: ${escapeHtml(champ.difficulty)}</span>
    </div>
  `;
}

function updateBossPreview() {
  const name = els.bossSelect.value;
  if (!name || !state.bosses[name]) {
    els.bossPreview.classList.add("hidden");
    els.bossPreview.innerHTML = "";
    return;
  }

  const boss = state.bosses[name];
  const counters = (boss.counter_tags || [])
    .map((t) => `<span class="mini-badge counter">+${escapeHtml(t)}</span>`)
    .join("");
  const penalties = (boss.penalized_tags || [])
    .map((t) => `<span class="mini-badge penalty">-${escapeHtml(t)}</span>`)
    .join("");

  els.bossPreview.classList.remove("hidden");
  els.bossPreview.innerHTML = `
    <div><strong>${escapeHtml(boss.name)} (${boss.stars}★)</strong> — ${escapeHtml(boss.threat_description)}</div>
    <div class="context-tags">${counters}${penalties}</div>
  `;
}

function setStars(val) {
  state.stars = val;
  els.starsInput.value = String(val);
  els.starValueLabel.textContent = `${val}★ ${val === 1 ? "Estrela" : "Estrelas"}`;

  const btns = els.starSelector.querySelectorAll(".star-btn");
  btns.forEach((btn) => {
    const s = Number(btn.dataset.star);
    btn.classList.toggle("active", s <= val);
  });
}

function buildCliCommand(payload) {
  let cmd = `python examples/demo_cli.py --champion "${payload.champion}" --stars ${payload.stars}`;
  if (payload.boss) cmd += ` --boss "${payload.boss}"`;
  if (payload.ban_relic) cmd += ` --ban-relic "${payload.ban_relic}"`;
  if (payload.top_k !== 3) cmd += ` --top_k ${payload.top_k}`;
  if (payload.pop_size !== 30) cmd += ` --pop-size ${payload.pop_size}`;
  if (payload.generations !== 100) cmd += ` --generations ${payload.generations}`;
  return cmd;
}

function formatSigned(val) {
  const n = Number(val || 0);
  if (n > 0) return `+${n.toFixed(2)}`;
  if (n < 0) return `${n.toFixed(2)}`;
  return "0.00";
}

function getValClass(val) {
  const n = Number(val || 0);
  if (n > 0) return "bd-val";
  if (n < 0) return "bd-val negative";
  return "bd-val zero";
}

function renderBuilds(data) {
  const relicsCatalog = data.relic_details || state.relics;
  const builds = data.top_k_builds || [];

  if (!builds.length) {
    els.buildsContainer.innerHTML = `<div class="panel">Nenhuma build encontrada.</div>`;
    return;
  }

  els.buildsContainer.innerHTML = builds
    .map((build, idx) => {
      const rank = idx + 1;
      const bd = build.breakdown || {};

      const slotsHtml = build.relics
        .map((rName, sIdx) => {
          const rInfo = relicsCatalog[rName] || state.relics[rName] || {
            name: rName,
            rarity: "Rare",
            description: "",
            base_score: 0,
          };
          const rarity = rInfo.rarity || "Rare";
          return `
            <div class="relic-slot rarity-${escapeHtml(rarity)}">
              <div class="slot-top">
                <span>Slot ${sIdx + 1}</span>
                <span class="rarity-pill ${escapeHtml(rarity)}">${escapeHtml(rarity)}</span>
              </div>
              <div class="relic-name">${escapeHtml(rName)}</div>
              <div class="relic-desc">${escapeHtml(rInfo.description || "Relíquia do Caminho dos Campeões.")}</div>
            </div>
          `;
        })
        .join("");

      return `
        <article class="build-card ${rank === 1 ? "rank-1" : ""}">
          <div class="build-header">
            <div class="rank-title">
              <span class="rank-badge">RANK #${rank}</span>
              <strong>${rank === 1 ? "Build Ótima Recomendada pela IA" : `Alternativa Viável #${rank}`}</strong>
            </div>
            <div class="fitness-score">Fitness Total: ${Number(build.fitness).toFixed(4)}</div>
          </div>

          <div class="relics-grid">
            ${slotsHtml}
          </div>

          <div class="breakdown-box">
            <div class="breakdown-title">Decomposição Matemática da Função de Fitness</div>
            <div class="breakdown-items">
              <div class="bd-item">
                <span class="bd-label">Poder Base Relíquias</span>
                <span class="${getValClass(bd.base_score)}">${formatSigned(bd.base_score)}</span>
              </div>
              <div class="bd-item">
                <span class="bd-label">Sinergia Campeão</span>
                <span class="${getValClass(bd.champion_synergy)}">${formatSigned(bd.champion_synergy)}</span>
              </div>
              <div class="bd-item">
                <span class="bd-label">Sinergia Poder Estelar</span>
                <span class="${getValClass(bd.star_power_synergy)}">${formatSigned(bd.star_power_synergy)}</span>
              </div>
              <div class="bd-item">
                <span class="bd-label">Bônus Combos</span>
                <span class="${getValClass(bd.combo_bonus)}">${formatSigned(bd.combo_bonus)}</span>
              </div>
              <div class="bd-item">
                <span class="bd-label">Adaptação ao Chefe</span>
                <span class="${getValClass(bd.boss_adaptation)}">${formatSigned(bd.boss_adaptation)}</span>
              </div>
            </div>
          </div>
        </article>
      `;
    })
    .join("");
}

async function runOptimization(e) {
  if (e) e.preventDefault();

  const payload = {
    champion: els.championSelect.value,
    stars: state.stars,
    boss: els.bossSelect.value || null,
    ban_relic: els.banRelicSelect.value || null,
    top_k: Number(els.topKInput.value) || 3,
    pop_size: Number(els.popSizeInput.value) || 30,
    generations: Number(els.generationsInput.value) || 100,
  };

  els.runBtn.disabled = true;
  els.runBtnText.textContent = "Evoluindo População...";
  els.terminalCmdPreview.textContent = buildCliCommand(payload);

  try {
    const resp = await fetch("/api/optimize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await resp.json();
    if (!resp.ok) {
      throw new Error(data.error || "Erro ao otimizar builds.");
    }

    // Update metrics bar
    const strategies = [];
    if (payload.boss) strategies.push(`E3 (${payload.boss})`);
    if (payload.ban_relic) strategies.push("E2 (Restrição)");
    if (!strategies.length) strategies.push("E1 • Geral");

    els.metricScenario.textContent = strategies.join(" + ");
    els.metricBestFitness.textContent = data.best_build
      ? Number(data.best_build.fitness).toFixed(4)
      : "—";
    els.metricTime.textContent = `${Number(data.execution_time_ms).toFixed(2)} ms`;
    els.metricConfig.textContent = `${data.population_size} ind × ${data.generations_run} ger`;

    renderBuilds(data);
    els.cliOutputPre.textContent = data.cli_output || "";
  } catch (err) {
    els.buildsContainer.innerHTML = `<div class="panel" style="color:#f87171;">Erro: ${escapeHtml(err.message)}</div>`;
  } finally {
    els.runBtn.disabled = false;
    els.runBtnText.textContent = "Gerar Builds Recomendadas";
  }
}

async function init() {
  // Setup star selector events
  els.starSelector.querySelectorAll(".star-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      setStars(Number(btn.dataset.star));
    });
  });

  // Setup tabs
  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
      document.querySelectorAll(".tab-content").forEach((c) => c.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById(btn.dataset.tab).classList.add("active");
    });
  });

  // Copy CLI output button
  els.copyCliBtn.addEventListener("click", async () => {
    await navigator.clipboard.writeText(els.cliOutputPre.textContent);
    const oldText = els.copyCliBtn.textContent;
    els.copyCliBtn.textContent = "Copiado!";
    setTimeout(() => {
      els.copyCliBtn.textContent = oldText;
    }, 1500);
  });

  // Load metadata
  const res = await fetch("/api/metadata");
  const meta = await res.json();

  // Populate champions
  els.championSelect.innerHTML = meta.champions
    .map((c) => {
      state.champions[c.name] = c;
      const selected = c.name === "Jinx" ? "selected" : "";
      return `<option value="${escapeHtml(c.name)}" ${selected}>${escapeHtml(c.name)} (Tier ${escapeHtml(c.tier)} • ${escapeHtml(c.archetype)})</option>`;
    })
    .join("");

  // Populate bosses
  meta.bosses.forEach((b) => {
    state.bosses[b.name] = b;
    const opt = document.createElement("option");
    opt.value = b.name;
    opt.textContent = `${b.name} (${b.stars}★ — ${b.map_type})`;
    els.bossSelect.appendChild(opt);
  });

  // Populate relics for ban (E2)
  meta.relics.forEach((r) => {
    state.relics[r.name] = r;
    const opt = document.createElement("option");
    opt.value = r.name;
    opt.textContent = `${r.name} [${r.rarity}]`;
    els.banRelicSelect.appendChild(opt);
  });

  els.dbStatsPill.textContent = `${meta.champions.length} Campeões • ${meta.relics.length} Relíquias • ${meta.bosses.length} Chefes`;

  els.championSelect.addEventListener("change", updateChampionPreview);
  els.bossSelect.addEventListener("change", updateBossPreview);
  els.form.addEventListener("submit", runOptimization);

  updateChampionPreview();
  updateBossPreview();

  // Run initial optimization automatically
  await runOptimization();
}

init();

