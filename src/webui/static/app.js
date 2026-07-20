const friendlyFleet = document.querySelector('#friendly-fleet');
const enemyFleet = document.querySelector('#enemy-list');
const addFriendly = document.querySelector('#add-friendly');
const addEnemy = document.querySelector('#add-enemy');
const resultLogs = [...document.querySelectorAll('.shared-result-log')];
const editor = document.querySelector('#ship-editor');
const editorName = document.querySelector('#editor-name');
const editorLevel = document.querySelector('#editor-level');
const editorLevelField = document.querySelector('#editor-level-field');
const editorAffection = document.querySelector('#editor-affection');
const editorSkill = document.querySelector('#editor-skill');
const friendEditorFields = document.querySelector('#friend-editor-fields');
const equipmentEditors = [1, 2, 3, 4].map(index => document.querySelector(`#editor-equipment-${index}`));
const editorShipPicker = setupSearchablePicker(document.querySelector('#editor-ship-picker'), editorName);
const equipmentPickers = [1, 2, 3, 4].map(index => setupSearchablePicker(
  document.querySelector(`#editor-equipment-picker-${index}`),
  document.querySelector(`#editor-equipment-${index}`),
));
const strategyEditors = {
  attack: document.querySelector('#editor-attack-strategy'),
  defense: document.querySelector('#editor-defense-strategy'),
  special: document.querySelector('#editor-special-strategy'),
};
const strategyLevelEditors = {
  attack: document.querySelector('#editor-attack-strategy-level'),
  defense: document.querySelector('#editor-defense-strategy-level'),
  special: document.querySelector('#editor-special-strategy-level'),
};
const editorSelectPickers = [editorSkill, ...Object.values(strategyEditors)].map(setupEditorSelectPicker);
const battleTypePicker = document.querySelector('#battle-type-picker');
const battleTypeValue = document.querySelector('#battle-type-value');
const epochRange = document.querySelector('#epoch-range');
const epochValue = document.querySelector('#epoch-value');
const roundsRange = document.querySelector('#rounds-range');
const roundsValue = document.querySelector('#rounds-value');
const simulationButton = document.querySelector('#simulation-button');
const simulationCountStat = document.querySelector('#epoch-stat');
const configFileInput = document.querySelector('#config-file');
const notice = document.querySelector('#notice');
const clearWorkspaceButton = document.querySelector('#clear-workspace');
const clearConfirmDialog = document.querySelector('#clear-confirm');

document.addEventListener('pointerdown', event => {
  if (!(event.target instanceof Node)) return;
  [editorShipPicker, ...equipmentPickers].forEach(picker => {
    if (!picker.container.contains(event.target)) picker.close();
  });
  editorSelectPickers.forEach(picker => {
    if (!picker.container.contains(event.target)) picker.close();
  });
  if (!battleTypePicker.contains(event.target)) battleTypePicker.open = false;
});

let metadata = null;
let friendShipMap = new Map();
let enemyShipMap = new Map();
let equipmentMap = new Map();
let strategyMap = new Map();
let editorShipLabels = new Map();
let editorEquipmentLabels = new Map();
let draggedCard = null;
let currentEditing = null;
let loadTarget = null;
let simulationState = 'idle';
let pollTimer = null;
let statusAbortController = null;
let latestSimulation = null;
let simulationDisplayFrozen = false;
let latestSummary = null;
let damagePhaseFilter = null;

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>'"]/g, character => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;',
  })[character]);
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.error || `请求失败（${response.status}）`);
  return payload;
}

function showNotice(message, error = false) {
  notice.textContent = message;
  notice.classList.toggle('error', error);
  notice.hidden = false;
  clearTimeout(showNotice.timer);
  showNotice.timer = setTimeout(() => { notice.hidden = true; }, 3200);
}

function setResultLog(content) {
  resultLogs.forEach(output => { output.textContent = content; });
}

function resetResultDisplay() {
  latestSummary = null;
  damagePhaseFilter = null;
  document.querySelector('#win-rate-stat').innerHTML = '—<em>%</em>';
  document.querySelector('#flagship-stat').innerHTML = '—<em>%</em>';
  document.querySelector('#average-damage-stat').textContent = '—';
  document.querySelector('#average-loss-stat').textContent = '—';
  document.querySelector('#resource-stat').textContent = '—';
  updateSimulationCountStat(0);
  document.querySelector('#win-chart-value').innerHTML = '—<small>%</small>';
  document.querySelector('#recon-rate-value').innerHTML = '—<small>%</small>';
  document.querySelector('#friend-recon-value').textContent = '—';
  document.querySelector('#recon-request-value').textContent = '—';
  document.querySelector('#air-con-value').textContent = '—';
  document.querySelector('#friend-aerial-value').textContent = '—';
  document.querySelector('#enemy-aerial-value').textContent = '—';
  document.querySelector('#damage-chart-value').textContent = '—';
  document.querySelector('#damage-floor-value').textContent = '—';
  document.querySelector('#ship-damage-chart-value').textContent = '—';
  document.querySelector('#ship-damage-chart-label').textContent = '舰船伤害';
  ['#win-chart', '#damage-chart', '#ship-damage-chart'].forEach(selector => setDonut(document.querySelector(selector), [], []));
  const winChart = document.querySelector('#win-chart');
  const winLegend = document.querySelector('#win-legend');
  const flags = ['SS 完胜', 'S 胜利', 'A 小胜', 'B 战术胜利', 'C 战术失败', 'D 失败'];
  renderLegend(winLegend, flags.map((name, index) => ({ name, value: 0, index })), 0, ['var(--ss)', 'var(--s)', 'var(--a)', 'var(--b)', 'var(--c)', 'var(--d)'], 6, { chart: winChart, percentOnly: true });
  bindChartInteractions(winChart, winLegend);
  document.querySelector('#phase-legend').replaceChildren();
  const shipLegend = document.querySelector('#ship-damage-legend');
  shipLegend.replaceChildren();
  shipLegend.hidden = true;
  ['#oil-value', '#ammo-value', '#steel-value', '#aluminum-value'].forEach(selector => { document.querySelector(selector).textContent = '—'; });
  ['#friend-mid-rates', '#friend-heavy-rates', '#enemy-sink-rates', '#enemy-health-rates'].forEach(selector => document.querySelector(selector).replaceChildren());
  document.querySelector('#battle-detail').textContent = '模拟完成后将在这里显示一场战斗的详细记录。';
  setResultLog('等待开始模拟');
  document.querySelectorAll('.result-tabs button').forEach(tab => {
    const active = tab.dataset.view === 'win';
    tab.classList.toggle('active', active);
    tab.setAttribute('aria-selected', String(active));
  });
  document.querySelectorAll('.result-view-panel').forEach(panel => {
    const active = panel.dataset.panel === 'win';
    panel.hidden = !active;
    panel.classList.toggle('active', active);
  });
}

async function clearWorkspace() {
  simulationDisplayFrozen = true;
  clearTimeout(pollTimer);
  statusAbortController?.abort();
  if (simulationState === 'running' || simulationState === 'stopping') {
    try {
      await api('/api/simulation/stop', { method: 'POST', body: '{}' });
    } catch {
      // Clearing the page must not be blocked by an already-ending simulation.
    }
  }
  try {
    await api('/api/simulation/reset', { method: 'POST', body: '{}' });
  } catch {
    // The local view is still reset if the service is temporarily unavailable.
  }
  friendlyFleet.replaceChildren();
  enemyFleet.replaceChildren();
  updateAllSlots();
  setFormation('friend', 4);
  setFormation('enemy', 4);
  setBattleType('NormalBattle');
  updateEpoch(5000);
  roundsRange.value = '1';
  roundsValue.value = '1';
  battleTypePicker.open = false;
  [editorShipPicker, ...equipmentPickers].forEach(picker => picker.close());
  editorSelectPickers.forEach(picker => picker.close());
  latestSimulation = null;
  simulationState = 'idle';
  simulationButton.classList.remove('running', 'stopping');
  simulationButton.style.removeProperty('--run-progress');
  setSimulationButtonContent('play', '开始模拟');
  resetResultDisplay();
}

function normaliseCid(value) {
  return String(value ?? '').padStart(5, '0');
}

function cloneConfig(value) {
  return JSON.parse(JSON.stringify(value));
}

function formatNumber(value, digits = 0) {
  const number = Number(value);
  if (!Number.isFinite(number)) return '—';
  return number.toLocaleString('zh-CN', { minimumFractionDigits: digits, maximumFractionDigits: digits });
}

function fillSelect(select, options, selectedValue = '', emptyLabel = null) {
  const items = [];
  if (emptyLabel !== null) items.push({ value: '', label: emptyLabel });
  options.forEach(option => items.push(option));
  select.replaceChildren(...items.map(item => {
    const element = document.createElement('option');
    element.value = String(item.value);
    element.textContent = item.label;
    return element;
  }));
  select.value = String(selectedValue ?? '');
  if (select.selectedIndex < 0) select.selectedIndex = 0;
  select._editorSelectPicker?.sync();
}

function shipEditorLabel(ship, isFriend) {
  return isFriend ? ship.name : `${ship.name} · cid ${ship.cid}`;
}

function setupSearchablePicker(container, input) {
  const picker = {
    container,
    input,
    menu: container.querySelector('.picker-menu'),
    toggle: container.querySelector('.picker-toggle'),
    choices: [],
  };
  const open = () => {
    renderPickerChoices(picker);
    container.classList.add('open');
    input.setAttribute('aria-expanded', 'true');
  };
  const close = () => {
    container.classList.remove('open');
    input.setAttribute('aria-expanded', 'false');
  };
  picker.open = open;
  picker.close = close;
  picker.setDisabled = disabled => {
    input.disabled = disabled;
    picker.toggle.disabled = disabled;
    container.classList.toggle('disabled', disabled);
    if (disabled) close();
  };
  input.addEventListener('focus', open);
  input.addEventListener('input', open);
  input.addEventListener('keyup', open);
  input.addEventListener('change', open);
  input.addEventListener('keydown', event => {
    if (event.key !== 'Enter') return;
    // Searching an equipment/ship list must not bubble into the editor's
    // Enter-to-save shortcut.
    event.preventDefault();
    event.stopPropagation();
    open();
  });
  picker.toggle.addEventListener('mousedown', event => event.preventDefault());
  picker.toggle.addEventListener('click', () => {
    if (container.classList.contains('open')) close();
    else {
      input.focus();
      open();
    }
  });
  picker.menu.addEventListener('mousedown', event => event.preventDefault());
  picker.menu.addEventListener('click', event => {
    const option = event.target.closest('button[data-value]');
    if (!option) return;
    input.value = option.dataset.value;
    input.dispatchEvent(new Event('input', { bubbles: true }));
    close();
  });
  return picker;
}

function setupEditorSelectPicker(select) {
  const container = document.createElement('span');
  container.className = 'editor-select-picker';
  const toggle = document.createElement('button');
  toggle.type = 'button';
  toggle.className = 'editor-select-toggle';
  const value = document.createElement('span');
  const menu = document.createElement('span');
  menu.className = 'picker-menu';
  menu.setAttribute('role', 'listbox');
  toggle.append(value);
  select.before(container);
  container.append(select, toggle, menu);

  const close = () => container.classList.remove('open');
  const render = () => {
    value.textContent = select.selectedOptions[0]?.textContent || '';
    menu.replaceChildren(...[...select.options].map(option => {
      const item = document.createElement('button');
      item.type = 'button';
      item.dataset.value = option.value;
      item.textContent = option.textContent;
      item.classList.toggle('selected', option.selected);
      item.setAttribute('role', 'option');
      item.setAttribute('aria-selected', String(option.selected));
      return item;
    }));
  };
  const sync = () => render();
  select._editorSelectPicker = { container, sync, close };
  toggle.addEventListener('click', () => {
    render();
    container.classList.toggle('open');
  });
  menu.addEventListener('mousedown', event => event.preventDefault());
  menu.addEventListener('click', event => {
    const option = event.target.closest('button[data-value]');
    if (!option) return;
    select.value = option.dataset.value;
    select.dispatchEvent(new Event('change', { bubbles: true }));
    close();
  });
  select.addEventListener('change', sync);
  sync();
  return select._editorSelectPicker;
}

function renderPickerChoices(picker) {
  const query = picker.input.value.trim().toLocaleLowerCase('zh-CN');
  const matched = query
    ? picker.choices.filter(value => value.toLocaleLowerCase('zh-CN').includes(query))
    : picker.choices;
  const choices = matched.length ? matched : picker.choices;
  picker.menu.replaceChildren(...choices.map(value => {
    const option = document.createElement('button');
    option.type = 'button';
    option.dataset.value = value;
    option.textContent = value;
    option.classList.toggle('selected', value === picker.input.value);
    option.setAttribute('aria-selected', String(value === picker.input.value));
    return option;
  }));
}

function setPickerChoices(picker, choices) {
  picker.choices = choices;
  renderPickerChoices(picker);
}

function setEditorShipOptions(catalog, isFriend, selectedCid) {
  editorShipLabels = new Map(catalog.map(ship => [shipEditorLabel(ship, isFriend), ship.cid]));
  setPickerChoices(editorShipPicker, [...editorShipLabels.keys()]);
  const selected = catalog.find(ship => ship.cid === String(selectedCid));
  editorName.value = selected ? shipEditorLabel(selected, isFriend) : '';
  renderPickerChoices(editorShipPicker);
}

function selectedEditorShip(side) {
  const catalog = side === 'friend' ? metadata.friend_ships : metadata.enemy_ships;
  const isFriend = side === 'friend';
  const value = editorName.value.trim();
  const cid = editorShipLabels.get(value);
  if (cid) return (isFriend ? friendShipMap : enemyShipMap).get(cid) || catalog[0];
  return catalog.find(ship => ship.name === value || shipEditorLabel(ship, isFriend) === value)
    || (currentEditing ? (isFriend ? friendShipMap : enemyShipMap).get(currentEditing._shipConfig.cid) : null)
    || catalog[0];
}

function setEquipmentOptions() {
  editorEquipmentLabels = new Map(metadata.equipment.map(item => [item.name, item.eid]));
  equipmentPickers.forEach(picker => setPickerChoices(picker, [...editorEquipmentLabels.keys()]));
}

function selectedEquipmentId(value) {
  return editorEquipmentLabels.get(value.trim()) || null;
}

function clampEditorInput(input, minimum, maximum, fallback) {
  const value = Number(input.value);
  const clamped = Math.max(minimum, Math.min(maximum, Number.isFinite(value) ? value : fallback));
  input.value = String(clamped);
  return clamped;
}

function updateSlots(list, addButton) {
  const cards = [...list.querySelectorAll('.ship-card')];
  cards.forEach((card, index) => {
    const slot = card.querySelector('.slot');
    slot.textContent = index + 1;
    slot.dataset.number = String(index + 1);
    slot.classList.toggle('flag', index === 0);
    slot.setAttribute('aria-label', `删除第 ${index + 1} 艘舰船`);
    card._shipConfig.loc = index + 1;
  });
  const panel = list.closest('.fleet-panel');
  if (panel) {
    const panelRect = panel.getBoundingClientRect();
    const listRect = list.getBoundingClientRect();
    const slotHeight = listRect.height / 6;
    addButton.style.top = `${listRect.top - panelRect.top + cards.length * slotHeight}px`;
  }
  addButton.hidden = cards.length >= 6;
}

function updateAllSlots() {
  updateSlots(friendlyFleet, addFriendly);
  updateSlots(enemyFleet, addEnemy);
}

window.addEventListener('resize', updateAllSlots);

function strategyDetails(shipConfig) {
  const selected = { attack: null, defense: null, special: null };
  (shipConfig.strategy || []).forEach(item => {
    const detail = strategyMap.get(String(item.stid));
    if (detail) selected[detail.category] = { ...detail, level: Number(item.level) || 3 };
  });
  return selected;
}

function createShipCard(side, sourceConfig = null) {
  const isFriend = side === 'friend';
  const catalog = isFriend ? metadata.friend_ships : metadata.enemy_ships;
  const fallback = catalog[0];
  const config = sourceConfig ? cloneConfig(sourceConfig) : {
    loc: 1,
    cid: null,
    level: isFriend ? 110 : 1,
    affection: isFriend ? 200 : 50,
    skill: 0,
    pending: true,
    ...(isFriend ? { equipment: [], strategy: [] } : {}),
  };
  const pending = Boolean(config.pending) || !config.cid;
  config.pending = pending;
  const ship = pending ? null : (isFriend ? friendShipMap : enemyShipMap).get(normaliseCid(config.cid)) || fallback;
  if (ship) config.cid = ship.cid;
  config.level = isFriend
    ? Math.max(1, Math.min(110, Number(config.level) || 110))
    : Math.max(1, Number(ship?.level) || 1);
  if (isFriend) {
    config.affection = Math.max(0, Math.min(200, Number(config.affection) || 0));
    config.skill = Number(config.skill) || 0;
    config.equipment = (config.equipment || []).map(item => ({ loc: Number(item.loc), eid: normaliseCid(item.eid) }));
    config.strategy = (config.strategy || []).map(item => ({
      stid: String(item.stid),
      level: Math.max(0, Math.min(3, Number.isFinite(Number(item.level)) ? Number(item.level) : 3)),
    }));
  }

  const card = document.createElement('li');
  card.className = `ship-card${isFriend ? '' : ' enemy-ship'}`;
  card.draggable = true;
  card.dataset.side = side;
  card.dataset.cid = ship?.cid || '';
  card._shipConfig = config;

  if (pending) {
    const description = isFriend ? '点击编辑选择舰船、技能与装备' : '点击编辑选择敌方舰船';
    card.innerHTML = `<button type="button" class="slot"></button><div class="ship-name"><strong>待选择舰船</strong></div><div class="ship-details"><div class="ship-meta">${description}</div></div><div class="ship-actions"><button class="edit-ship" aria-label="编辑待选择舰船">⋮</button><button class="drag-handle" aria-label="拖动待选择舰船">☰</button></div>`;
  } else if (isFriend) {
    const skill = ship.skills.find(item => Number(item.id) === config.skill);
    const selectedStrategies = strategyDetails(config);
    const tacticLabels = ['attack', 'defense', 'special'].map(category => {
      const selected = selectedStrategies[category];
      const label = metadata.strategies[category].label;
      return selected ? `${selected.name} Lv.${selected.level}` : `无${label}战术`;
    });
    const equipped = new Map(config.equipment.map(item => [Number(item.loc), equipmentMap.get(item.eid)?.name || item.eid]));
    const equipmentLabels = [1, 2, 3, 4].map(index => equipped.get(index) || '——');
    card.innerHTML = `<button type="button" class="slot"></button><div class="ship-name"><strong>${escapeHtml(ship.name)}</strong></div><div class="ship-details"><div class="ship-meta">${escapeHtml(ship.type)} · ${escapeHtml(ship.country)} · Lv.${config.level} · 好感 ${config.affection}</div><div class="tactics-list"><span>${escapeHtml(skill?.name || '无技能')}</span>${tacticLabels.map(label => `<span>${escapeHtml(label)}</span>`).join('')}</div><div class="equipment-list">${equipmentLabels.map(label => `<span>${escapeHtml(label)}</span>`).join('')}</div></div><div class="ship-actions"><button class="edit-ship" aria-label="编辑${escapeHtml(ship.name)}">⋮</button><button class="drag-handle" aria-label="拖动${escapeHtml(ship.name)}">☰</button></div>`;
  } else {
    card.innerHTML = `<button type="button" class="slot"></button><div class="ship-name"><strong>${escapeHtml(ship.name)}</strong></div><div class="ship-details"><div class="ship-meta">${escapeHtml(ship.type)}·Lv.${config.level}·cid ${escapeHtml(ship.cid)}</div><div class="enemy-status">耐久 ${ship.health} · 装甲 ${ship.armor} · 对空 ${ship.antiair}</div></div><div class="ship-actions"><button class="edit-ship" aria-label="编辑${escapeHtml(ship.name)}">⋮</button><button class="drag-handle" aria-label="拖动${escapeHtml(ship.name)}">☰</button></div>`;
  }
  wireShipCard(card);
  return card;
}

function wireShipCard(card) {
  card.addEventListener('dragstart', () => {
    draggedCard = card;
    card.classList.add('dragging');
  });
  card.addEventListener('dragend', () => {
    draggedCard = null;
    card.classList.remove('dragging');
    document.querySelectorAll('.ship-card').forEach(item => item.classList.remove('drop-before', 'drop-after'));
  });
  card.addEventListener('dragover', event => {
    if (draggedCard?.parentElement !== card.parentElement || draggedCard === card) return;
    event.preventDefault();
    const cards = [...card.parentElement.querySelectorAll('.ship-card')];
    const movingDown = cards.indexOf(draggedCard) < cards.indexOf(card);
    card.classList.toggle('drop-before', !movingDown);
    card.classList.toggle('drop-after', movingDown);
  });
  card.addEventListener('dragleave', () => card.classList.remove('drop-before', 'drop-after'));
  card.addEventListener('drop', event => {
    event.preventDefault();
    card.classList.remove('drop-before', 'drop-after');
    if (!draggedCard || draggedCard === card || draggedCard.parentElement !== card.parentElement) return;
    const cards = [...card.parentElement.querySelectorAll('.ship-card')];
    card.parentElement.insertBefore(draggedCard, cards.indexOf(draggedCard) < cards.indexOf(card) ? card.nextSibling : card);
    updateAllSlots();
  });
  card.querySelector('.edit-ship').addEventListener('click', event => {
    event.stopPropagation();
    openEditor(card);
  });
  card.querySelector('.slot').addEventListener('click', event => {
    event.stopPropagation();
    card.remove();
    updateAllSlots();
  });
  card.querySelector('.slot').addEventListener('mouseenter', event => {
    event.currentTarget.textContent = '×';
  });
  card.querySelector('.slot').addEventListener('mouseleave', event => {
    event.currentTarget.textContent = event.currentTarget.dataset.number || '';
  });
  card.addEventListener('click', event => {
    if (!event.target.closest('button')) openEditor(card);
  });
}

function renderFleet(side, fleetConfig) {
  const list = side === 'friend' ? friendlyFleet : enemyFleet;
  list.replaceChildren(...(fleetConfig?.ships || []).slice(0, 6).map(ship => createShipCard(side, ship)));
  setFormation(side, Number(fleetConfig?.form) || 4);
  updateSlots(list, side === 'friend' ? addFriendly : addEnemy);
}

function populateStrategySelect(category, selected = '', level = 0) {
  const group = metadata.strategies[category];
  fillSelect(
    strategyEditors[category],
    group.items.map(item => ({ value: item.stid, label: item.name })),
    selected,
    `无${group.label}战术`,
  );
  strategyLevelEditors[category].value = Math.max(0, Math.min(3, Number(level) || 0));
}

function updateFriendEditorFields(config = null) {
  const ship = selectedEditorShip('friend');
  fillSelect(
    editorSkill,
    ship.skills.map(item => ({ value: item.id, label: item.name })),
    config?.skill ?? 0,
  );
  const selectedStrategies = strategyDetails(config || { strategy: [] });
  Object.keys(strategyEditors).forEach(category => populateStrategySelect(
    category,
    selectedStrategies[category]?.stid || '',
    selectedStrategies[category]?.level ?? 0,
  ));
  const equipmentByLoc = new Map((config?.equipment || []).map(item => [Number(item.loc), String(item.eid)]));
  equipmentEditors.forEach((input, index) => {
    const loc = index + 1;
    input.value = equipmentMap.get(equipmentByLoc.get(loc))?.name || '';
    equipmentPickers[index].setDisabled(loc > ship.equip_slots);
  });
}

function openEditor(card) {
  currentEditing = card;
  const isFriend = card.dataset.side === 'friend';
  const catalog = isFriend ? metadata.friend_ships : metadata.enemy_ships;
  setEditorShipOptions(catalog, isFriend, card._shipConfig.pending ? null : card._shipConfig.cid);
  editorLevelField.hidden = !isFriend;
  if (isFriend) editorLevel.value = card._shipConfig.level;
  friendEditorFields.hidden = !isFriend;
  if (isFriend) {
    editorAffection.value = card._shipConfig.affection;
    updateFriendEditorFields(card._shipConfig);
  }
  editor.showModal();
}

function syncEditorShipSelection() {
  if (!currentEditing) return;
  if (currentEditing.dataset.side !== 'friend') return;
  updateFriendEditorFields();
}

editorName.addEventListener('input', syncEditorShipSelection);
editorName.addEventListener('change', syncEditorShipSelection);
editorLevel.addEventListener('change', () => clampEditorInput(
  editorLevel,
  1,
  currentEditing?.dataset.side === 'friend' ? 110 : Infinity,
  currentEditing?.dataset.side === 'friend' ? 110 : 1,
));
editorAffection.addEventListener('change', () => clampEditorInput(editorAffection, 0, 200, 200));
Object.entries(strategyEditors).forEach(([category, select]) => select.addEventListener('change', () => {
  if (select.value && Number(strategyLevelEditors[category].value) === 0) strategyLevelEditors[category].value = 3;
}));
Object.values(strategyLevelEditors).forEach(input => input.addEventListener('change', () => clampEditorInput(input, 0, 3, 0)));

function saveCurrentShip() {
  if (!currentEditing) return;
  const isFriend = currentEditing.dataset.side === 'friend';
  if (!editorShipLabels.has(editorName.value.trim())) return false;
  const ship = selectedEditorShip(isFriend ? 'friend' : 'enemy');
  editorName.value = shipEditorLabel(ship, isFriend);
  const config = {
    loc: currentEditing._shipConfig.loc,
    cid: ship.cid,
    pending: false,
    level: isFriend ? clampEditorInput(editorLevel, 1, 110, 110) : Math.max(1, Number(ship.level) || 1),
    affection: isFriend ? clampEditorInput(editorAffection, 0, 200, 200) : 50,
    skill: isFriend ? Number(editorSkill.value) || 0 : 1,
  };
  if (isFriend) {
    config.equipment = equipmentEditors.flatMap((input, index) => {
      const eid = selectedEquipmentId(input.value);
      return input.disabled || !eid ? [] : [{ loc: index + 1, eid }];
    });
    config.strategy = Object.keys(strategyEditors).flatMap(category => {
      const stid = strategyEditors[category].value;
      return stid ? [{ stid, level: clampEditorInput(strategyLevelEditors[category], 0, 3, 0) }] : [];
    });
  }
  const replacement = createShipCard(isFriend ? 'friend' : 'enemy', config);
  currentEditing.replaceWith(replacement);
  currentEditing = replacement;
  updateAllSlots();
  return true;
}

document.querySelector('#save-ship').addEventListener('click', event => {
  event.preventDefault();
  if (saveCurrentShip()) editor.close('saved');
  else showNotice('请从列表中选择舰船', true);
});

document.querySelector('#delete-editor-ship').addEventListener('click', () => {
  if (!currentEditing) return;
  const list = currentEditing.parentElement;
  currentEditing.remove();
  updateSlots(list, list === friendlyFleet ? addFriendly : addEnemy);
  currentEditing = null;
});

addFriendly.addEventListener('click', () => {
  if (!metadata || friendlyFleet.children.length >= 6) return;
  friendlyFleet.append(createShipCard('friend'));
  updateAllSlots();
});

addEnemy.addEventListener('click', () => {
  if (!metadata || enemyFleet.children.length >= 6) return;
  enemyFleet.append(createShipCard('enemy'));
  updateAllSlots();
});

editor.addEventListener('keydown', event => {
  if (event.key === 'Enter') {
    event.preventDefault();
    if (saveCurrentShip()) editor.close('saved');
    else showNotice('请从列表中选择舰船', true);
  }
  if (event.key === 'Escape') {
    event.preventDefault();
    editor.close('cancel');
  }
});
editor.addEventListener('click', event => {
  [editorShipPicker, ...equipmentPickers].forEach(picker => {
    if (!picker.container.contains(event.target)) picker.close();
  });
});

function setupFormations() {
  document.querySelectorAll('.formation > div').forEach(container => {
    container.querySelectorAll('button').forEach((button, index) => {
      button.dataset.form = metadata.formations[index].id;
      button.textContent = metadata.formations[index].name;
      button.addEventListener('click', () => {
        container.querySelectorAll('button').forEach(item => item.classList.toggle('selected', item === button));
      });
    });
  });
}

function setFormation(side, form) {
  const container = document.querySelector(side === 'friend' ? '#friend-formation' : '#enemy-formation');
  container.querySelectorAll('button').forEach(button => button.classList.toggle('selected', Number(button.dataset.form) === form));
}

function getFormation(side) {
  const container = document.querySelector(side === 'friend' ? '#friend-formation' : '#enemy-formation');
  return Number(container.querySelector('.selected')?.dataset.form) || 4;
}

function setupBattleTypes(selectedId = null) {
  const menu = battleTypePicker.querySelector('.battle-type-menu');
  menu.replaceChildren(...metadata.battle_types.map(type => {
    const button = document.createElement('button');
    button.dataset.value = type.id;
    button.textContent = type.name;
    button.addEventListener('click', event => {
      event.preventDefault();
      setBattleType(type.id);
      battleTypePicker.open = false;
    });
    return button;
  }));
  setBattleType(selectedId || metadata.battle_types[0].id);
}

function setBattleType(id) {
  const accepted = metadata.battle_types.find(type => type.id === id) || metadata.battle_types[0];
  battleTypePicker.dataset.value = accepted.id;
  battleTypeValue.textContent = accepted.name;
  battleTypePicker.querySelectorAll('.battle-type-menu button').forEach(button => button.classList.toggle('selected', button.dataset.value === accepted.id));
}

function updateEpoch(value, manual = false) {
  const minimum = manual ? 1 : Number(epochRange.min);
  const epoch = Math.max(minimum, Math.min(1000000, Number(value) || minimum));
  epochValue.value = epoch;
  if (manual) epochRange.value = Math.max(Number(epochRange.min), Math.min(epoch, Number(epochRange.max)));
}

epochRange.addEventListener('input', () => updateEpoch(epochRange.value));
epochValue.addEventListener('input', () => updateEpoch(epochValue.value, true));
epochValue.addEventListener('click', () => epochValue.select());
epochValue.addEventListener('keydown', event => {
  if (event.key !== 'ArrowUp' && event.key !== 'ArrowDown') return;
  event.preventDefault();
  const current = Math.max(1, Number(epochValue.value) || 1);
  const next = event.key === 'ArrowUp'
    ? (current < 1000 ? 1000 : Math.min(1000000, current + 1000))
    : (current <= 1000 ? 1 : Math.max(1, current - 1000));
  updateEpoch(next, true);
});
roundsRange.addEventListener('input', () => { roundsValue.value = roundsRange.value; });

function buildFleetConfig(side) {
  const list = side === 'friend' ? friendlyFleet : enemyFleet;
  return {
    side: side === 'friend' ? 1 : 0,
    form: getFormation(side),
    ships: [...list.querySelectorAll('.ship-card')].map((card, index) => {
      const { pending, ...config } = cloneConfig(card._shipConfig);
      return { ...config, loc: index + 1 };
    }),
  };
}

function buildBattleConfig() {
  const friendFleet = buildFleetConfig('friend');
  const enemyFleetConfig = buildFleetConfig('enemy');
  if (!friendFleet.ships.length) throw new Error('我方舰队不能为空');
  if (!enemyFleetConfig.ships.length) throw new Error('敌方舰队不能为空');
  return {
    battle_type: battleTypePicker.dataset.value,
    friend_fleet: friendFleet,
    enemy_fleet: enemyFleetConfig,
  };
}

function removePendingShips() {
  let removed = 0;
  [friendlyFleet, enemyFleet].forEach(list => {
    [...list.querySelectorAll('.ship-card')].forEach(card => {
      if (!card._shipConfig.pending) return;
      card.remove();
      removed += 1;
    });
  });
  if (removed) updateAllSlots();
  return removed;
}

function applyConfig(config, target = null) {
  if (!config?.friend_fleet || !config?.enemy_fleet) throw new Error('配置文件缺少舰队信息');
  if (!target || target === 'friend') renderFleet('friend', config.friend_fleet);
  if (!target || target === 'enemy') renderFleet('enemy', config.enemy_fleet);
  if (!target) setBattleType(config.battle_type);
  setResultLog(target ? `已载入${target === 'friend' ? '我方' : '敌方'}舰队配置` : '已载入战斗配置，等待开始模拟');
}

function setSimulationButtonContent(icon, label, retry = false) {
  const iconContent = retry
    ? '<svg class="retry-svg" viewBox="0 0 24 24" aria-hidden="true"><path d="M3.2 8.5V2.8m0 5.7h5.7M4.4 7.1a8.5 8.5 0 1 1-.6 8.8"/></svg>'
    : icon === 'loading'
      ? '<svg class="running-svg" viewBox="0 0 24 24" aria-hidden="true"><g><line x1="12" y1="2.8" x2="12" y2="6.8" opacity="1"/><line x1="18.5" y1="5.5" x2="15.7" y2="8.3" opacity=".86"/><line x1="21.2" y1="12" x2="17.2" y2="12" opacity=".72"/><line x1="18.5" y1="18.5" x2="15.7" y2="15.7" opacity=".58"/><line x1="12" y1="21.2" x2="12" y2="17.2" opacity=".44"/><line x1="5.5" y1="18.5" x2="8.3" y2="15.7" opacity=".3"/><line x1="2.8" y1="12" x2="6.8" y2="12" opacity=".2"/><line x1="5.5" y1="5.5" x2="8.3" y2="8.3" opacity=".12"/></g></svg>'
      : '<svg class="play-svg" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4v16l12-8z"/></svg>';
  const iconClass = retry ? ' retry-icon' : icon === 'loading' ? ' running-icon' : ' play-icon';
  simulationButton.innerHTML = `<span class="simulation-content"><span class="simulation-icon${iconClass}">${iconContent}</span><span>${label}</span></span><span class="stop-content" aria-hidden="true"><span class="simulation-icon stop-icon"><svg class="stop-svg" viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="6" width="12" height="12" rx="1"/></svg></span><span>停止模拟</span></span>`;
}

function updateSimulationCountStat(value) {
  simulationCountStat.innerHTML = `${formatNumber(value)}<em>次</em>`;
}

function setDonut(chart, values, colors, indexes = null) {
  const total = values.reduce((sum, value) => sum + Math.max(0, Number(value) || 0), 0);
  chart._segments = [];
  if (!total) {
    chart.style.background = 'var(--soft)';
    renderChartOverlay(chart);
    return;
  }
  let cursor = 0;
  const segments = values.map((value, index) => {
    const start = cursor;
    cursor += Math.max(0, Number(value) || 0) / total * 100;
    chart._segments.push({ index: indexes?.[index] ?? index, start, end: cursor, color: colors[index % colors.length] });
    return `${colors[index % colors.length]} ${start}% ${cursor}%`;
  });
  chart.style.background = `conic-gradient(${segments.join(',')})`;
  renderChartOverlay(chart);
}

const CHART_OUTER_RADIUS = 50;
const CHART_INNER_RADIUS = 38;

function chartArcPoint(angle, radius = CHART_OUTER_RADIUS) {
  const radians = (angle - 90) * Math.PI / 180;
  return [50 + radius * Math.cos(radians), 50 + radius * Math.sin(radians)];
}

function renderChartOverlay(chart) {
  chart.querySelector('.chart-overlay')?.remove();
  const overlay = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  overlay.setAttribute('class', 'chart-overlay');
  overlay.setAttribute('viewBox', '0 0 100 100');
  (chart._segments || []).forEach(segment => {
    if (segment.end <= segment.start) return;
    const startAngle = segment.start / 100 * 360;
    const endAngle = segment.end / 100 * 360;
    const [startX, startY] = chartArcPoint(startAngle);
    const [endX, endY] = chartArcPoint(endAngle);
    const [innerStartX, innerStartY] = chartArcPoint(startAngle, CHART_INNER_RADIUS);
    const [innerEndX, innerEndY] = chartArcPoint(endAngle, CHART_INNER_RADIUS);
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    const largeArc = segment.end - segment.start > 50 ? 1 : 0;
    const fullCircle = segment.end - segment.start >= 99.999;
    path.dataset.index = String(segment.index);
    path.style.stroke = segment.color;
    path.setAttribute('d', fullCircle
      ? `M 50 ${50 - CHART_OUTER_RADIUS} A ${CHART_OUTER_RADIUS} ${CHART_OUTER_RADIUS} 0 1 1 50 ${50 + CHART_OUTER_RADIUS} A ${CHART_OUTER_RADIUS} ${CHART_OUTER_RADIUS} 0 1 1 50 ${50 - CHART_OUTER_RADIUS} M 50 ${50 - CHART_INNER_RADIUS} A ${CHART_INNER_RADIUS} ${CHART_INNER_RADIUS} 0 1 1 50 ${50 + CHART_INNER_RADIUS} A ${CHART_INNER_RADIUS} ${CHART_INNER_RADIUS} 0 1 1 50 ${50 - CHART_INNER_RADIUS}`
      : `M ${startX} ${startY} A ${CHART_OUTER_RADIUS} ${CHART_OUTER_RADIUS} 0 ${largeArc} 1 ${endX} ${endY} L ${innerEndX} ${innerEndY} A ${CHART_INNER_RADIUS} ${CHART_INNER_RADIUS} 0 ${largeArc} 0 ${innerStartX} ${innerStartY} Z`);
    overlay.append(path);
  });
  chart.prepend(overlay);
}

function chartSegmentAt(chart, event) {
  const rect = chart.getBoundingClientRect();
  const x = (event.clientX - rect.left) / rect.width - .5;
  const y = (event.clientY - rect.top) / rect.height - .5;
  if (Math.hypot(x, y) < .13) return null;
  const angle = (Math.atan2(y, x) * 180 / Math.PI + 450) % 360;
  const percent = angle / 360 * 100;
  return (chart._segments || []).find(segment => percent >= segment.start && percent < segment.end)?.index ?? null;
}

function setChartHighlight(chart, index) {
  chart.querySelectorAll('.chart-overlay path').forEach(path => {
    path.classList.toggle('highlighted', Number(path.dataset.index) === index);
  });
  chart._legend?.querySelectorAll('li').forEach(item => {
    item.classList.toggle('highlighted', Number(item.dataset.index) === index);
  });
}

function bindChartInteractions(chart, legend, onSegmentClick = null) {
  chart._legend = legend;
  chart._onSegmentClick = onSegmentClick;
  if (chart.dataset.interactive) return;
  chart.dataset.interactive = 'true';
  chart.addEventListener('mousemove', event => setChartHighlight(chart, chartSegmentAt(chart, event)));
  chart.addEventListener('mouseleave', () => setChartHighlight(chart, null));
  chart.addEventListener('click', event => {
    if (!chart._onSegmentClick) return;
    const index = event.target.closest('.chart-center') ? null : chartSegmentAt(chart, event);
    if (index !== null || event.target.closest('.chart-center')) chart._onSegmentClick(index);
  });
}

function renderLegend(list, entries, total, colors, slots = entries.length, options = {}) {
  const rows = Math.max(slots, entries.length);
  list.replaceChildren(...Array.from({ length: rows }, (_, index) => {
    const entry = entries[index];
    const value = entry ? Number(entry.value) || 0 : 0;
    const item = document.createElement('li');
    const entryIndex = entry?.index ?? index;
    item.dataset.index = String(entryIndex);
    item.classList.toggle('empty', !entry);
    item.classList.toggle('percent-only', options.percentOnly === true);
    item.classList.toggle('selected', entryIndex === options.selectedIndex);
    const marker = document.createElement('i');
    marker.style.background = entry ? colors[index % colors.length] : 'var(--line)';
    const name = document.createElement('span');
    name.textContent = entry?.name || '——';
    const percent = document.createElement('em');
    const percentDigits = options.percentDigits ?? 1;
    percent.textContent = entry && total ? `${(value / total * 100).toFixed(percentDigits)}%` : '——';
    item.append(marker, name);
    if (!options.percentOnly) {
      const count = document.createElement('b');
      count.textContent = entry ? formatNumber(value) : '——';
      item.append(count);
    }
    item.append(percent);
    if (entry && options.chart) {
      item.addEventListener('mouseenter', () => setChartHighlight(options.chart, entryIndex));
      item.addEventListener('mouseleave', () => setChartHighlight(options.chart, null));
      if (options.onSegmentClick) item.addEventListener('pointerdown', event => {
        if (!event.isPrimary || (event.pointerType === 'mouse' && event.button !== 0)) return;
        // While a simulation is running the legend is rebuilt every poll.
        // Handle selection on press, before that rebuild can discard the DOM
        // node and prevent the later click event from being dispatched.
        event.preventDefault();
        options.onSegmentClick(entryIndex);
      });
    }
    return item;
  }));
}

function renderRateList(list, entries, valueKey = 'rate') {
  list.replaceChildren(...Array.from({ length: 6 }, (_, index) => {
    const entry = entries[index];
    const item = document.createElement('li');
    item.classList.toggle('empty', !entry);
    const name = document.createElement('span');
    name.textContent = entry?.name || '——';
    const value = document.createElement('strong');
    value.textContent = entry ? (valueKey === 'rate' ? `${entry.rate.toFixed(1)}%` : formatNumber(entry.value, 1)) : '——';
    item.append(name, value);
    if (valueKey === 'rate') {
      const track = document.createElement('i');
      const bar = document.createElement('b');
      // Empty ship slots keep the row layout but must not look like a full
      // progress bar.  A block-level bar without an explicit width expands
      // to the entire track by default.
      bar.style.width = entry ? `${Math.max(0, Math.min(100, entry.rate))}%` : '0%';
      track.append(bar);
      item.append(track);
    }
    return item;
  }));
}

function renderSummary(summary) {
  if (!summary) {
    document.querySelector('#ship-damage-legend').hidden = true;
    return;
  }
  latestSummary = summary;
  document.querySelector('#win-rate-stat').innerHTML = `${summary.win_rate.toFixed(2)}<em>%</em>`;
  document.querySelector('#flagship-stat').innerHTML = `${summary.flagship_sink_rate.toFixed(2)}<em>%</em>`;
  document.querySelector('#average-damage-stat').textContent = formatNumber(summary.average_damage);
  document.querySelector('#average-loss-stat').textContent = formatNumber(summary.average_bucket, 2);
  document.querySelector('#resource-stat').textContent = formatNumber(summary.resource_total, 1);
  const prebattle = summary.prebattle || {};
  const reconRate = Number(prebattle.recon_rate);
  document.querySelector('#recon-rate-value').innerHTML = Number.isFinite(reconRate)
    ? `${reconRate.toFixed(0)}<small>%</small>`
    : '—<small>%</small>';
  document.querySelector('#friend-recon-value').textContent = Number.isFinite(Number(prebattle.friend_recon))
    ? formatNumber(prebattle.friend_recon, 0) : '—';
  document.querySelector('#recon-request-value').textContent = Number.isFinite(Number(prebattle.recon_request))
    ? formatNumber(prebattle.recon_request, 0) : '—';
  document.querySelector('#air-con-value').textContent = prebattle.air_con || '—';
  document.querySelector('#friend-aerial-value').textContent = Number.isFinite(Number(prebattle.friend_aerial))
    ? formatNumber(prebattle.friend_aerial, 2) : '—';
  document.querySelector('#enemy-aerial-value').textContent = Number.isFinite(Number(prebattle.enemy_aerial))
    ? formatNumber(prebattle.enemy_aerial, 2) : '—';

  const flags = ['SS', 'S', 'A', 'B', 'C', 'D'];
  const flagNames = ['SS 完胜', 'S 胜利', 'A 小胜', 'B 战术胜利', 'C 战术失败', 'D 失败'];
  const counts = flags.map(flag => summary.result_counts[flag] || 0);
  const totalCount = counts.reduce((sum, value) => sum + value, 0);
  const winChart = document.querySelector('#win-chart');
  const winLegend = document.querySelector('#win-legend');
  document.querySelector('#win-chart-value').innerHTML = `${summary.win_rate.toFixed(2)}<small>%</small>`;
  setDonut(winChart, counts, ['var(--ss)', 'var(--s)', 'var(--a)', 'var(--b)', 'var(--c)', 'var(--d)']);
  const winColors = ['var(--ss)', 'var(--s)', 'var(--a)', 'var(--b)', 'var(--c)', 'var(--d)'];
  renderLegend(winLegend, counts.map((value, index) => ({ name: flagNames[index], value, index })), totalCount, winColors, 6, { chart: winChart, percentOnly: true, percentDigits: 2 });
  bindChartInteractions(winChart, winLegend);

  const phaseValues = summary.phase_damage.map(item => item.value);
  const damageTotal = phaseValues.reduce((sum, value) => sum + value, 0);
  const phaseColors = ['var(--phase-1)', 'var(--phase-2)', 'var(--phase-3)', 'var(--phase-4)', 'var(--phase-5)',
                               'var(--phase-6)', 'var(--phase-7)', 'var(--phase-8)', 'var(--phase-9)', 'var(--phase-10)', 'var(--phase-11)'];
  const damageChart = document.querySelector('#damage-chart');
  const phaseLegend = document.querySelector('#phase-legend');
  document.querySelector('#damage-chart-value').textContent = formatNumber(summary.average_damage);
  document.querySelector('#damage-floor-value').textContent = formatNumber(summary.damage_floor_5);
  setDonut(damageChart, phaseValues, phaseColors, summary.phase_damage.map(entry => entry.index));
  const selectDamagePhase = index => {
    damagePhaseFilter = damagePhaseFilter === index ? null : index;
    renderSummary(latestSummary);
  };
  renderLegend(phaseLegend, summary.phase_damage, damageTotal, phaseColors, summary.phase_damage.length, {
    chart: damageChart,
    onSegmentClick: selectDamagePhase,
    selectedIndex: damagePhaseFilter,
  });
  bindChartInteractions(damageChart, phaseLegend, selectDamagePhase);

  const selectedPhase = damagePhaseFilter === null ? null : summary.ship_damage_by_phase?.[damagePhaseFilter];
  const shipEntries = selectedPhase?.ships || summary.ship_damage;
  const shipValues = shipEntries.map(item => item.value);
  const shipTotal = shipValues.reduce((sum, value) => sum + value, 0);
  const shipColors = ['var(--ss)', 'var(--s)', 'var(--a)', 'var(--b)', 'var(--c)', 'var(--d)'];
  const shipChart = document.querySelector('#ship-damage-chart');
  const shipLegend = document.querySelector('#ship-damage-legend');
  shipLegend.hidden = shipEntries.length === 0;
  document.querySelector('#ship-damage-chart-value').textContent = formatNumber(shipTotal);
  document.querySelector('#ship-damage-chart-label').textContent = selectedPhase ? `${selectedPhase.name}伤害` : '舰船伤害';
  setDonut(shipChart, shipValues, shipColors);
  renderLegend(shipLegend, shipEntries, shipTotal, shipColors, 6, { chart: shipChart });
  bindChartInteractions(shipChart, shipLegend);

  document.querySelector('#oil-value').textContent = formatNumber(summary.supply.oil, 1);
  document.querySelector('#ammo-value').textContent = formatNumber(summary.supply.ammo, 1);
  document.querySelector('#steel-value').textContent = formatNumber(summary.supply.steel, 1);
  document.querySelector('#aluminum-value').textContent = formatNumber(summary.supply.almn, 1);
  renderRateList(document.querySelector('#friend-mid-rates'), summary.friend_mid_damage_rates);
  renderRateList(document.querySelector('#friend-heavy-rates'), summary.friend_heavy_damage_rates);
  renderRateList(document.querySelector('#enemy-sink-rates'), summary.enemy_sink_rates);
  renderRateList(document.querySelector('#enemy-health-rates'), summary.enemy_remaining_health, 'value');
  document.querySelector('#battle-detail').textContent = summary.battle_detail
    ? `${summary.battle_detail}`
    : '本轮模拟尚未生成战斗详情。';
}

function renderSimulationStatus(status) {
  if (simulationDisplayFrozen) return;
  latestSimulation = status;
  const wasStopping = simulationState === 'stopping';
  const liveCompleted = status.live_completed ?? status.completed ?? 0;
  const liveProgress = status.live_progress ?? status.progress ?? 0;
  simulationState = status.state;
  setResultLog(status.log || status.message || '');
  renderSummary(status.summary);
  updateSimulationCountStat(liveCompleted);
  if (status.state === 'stopping' || (wasStopping && status.state === 'running')) {
    simulationState = 'stopping';
    simulationButton.classList.add('running', 'stopping');
    simulationButton.style.setProperty('--run-progress', `${liveProgress}%`);
    const requestedCompleted = status.stop_requested_completed ?? liveCompleted;
    setSimulationButtonContent('loading', `正在停止模拟… ${formatNumber(requestedCompleted)} 次`);
    return;
  }
  if (status.state === 'running') {
    simulationButton.classList.add('running');
    simulationButton.classList.remove('stopping');
    simulationButton.style.setProperty('--run-progress', `${liveProgress}%`);
    setSimulationButtonContent('loading', `正在模拟… ${formatNumber(liveCompleted)} / ${formatNumber(status.target)}`);
    return;
  }
  simulationButton.classList.remove('running', 'stopping');
  simulationButton.style.removeProperty('--run-progress');
  if (status.state === 'idle') setSimulationButtonContent('play', '开始模拟');
  else setSimulationButtonContent('retry', '再次模拟', true);
  if (status.state === 'complete' || status.state === 'stopped') updateSimulationCountStat(status.completed);
  if (status.state === 'error') showNotice(status.message || '模拟失败', true);
}

async function pollSimulation() {
  clearTimeout(pollTimer);
  statusAbortController?.abort();
  const controller = new AbortController();
  statusAbortController = controller;
  try {
    const status = await api('/api/simulation/status', { signal: controller.signal });
    renderSimulationStatus(status);
    if (!simulationDisplayFrozen && (status.state === 'running' || status.state === 'stopping')) {
      pollTimer = setTimeout(pollSimulation, 20);
    }
  } catch (error) {
    if (!simulationDisplayFrozen && error.name !== 'AbortError') showNotice(error.message, true);
  } finally {
    if (statusAbortController === controller) statusAbortController = null;
  }
}

async function startSimulation() {
  try {
    simulationDisplayFrozen = false;
    removePendingShips();
    const status = await api('/api/simulation/start', {
      method: 'POST',
      body: JSON.stringify({
        config: buildBattleConfig(),
        epoch: Number(epochValue.value) || 1,
        battle_num: Number(roundsValue.value) || 1,
      }),
    });
    renderSimulationStatus(status);
    pollTimer = setTimeout(pollSimulation, 20);
  } catch (error) {
    showNotice(error.message, true);
  }
}

function freezeSimulationDisplay() {
  if (simulationDisplayFrozen || simulationState !== 'running') return;
  simulationDisplayFrozen = true;
  clearTimeout(pollTimer);
  statusAbortController?.abort();
  simulationButton.classList.remove('running', 'stopping');
  simulationButton.style.removeProperty('--run-progress');
  setSimulationButtonContent('retry', '再次模拟', true);
}

async function toggleSimulation() {
  if (simulationState === 'stopping') return;
  if (simulationState !== 'running') {
    await startSimulation();
    return;
  }
  try {
    freezeSimulationDisplay();
    simulationState = 'stopping';
    const status = await api('/api/simulation/stop', { method: 'POST', body: '{}' });
    simulationState = status.state;
  } catch {
    // The display is deliberately already frozen.  A later start request can retry safely.
    simulationState = 'stopped';
  }
}

let simulationToggleInFlight = false;
simulationButton.addEventListener('pointerdown', event => {
  if (!event.isPrimary || (event.pointerType === 'mouse' && event.button !== 0)) return;
  freezeSimulationDisplay();
});
simulationButton.addEventListener('click', event => {
  event.preventDefault();
  if (simulationToggleInFlight) return;
  simulationToggleInFlight = true;
  void toggleSimulation().finally(() => { simulationToggleInFlight = false; });
});

document.querySelector('#load-config').addEventListener('click', () => {
  loadTarget = null;
  configFileInput.click();
});
clearWorkspaceButton.addEventListener('click', () => clearConfirmDialog.showModal());
document.querySelector('#confirm-clear').addEventListener('click', () => {
  clearConfirmDialog.close('confirmed');
  void clearWorkspace();
});
document.querySelectorAll('.fleet-load').forEach(button => button.addEventListener('click', () => {
  loadTarget = button.dataset.side;
  configFileInput.click();
}));

configFileInput.addEventListener('change', async () => {
  const file = configFileInput.files[0];
  configFileInput.value = '';
  if (!file) return;
  try {
    const payload = await api('/api/config/import', {
      method: 'POST',
      body: JSON.stringify({ filename: file.name, content: await file.text() }),
    });
    applyConfig(payload.config, loadTarget);
    showNotice(loadTarget ? '舰队配置已载入' : '战斗配置已载入');
  } catch (error) {
    showNotice(error.message, true);
  }
});

function downloadBlob(content, filename, type) {
  const link = document.createElement('a');
  link.href = URL.createObjectURL(new Blob([content], { type }));
  link.download = filename;
  link.click();
  setTimeout(() => URL.revokeObjectURL(link.href), 1000);
}

document.querySelector('#save-config').addEventListener('click', async () => {
  try {
    const response = await fetch('/api/config/export', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ config: buildBattleConfig() }),
    });
    if (!response.ok) throw new Error((await response.json()).error || '保存失败');
    downloadBlob(await response.text(), 'wsgr_config.yaml', 'application/yaml;charset=utf-8');
    showNotice('配置文件已生成');
  } catch (error) {
    showNotice(error.message, true);
  }
});

document.querySelector('#export-report').addEventListener('click', () => {
  if (!latestSimulation?.summary) {
    showNotice('请先完成至少一次模拟', true);
    return;
  }
  const summary = latestSimulation.summary;
  const content = [
    'WSGR 战斗模拟报告',
    `实际模拟次数：${latestSimulation.completed}`,
    `综合胜率：${summary.win_rate.toFixed(2)}%`,
    `旗舰击沉率：${summary.flagship_sink_rate.toFixed(2)}%`,
    `平均伤害：${summary.average_damage.toFixed(1)}`,
    `平均桶耗：${summary.average_bucket.toFixed(2)}`,
    `资源消耗：油 ${summary.supply.oil.toFixed(1)} / 弹 ${summary.supply.ammo.toFixed(1)} / 钢 ${summary.supply.steel.toFixed(1)} / 铝 ${summary.supply.almn.toFixed(1)}`,
    '',
    '【一场战斗详情】',
    summary.battle_detail || '无',
  ].join('\n');
  downloadBlob(content, 'wsgr_battle_report.txt', 'text/plain;charset=utf-8');
});

const resultTabs = document.querySelectorAll('.result-tabs button');
const resultPanels = document.querySelectorAll('.result-view-panel');
resultTabs.forEach(tab => tab.addEventListener('click', () => {
  resultTabs.forEach(item => {
    const selected = item === tab;
    item.classList.toggle('active', selected);
    item.setAttribute('aria-selected', String(selected));
  });
  resultPanels.forEach(panel => {
    const selected = panel.dataset.panel === tab.dataset.view;
    panel.hidden = !selected;
    panel.classList.toggle('active', selected);
  });
}));

const modeSwitch = document.querySelector('#mode-switch');
modeSwitch.addEventListener('click', () => {
  const dark = document.body.classList.toggle('dark');
  modeSwitch.setAttribute('aria-pressed', String(dark));
});

document.querySelectorAll('.topbar nav button').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('.topbar nav button').forEach(item => item.classList.toggle('active', item === button));
  document.title = `WSGR · ${button.textContent.trim()}`;
}));

async function initialise() {
  try {
    metadata = await api('/api/bootstrap');
    friendShipMap = new Map(metadata.friend_ships.map(ship => [ship.cid, ship]));
    enemyShipMap = new Map(metadata.enemy_ships.map(ship => [ship.cid, ship]));
    equipmentMap = new Map(metadata.equipment.map(item => [item.eid, item]));
    setEquipmentOptions();
    strategyMap = new Map();
    Object.entries(metadata.strategies).forEach(([category, group]) => {
      group.items.forEach(item => strategyMap.set(item.stid, { ...item, category }));
    });
    setupFormations();
    setupBattleTypes(metadata.config.battle_type);
    // A full page reload starts a fresh WebUI session.  Do not restore the
    // previous server snapshot (or leave its worker running) into this page.
    await api('/api/simulation/reset', { method: 'POST', body: '{}' });
    applyConfig(metadata.config);
    resetResultDisplay();
    simulationState = 'idle';
    updateSimulationCountStat(0);
    setSimulationButtonContent('play', '开始模拟');
  } catch (error) {
    setResultLog(`WebUI 初始化失败：${error.message}`);
    showNotice(error.message, true);
  }
}

void initialise();
