(function () {
  'use strict';

  const WORLD_WIDTH = 1000;
  const WORLD_HEIGHT = 680;
  const NODE_SIZE = 10;
  const FORMATIONS = { 1: '单纵', 2: '复纵', 3: '轮形', 4: '梯形', 5: '单横' };
  const LEVEL_NAMES = {
    0: '入口',
    1: '出门点',
    2: '道中点',
    3: '门神点',
    4: '非 Boss 终点',
    5: 'Boss',
  };
  const NODE_KINDS = ['no_battle', 'resource_gain', 'resource_loss', 'normal', 'air', 'night', 'elite', 'boss'];
  const KIND_BATTLE_TYPES = {
    entrance: 'Entrance',
    no_battle: 'MidPoint',
    resource_gain: 'ResourcePoint',
    resource_loss: 'ResourcePoint',
    normal: 'NormalBattle',
    air: 'AirBattle',
    night: 'NightBattle',
    elite: 'NormalBattle',
    boss: 'NormalBattle',
  };
  const NON_COMBAT_BATTLE_TYPES = new Set(['Entrance', 'MidPoint', 'ResourcePoint']);
  const RESOURCE_TYPES = new Set(['oil', 'ammo', 'steel', 'almn']);
  let shipTypes = [
    ['BB', '战列舰'], ['BC', '战列巡洋舰'], ['CV', '航空母舰'], ['CVL', '轻型航母'],
    ['CA', '重巡洋舰'], ['CL', '轻巡洋舰'], ['DD', '驱逐舰'], ['SS', '潜艇'],
  ];
  const STATUS_FIELDS = [
    ['low_speed', '最低航速'], ['high_speed', '最高航速'], ['avg_speed', '平均航速'],
    ['leader_speed', '旗舰航速'], ['speed', '舰队航速'], ['recon', '索敌值'],
    ['antisub_recon', '反潜索敌'], ['luck', '幸运合计'], ['level', '等级合计'],
  ];
  const NUMBER_OPERATORS = [
    ['lt', '<'], ['le', '≤'], ['eq', '='], ['ge', '≥'], ['gt', '>'],
  ];
  const USER_RULE_DEFAULTS = {
    formation: 2,
    formation_if_recon_fails: false,
    long_missile: false,
    night: false,
    round: true,
    rules: [],
    retreat_if_recon_fails: false,
    retreat_if_round_fails: true,
    proceed: true,
    proceed_stop: [2, 2, 2, 2, 2, 2],
  };

  function shipTypeOptions() {
    return shipTypes;
  }

  const dom = {
    mapName: document.querySelector('#map-name'),
    viewport: document.querySelector('#canvas-viewport'),
    world: document.querySelector('#canvas-world'),
    routeLayer: document.querySelector('#route-layer'),
    routeLabelLayer: document.querySelector('#route-label-layer'),
    nodeLayer: document.querySelector('#node-layer'),
    modeTitle: document.querySelector('#mode-title'),
    modeHint: document.querySelector('#mode-hint'),
    emptyInspector: document.querySelector('#empty-inspector'),
    nodeInspector: document.querySelector('#node-inspector'),
    routeInspector: document.querySelector('#route-inspector'),
    fleetList: document.querySelector('#fleet-list'),
    conditionList: document.querySelector('#condition-list'),
    toast: document.querySelector('#map-notice'),
    yamlFile: document.querySelector('#map-yaml-file'),
    confirmDialog: document.querySelector('#map-confirm-dialog'),
    mapEditorLayout: document.querySelector('#map-editor-layout'),
    mapResultScreen: document.querySelector('#map-result-screen'),
    mapViewButtons: document.querySelectorAll('[data-map-view]'),
    undoButton: document.querySelector('#undo-map-edit'),
    strategyDialog: document.querySelector('#map-strategy-dialog'),
    strategyForm: document.querySelector('#map-strategy-form'),
    strategyAllNodes: document.querySelector('#strategy-all-nodes'),
    strategyNodePicker: document.querySelector('#strategy-node-picker'),
    strategyScope: document.querySelector('#strategy-scope'),
    strategyFormation: document.querySelector('#strategy-formation'),
    strategyFormationRecon: document.querySelector('#strategy-formation-recon'),
    strategyLongMissile: document.querySelector('#strategy-long-missile'),
    strategyNight: document.querySelector('#strategy-night'),
    strategyRound: document.querySelector('#strategy-round'),
    strategyRoundThresholdField: document.querySelector('#strategy-round-threshold-field'),
    strategyRoundThreshold: document.querySelector('#strategy-round-threshold'),
    strategyRetreatRecon: document.querySelector('#strategy-retreat-recon'),
    strategyRetreatRound: document.querySelector('#strategy-retreat-round'),
    strategyProceed: document.querySelector('#strategy-proceed'),
    strategyProceedStop: document.querySelector('#strategy-proceed-stop'),
    strategyRules: document.querySelector('#strategy-rules'),
    mapEffectDialog: document.querySelector('#map-effect-dialog'),
    mapEffectPointName: document.querySelector('#map-effect-point-name'),
    mapEffectList: document.querySelector('#map-effect-list'),
    mapEffectEmpty: document.querySelector('#map-effect-empty'),
    mapEffectCatalog: document.querySelector('#map-effect-catalog'),
    mapEffectCatalogList: document.querySelector('#map-effect-catalog-list'),
    mapEffectCatalogToggle: document.querySelector('#show-map-effect-catalog'),
  };

  let mapDocument = createDefaultDocument();
  let selection = { type: 'node', id: 'node-entrance' };
  let interactionMode = 'select';
  let connectionSourceId = null;
  let idCounter = 1;
  let toastTimer = 0;
  let suppressNodeClick = false;
  let activeMapView = 'editor';
  let mapUserRules = createDefaultUserRules();
  let activeStrategyScope = '__default__';
  const strategyDrafts = new Map();
  const undoStack = [];
  const MAX_UNDO_STEPS = 50;
  const fleetStatsCache = new Map();
  let mapEffectOptions = null;
  let mapEffectNodeId = null;
  let mapEffectCatalogOpen = false;

  function uid(prefix) {
    idCounter += 1;
    return `${prefix}-${Date.now().toString(36)}-${idCounter.toString(36)}`;
  }

  function createDefaultDocument() {
    return {
      map: {
        mapid: '未命名海图',
        name: '未命名海图',
        entrance: 'node-entrance',
        canvas: { width: WORLD_WIDTH, height: WORLD_HEIGHT },
        nodes: [{
          id: 'node-entrance',
          name: '入口',
          kind: 'entrance',
          level: 0,
          level_auto: true,
          position: { x: 80, y: 318 },
          battle: { type: 'Entrance', roundabout: false, support: false },
          enemy_fleets: [],
          map_effects: [],
        }],
        routes: [],
      },
    };
  }

  function nodeData(id, name, kind, x, y, fleets, roundabout = false, support = false) {
    return {
      id, name, kind, level: kind === 'entrance' ? 0 : 2, level_auto: true,
      position: { x, y },
      battle: { type: battleTypeForKind(kind), roundabout, support },
      enemy_fleets: fleets,
      map_effects: [],
    };
  }

  function fleetData(id, name, formation, ships) {
    return { id, name, formation, ships };
  }

  function shipData(loc, cid, name, level) {
    return { loc, cid, name, level };
  }

  function routeData(id, from, to, weight, conditions = []) {
    return { id, from, to, weight, relation: 'all', conditions };
  }

  function currentMap() {
    return mapDocument.map;
  }

  function cloneMapData(value) {
    return JSON.parse(JSON.stringify(value));
  }

  function createDefaultUserRules() {
    return {
      selected_nodes: 'all',
      node_defaults: cloneMapData(USER_RULE_DEFAULTS),
      node_args: {},
    };
  }

  function strategyNodeNames() {
    return currentMap().nodes
      .filter(node => node.id !== currentMap().entrance)
      .map(node => node.name);
  }

  function normalizeMapUserRules() {
    const names = new Set(currentMap().nodes.map(node => node.name));
    const combatNames = new Set(strategyNodeNames());
    if (Array.isArray(mapUserRules.selected_nodes)) {
      mapUserRules.selected_nodes = [...new Set(mapUserRules.selected_nodes)]
        .filter(name => combatNames.has(name));
    }
    mapUserRules.node_args = Object.fromEntries(
      Object.entries(mapUserRules.node_args || {}).filter(([name]) => names.has(name)),
    );
  }

  function loadMapUserRules(value) {
    const defaults = createDefaultUserRules();
    if (!value || typeof value !== 'object' || Array.isArray(value)) {
      mapUserRules = defaults;
      return;
    }
    mapUserRules = {
      selected_nodes: value.selected_nodes === 'all' || Array.isArray(value.selected_nodes)
        ? cloneMapData(value.selected_nodes) : defaults.selected_nodes,
      node_defaults: { ...defaults.node_defaults, ...(value.node_defaults || {}) },
      node_args: value.node_args && typeof value.node_args === 'object' && !Array.isArray(value.node_args)
        ? cloneMapData(value.node_args) : {},
    };
    normalizeMapUserRules();
  }

  function strategySourceSettingsFor(scope) {
    if (scope === '__default__') return cloneMapData(mapUserRules.node_defaults);
    const defaults = strategyDrafts.get('__default__') || mapUserRules.node_defaults;
    return { ...cloneMapData(defaults), ...cloneMapData(mapUserRules.node_args[scope] || {}) };
  }

  function strategySettingsFor(scope) {
    if (scope === '__default__') {
      return cloneMapData(strategyDrafts.get(scope) || strategySourceSettingsFor(scope));
    }
    return {
      ...strategySourceSettingsFor(scope),
      ...cloneMapData(strategyDrafts.get(scope) || {}),
    };
  }

  function formatStrategyRules(rules) {
    return (rules || []).map(([condition, action]) => `${condition} => ${action}`).join('\n');
  }

  function parseStrategyRules(value) {
    return value.split('\n').map(line => line.trim()).filter(Boolean).map((line, index) => {
      const separator = line.indexOf('=>');
      if (separator < 1) throw new Error(`第 ${index + 1} 条规则需使用 => 分隔条件和操作`);
      const condition = line.slice(0, separator).trim();
      const action = line.slice(separator + 2).trim();
      if (!condition || !/^(retreat|round|[1-5])$/.test(action)) {
        throw new Error(`第 ${index + 1} 条规则的操作必须是 retreat、round 或 1–5`);
      }
      return [condition, action];
    });
  }

  function updateUndoButton() {
    dom.undoButton.disabled = undoStack.length === 0;
  }

  function pushUndo(action) {
    undoStack.push(action);
    if (undoStack.length > MAX_UNDO_STEPS) undoStack.shift();
    updateUndoButton();
  }

  function clearUndoHistory() {
    undoStack.length = 0;
    updateUndoButton();
  }

  function undoLastMapEdit() {
    const action = undoStack.pop();
    updateUndoButton();
    if (!action) return;

    if (action.type === 'add-node') {
      currentMap().nodes = currentMap().nodes.filter(node => node.id !== action.nodeId);
      currentMap().routes = currentMap().routes.filter(route => route.from !== action.nodeId && route.to !== action.nodeId);
      selection = { type: 'node', id: currentMap().entrance };
    } else if (action.type === 'delete-node') {
      currentMap().nodes.splice(Math.min(action.index, currentMap().nodes.length), 0, cloneMapData(action.node));
      [...action.routes]
        .sort((left, right) => left.index - right.index)
        .forEach(item => currentMap().routes.splice(
          Math.min(item.index, currentMap().routes.length), 0, cloneMapData(item.route),
        ));
      selection = { type: 'node', id: action.node.id };
    } else if (action.type === 'add-route') {
      currentMap().routes = currentMap().routes.filter(route => route.id !== action.routeId);
      selection = { type: 'node', id: action.from };
    } else if (action.type === 'delete-route') {
      currentMap().routes.splice(
        Math.min(action.index, currentMap().routes.length), 0, cloneMapData(action.route),
      );
      selection = { type: 'route', id: action.route.id };
    }
    render();
  }

  function switchMapView(view) {
    if (!['editor', 'result'].includes(view)) return;
    activeMapView = view;
    dom.mapViewButtons.forEach(button => button.classList.toggle('active', button.dataset.mapView === view));
    dom.mapEditorLayout.hidden = view !== 'editor';
    dom.mapResultScreen.hidden = view !== 'result';
  }

  function battleTypeForKind(kind) {
    return KIND_BATTLE_TYPES[kind] || 'NormalBattle';
  }

  function isCombatNode(node) {
    return !NON_COMBAT_BATTLE_TYPES.has(node.battle.type);
  }

  function isResourceNode(node) {
    return node.kind === 'resource_gain' || node.kind === 'resource_loss';
  }

  function canRoundabout(node) {
    return isCombatNode(node) && node.kind !== 'boss';
  }

  function recalculateNodeLevels(map = currentMap()) {
    const incoming = new Map(map.nodes.map(node => [node.id, []]));
    const outgoing = new Map(map.nodes.map(node => [node.id, []]));
    map.routes.forEach(route => {
      incoming.get(route.to)?.push(route);
      outgoing.get(route.from)?.push(route);
    });
    const bossIds = new Set(map.nodes.filter(node => node.kind === 'boss').map(node => node.id));

    map.nodes.forEach(node => {
      let calculatedLevel = 2;
      if (node.id === map.entrance) {
        node.kind = 'entrance';
        node.battle.roundabout = false;
        node.level_auto = true;
        calculatedLevel = 0;
      } else if (node.kind === 'boss') {
        calculatedLevel = 5;
      } else if ((outgoing.get(node.id) || []).some(route => bossIds.has(route.to))) {
        calculatedLevel = 3;
      } else if ((incoming.get(node.id) || []).some(route => route.from === map.entrance)) {
        calculatedLevel = 1;
      } else if ((incoming.get(node.id) || []).length > 0 && (outgoing.get(node.id) || []).length === 0) {
        calculatedLevel = 4;
      }
      if (node.level_auto !== false) node.level = calculatedLevel;
      node.battle.type = battleTypeForKind(node.kind);
      if (!isCombatNode(node)) {
        node.battle.roundabout = false;
        node.battle.support = false;
      }
      if (node.kind === 'boss') node.battle.roundabout = false;
    });
  }

  function getNode(id) {
    return currentMap().nodes.find(node => node.id === id);
  }

  function getRoute(id) {
    return currentMap().routes.find(route => route.id === id);
  }

  function showToast(message, error = false) {
    window.clearTimeout(toastTimer);
    dom.toast.textContent = message;
    dom.toast.classList.toggle('error', error);
    dom.toast.hidden = false;
    toastTimer = window.setTimeout(() => { dom.toast.hidden = true; }, 2600);
  }

  function closeMapSelectPickers(except = null) {
    document.querySelectorAll('.map-select-picker.open').forEach(picker => {
      if (picker !== except) picker._mapPickerClose?.();
    });
  }

  function closeMapSearchablePickers(except = null) {
    document.querySelectorAll('.map-searchable-picker.open').forEach(picker => {
      if (picker !== except) picker._mapSearchablePicker?.close();
    });
  }

  function setupMapSearchablePicker(select) {
    if (select._mapSearchablePicker) {
      select._mapSearchablePicker.sync();
      return select._mapSearchablePicker;
    }
    const picker = document.createElement('span');
    picker.className = 'searchable-picker searchable-select-picker map-searchable-picker';
    const input = document.createElement('input');
    input.type = 'text';
    input.autocomplete = 'off';
    input.setAttribute('aria-autocomplete', 'list');
    input.setAttribute('aria-label', '地图效果');
    const toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'picker-toggle';
    toggle.setAttribute('aria-label', '展开地图效果列表');
    toggle.textContent = '⌄';
    const menu = document.createElement('span');
    menu.className = 'picker-menu';
    menu.setAttribute('role', 'listbox');
    const items = document.createElement('span');
    items.className = 'picker-menu-scroll';
    menu.append(items);
    select.before(picker);
    picker.append(select, input, toggle, menu);

    let menuPortaled = false;
    const selectedText = () => select.selectedOptions[0]?.textContent || '';
    const restoreMenu = () => {
      if (!menuPortaled) return;
      menu.classList.remove('picker-menu-portal');
      menu.removeAttribute('style');
      picker.append(menu);
      menuPortaled = false;
    };
    const close = () => {
      picker.classList.remove('open');
      input.setAttribute('aria-expanded', 'false');
      input.value = selectedText();
      restoreMenu();
    };
    const portalMenu = () => {
      const dialog = picker.closest('.map-effect-dialog');
      if (!dialog) return;
      const pickerBox = picker.getBoundingClientRect();
      const dialogBox = dialog.getBoundingClientRect();
      dialog.append(menu);
      menu.classList.add('picker-menu-portal');
      Object.assign(menu.style, {
        top: `${pickerBox.bottom - dialogBox.top + 2}px`,
        left: `${pickerBox.left - dialogBox.left}px`,
        width: `${pickerBox.width}px`,
      });
      menuPortaled = true;
    };
    const render = () => {
      const selectedLabel = selectedText();
      const query = input.value.trim().toLocaleLowerCase('zh-CN');
      const allOptions = [...select.options];
      const matched = !query || query === selectedLabel.toLocaleLowerCase('zh-CN')
        ? allOptions
        : allOptions.filter(option => option.textContent.toLocaleLowerCase('zh-CN').includes(query));
      const choices = matched.length ? matched : allOptions;
      items.replaceChildren(...choices.map(option => {
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
    const open = () => {
      if (select.disabled) return;
      closeMapSelectPickers();
      closeMapSearchablePickers(picker);
      render();
      picker.classList.add('open');
      input.setAttribute('aria-expanded', 'true');
      portalMenu();
    };
    const sync = () => {
      input.value = selectedText();
      input.disabled = select.disabled;
      toggle.disabled = select.disabled;
      picker.classList.toggle('disabled', select.disabled);
      if (select.disabled) close();
      else render();
    };
    select._mapSearchablePicker = {
      close,
      sync,
      containsTarget: target => picker.contains(target) || menu.contains(target),
    };
    picker._mapSearchablePicker = select._mapSearchablePicker;
    input.addEventListener('focus', open);
    input.addEventListener('input', open);
    input.addEventListener('keydown', event => {
      if (event.key === 'Escape') {
        event.preventDefault();
        close();
      } else if (event.key === 'Enter') {
        event.preventDefault();
        event.stopPropagation();
        open();
      }
    });
    toggle.addEventListener('mousedown', event => event.preventDefault());
    toggle.addEventListener('click', () => {
      if (picker.classList.contains('open')) close();
      else {
        input.focus();
        open();
      }
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
    picker.closest('.map-effect-settings-content, #route-inspector')?.addEventListener('scroll', close);
    sync();
    return select._mapSearchablePicker;
  }

  document.addEventListener('pointerdown', event => {
    if (!(event.target instanceof Node)) return;
    document.querySelectorAll('.map-searchable-picker.open').forEach(picker => {
      if (!picker._mapSearchablePicker?.containsTarget(event.target)) picker._mapSearchablePicker.close();
    });
  });

  function enhanceMapSelects(root = dom.mapEditorLayout) {
    root.querySelectorAll('select').forEach(select => {
      if (select._mapSearchablePicker) {
        select._mapSearchablePicker.sync();
        return;
      }
      if (select._mapPickerRefresh) {
        select._mapPickerRefresh();
        return;
      }
      const picker = document.createElement('span');
      picker.className = 'map-select-picker';
      const toggle = document.createElement('button');
      toggle.type = 'button';
      toggle.className = 'map-select-toggle';
      const value = document.createElement('span');
      value.className = 'map-select-value';
      const caret = document.createElement('b');
      caret.className = 'map-select-caret';
      toggle.append(value, caret);
      const menu = document.createElement('span');
      menu.className = 'map-select-menu';
      menu.setAttribute('role', 'listbox');
      const items = document.createElement('span');
      items.className = 'map-select-menu-scroll';
      menu.append(items);
      let menuPortaled = false;
      const restoreMenu = () => {
        if (!menuPortaled) return;
        menu.classList.remove('map-select-menu-portal');
        menu.removeAttribute('style');
        picker.append(menu);
        menuPortaled = false;
      };
      const close = () => {
        picker.classList.remove('open');
        restoreMenu();
      };
      const portalMenu = () => {
        const dialog = picker.closest('.map-effect-dialog');
        if (!dialog) return;
        const pickerBox = picker.getBoundingClientRect();
        const dialogBox = dialog.getBoundingClientRect();
        dialog.append(menu);
        menu.classList.add('map-select-menu-portal');
        Object.assign(menu.style, {
          top: `${pickerBox.bottom - dialogBox.top + 2}px`,
          right: 'auto',
          left: `${pickerBox.left - dialogBox.left}px`,
          width: `${pickerBox.width}px`,
        });
        menuPortaled = true;
      };
      const refresh = () => {
        picker.hidden = select.hidden;
        const option = select.options[select.selectedIndex];
        value.textContent = option?.textContent || '';
        toggle.disabled = select.disabled;
        picker.classList.toggle('disabled', select.disabled);
        items.replaceChildren(...[...select.options].filter(optionItem => !optionItem.hidden).map(optionItem => {
          const item = document.createElement('button');
          item.type = 'button';
          item.className = 'map-select-option';
          item.textContent = optionItem.textContent;
          item.dataset.value = optionItem.value;
          item.classList.toggle('selected', optionItem.value === select.value);
          item.disabled = optionItem.disabled;
          item.addEventListener('click', event => {
            event.stopPropagation();
            select.value = optionItem.value;
            refresh();
            select.dispatchEvent(new Event('change', { bubbles: true }));
            close();
          });
          return item;
        }));
      };
      select._mapPickerRefresh = refresh;
      select.dataset.mapPicker = 'true';
      select.parentNode.insertBefore(picker, select);
      picker.append(select, toggle, menu);
      picker._mapPickerClose = close;
      toggle.addEventListener('click', event => {
        event.preventDefault();
        event.stopPropagation();
        if (select.disabled) return;
        if (picker.classList.contains('open')) {
          close();
          return;
        }
        closeMapSelectPickers(picker);
        refresh();
        picker.classList.add('open');
        portalMenu();
      });
      picker.closest('.map-effect-settings-content')?.addEventListener('scroll', close);
      refresh();
    });
  }

  function render() {
    recalculateNodeLevels();
    dom.mapName.value = currentMap().name;
    renderNodes();
    renderRoutes();
    renderInspector();
    enhanceMapSelects();
  }

  function renderNodes() {
    dom.nodeLayer.replaceChildren();
    currentMap().nodes.forEach(node => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = `map-node kind-${node.kind}`;
      button.dataset.id = node.id;
      button.style.left = `${node.position.x / WORLD_WIDTH * 100}%`;
      button.style.top = `${node.position.y / WORLD_HEIGHT * 100}%`;
      button.classList.toggle('selected', selection.type === 'node' && selection.id === node.id);
      button.classList.toggle('connect-source', connectionSourceId === node.id);
      button.classList.toggle('connect-candidate', interactionMode === 'connect' && connectionSourceId !== null);
      const marker = nodeMarker(node);
      button.innerHTML = `
        <span class="node-hit" aria-hidden="true"></span>
        <span class="node-visual" aria-hidden="true">
          <span class="point-marker ${marker.className}"></span>
          ${node.battle.roundabout ? '<span class="roundabout-mark"></span>' : ''}
        </span>
        <span class="node-name">${escapeHtml(node.name)}</span>
        <span class="node-meta">${LEVEL_NAMES[node.level] || '点位'}</span>
      `;
      button.addEventListener('pointerdown', event => startNodePointer(event, node.id));
      button.addEventListener('click', event => handleNodeClick(event, node.id));
      dom.nodeLayer.append(button);
    });
  }

  function nodeMarker(node) {
    return { className: `marker-${node.kind}` };
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  function startNodePointer(event, nodeId) {
    if (event.button !== 0 || interactionMode === 'connect') return;
    const node = getNode(nodeId);
    if (!node) return;
    event.stopPropagation();
    const start = { clientX: event.clientX, clientY: event.clientY, x: node.position.x, y: node.position.y };
    let moved = false;

    function onMove(moveEvent) {
      const dx = (moveEvent.clientX - start.clientX) * WORLD_WIDTH / dom.viewport.clientWidth;
      const dy = (moveEvent.clientY - start.clientY) * WORLD_HEIGHT / dom.viewport.clientHeight;
      if (Math.abs(dx) + Math.abs(dy) > 2) moved = true;
      node.position.x = clamp(start.x + dx, 18, WORLD_WIDTH - NODE_SIZE - 18);
      node.position.y = clamp(start.y + dy, 18, WORLD_HEIGHT - NODE_SIZE - 32);
      const element = dom.nodeLayer.querySelector(`[data-id="${cssEscape(nodeId)}"]`);
      if (element) {
        element.style.left = `${node.position.x / WORLD_WIDTH * 100}%`;
        element.style.top = `${node.position.y / WORLD_HEIGHT * 100}%`;
      }
      renderRoutes();
    }

    function onUp() {
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerup', onUp);
      suppressNodeClick = moved;
      if (moved) window.setTimeout(() => { suppressNodeClick = false; }, 0);
      selection = { type: 'node', id: nodeId };
      renderInspector();
      dom.nodeLayer.querySelectorAll('.map-node').forEach(item => {
        item.classList.toggle('selected', item.dataset.id === nodeId);
      });
    }

    window.addEventListener('pointermove', onMove);
    window.addEventListener('pointerup', onUp);
  }

  function handleNodeClick(event, nodeId) {
    event.stopPropagation();
    if (suppressNodeClick) return;
    if (interactionMode !== 'connect') {
      selection = { type: 'node', id: nodeId };
      render();
      return;
    }
    if (!connectionSourceId) {
      connectionSourceId = nodeId;
      setModeCopy('选择终点', `已选择“${getNode(nodeId).name}”，现在点击目标点位`);
      renderNodes();
      return;
    }
    if (connectionSourceId === nodeId) {
      showToast('起点和终点不能是同一个点位', true);
      return;
    }
    const duplicate = currentMap().routes.some(route => route.from === connectionSourceId && route.to === nodeId);
    if (duplicate) {
      showToast('这两个点位已经存在同方向路线', true);
      return;
    }
    const route = routeData(uid('route'), connectionSourceId, nodeId, 1);
    currentMap().routes.push(route);
    pushUndo({ type: 'add-route', routeId: route.id, from: route.from });
    selection = { type: 'route', id: route.id };
    exitConnectMode();
    render();
  }

  function cssEscape(value) {
    return window.CSS?.escape ? window.CSS.escape(value) : String(value).replace(/["\\]/g, '\\$&');
  }

  function renderRoutes() {
    dom.routeLayer.replaceChildren();
    dom.routeLabelLayer.replaceChildren();
    const outgoingRoutes = new Map();
    currentMap().routes.forEach(route => {
      const routes = outgoingRoutes.get(route.from) || [];
      routes.push(route);
      outgoingRoutes.set(route.from, routes);
    });

    currentMap().routes.forEach(route => {
      const source = getNode(route.from);
      const target = getNode(route.to);
      if (!source || !target) return;
      const geometry = routeGeometry(source, target);
      const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
      group.classList.add('route-group');
      group.classList.toggle('selected', selection.type === 'route' && selection.id === route.id);
      group.dataset.id = route.id;
      const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute('d', geometry.path);
      path.setAttribute('class', 'route-path');
      const hit = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      hit.setAttribute('d', geometry.path);
      hit.setAttribute('class', 'route-hit');
      hit.addEventListener('click', event => {
        event.stopPropagation();
        selectRoute(route.id);
      });
      group.append(path, hit);
      dom.routeLayer.append(group);

      const siblingRoutes = outgoingRoutes.get(route.from) || [];
      if (siblingRoutes.length < 2) return;
      const hasDifferentWeight = siblingRoutes.some(item => item.weight !== siblingRoutes[0].weight);
      const shouldShowWeight = hasDifferentWeight || siblingRoutes[0].weight !== 1;
      const conditions = route.conditions.length
        ? route.conditions.map(condition => `<span>${escapeHtml(conditionSummary(condition))}</span>`).join('')
        : '';
      if (!shouldShowWeight && !conditions) return;

      const label = document.createElement('button');
      label.type = 'button';
      label.className = 'route-label';
      label.classList.toggle('selected', selection.type === 'route' && selection.id === route.id);
      label.style.left = `${geometry.label.x / WORLD_WIDTH * 100}%`;
      label.style.top = `${geometry.label.y / WORLD_HEIGHT * 100}%`;
      const tooltipCondition = summarizeConditions(route);
      const titleParts = [`${source.name} → ${target.name}`];
      if (shouldShowWeight) titleParts.push(`权重 ${route.weight}`);
      if (tooltipCondition) titleParts.push(tooltipCondition);
      label.title = titleParts.join('；');
      const weight = shouldShowWeight
        ? `<span class="route-weight"><i>${'★'.repeat(clamp(Math.round(route.weight), 1, 3))}</i></span>`
        : '';
      label.innerHTML = `${weight}${conditions ? `<span class="route-conditions">${conditions}</span>` : ''}`;
      label.addEventListener('click', event => {
        event.stopPropagation();
        selectRoute(route.id);
      });
      dom.routeLabelLayer.append(label);
    });
  }

  function routeGeometry(source, target) {
    const sourceCenter = { x: source.position.x + NODE_SIZE / 2, y: source.position.y + NODE_SIZE / 2 };
    const targetCenter = { x: target.position.x + NODE_SIZE / 2, y: target.position.y + NODE_SIZE / 2 };
    const dx = targetCenter.x - sourceCenter.x;
    const dy = targetCenter.y - sourceCenter.y;
    const distance = Math.max(Math.hypot(dx, dy), 1);
    const offset = NODE_SIZE / 2 + 2;
    const start = { x: sourceCenter.x + dx / distance * offset, y: sourceCenter.y + dy / distance * offset };
    const end = { x: targetCenter.x - dx / distance * offset, y: targetCenter.y - dy / distance * offset };
    return {
      path: `M ${start.x} ${start.y} L ${end.x} ${end.y}`,
      label: { x: (start.x + end.x) / 2, y: (start.y + end.y) / 2 },
    };
  }

  function selectRoute(routeId) {
    selection = { type: 'route', id: routeId };
    render();
  }

  function summarizeConditions(route) {
    const joiner = route.relation === 'any' ? ' / ' : ' & ';
    return route.conditions.map(conditionSummary).join(joiner);
  }

  function conditionSummary(condition) {
    const operator = Object.fromEntries(NUMBER_OPERATORS)[condition.fun] || condition.fun;
    const shipTypeNames = Object.fromEntries(shipTypeOptions());
    if (condition.type === 'leader') {
      return `旗舰${condition.fun === 'not' ? '不是' : '是'}${shipTypeNames[condition.name] || condition.name}`;
    }
    if (condition.type === 'num') {
      const shipType = shipTypeNames[condition.name] || condition.name;
      return `${shipType}${operator}${condition.value}`;
    }
    const statusName = Object.fromEntries(STATUS_FIELDS)[condition.name] || condition.name;
    return `${statusName} ${operator} ${condition.value}`;
  }

  function renderInspector() {
    const node = selection.type === 'node' ? getNode(selection.id) : null;
    const route = selection.type === 'route' ? getRoute(selection.id) : null;
    dom.emptyInspector.hidden = Boolean(node || route);
    dom.nodeInspector.hidden = !node;
    dom.routeInspector.hidden = !route;
    if (node) renderNodeInspector(node);
    if (route) renderRouteInspector(route);
  }

  function renderNodeInspector(node) {
    document.querySelector('#node-name').value = node.name;
    const kindSelect = document.querySelector('#node-kind');
    kindSelect.value = node.kind;
    kindSelect.disabled = node.id === currentMap().entrance;
    const levelSelect = document.querySelector('#node-level');
    const autoOption = levelSelect.querySelector('option[value="auto"]');
    autoOption.textContent = `自动（${LEVEL_NAMES[node.level]}）`;
    levelSelect.value = node.level_auto !== false ? 'auto' : String(node.level);
    levelSelect.disabled = node.id === currentMap().entrance;
    const roundaboutInput = document.querySelector('#node-roundabout');
    roundaboutInput.checked = Boolean(node.battle.roundabout);
    roundaboutInput.disabled = !canRoundabout(node);
    const supportInput = document.querySelector('#node-support');
    supportInput.checked = Boolean(node.battle.support);
    supportInput.disabled = !isCombatNode(node);
    const resourceNode = isResourceNode(node);
    document.querySelector('#node-roundabout-label').textContent = resourceNode ? '资源种类' : '允许迂回';
    document.querySelector('#node-support-label').textContent = resourceNode ? '资源数量' : '支援攻击';
    const resourceType = document.querySelector('#node-resource-type');
    resourceType.value = RESOURCE_TYPES.has(node.battle.resource) ? node.battle.resource : 'oil';
    resourceType.hidden = !resourceNode;
    roundaboutInput.hidden = resourceNode;
    const resourceAmount = document.querySelector('#node-resource-amount');
    resourceAmount.value = String(Math.max(0, Math.trunc(Number(node.battle.amount) || 0)));
    resourceAmount.hidden = !resourceNode;
    supportInput.hidden = resourceNode;
    resourceType.closest('.map-compact-switch').classList.toggle('map-resource-field', resourceNode);
    resourceAmount.closest('.map-compact-switch').classList.toggle('map-resource-field', resourceNode);
    document.querySelector('#delete-node').disabled = node.id === currentMap().entrance;
    document.querySelector('#edit-node-effects').disabled = false;
    document.querySelector('#add-fleet').disabled = node.enemy_fleets.length >= 3 || !isCombatNode(node);
    renderFleets(node);
  }

  function updateMapEffectState() {
    const rows = [...dom.mapEffectList.querySelectorAll('.map-effect-row')];
    rows.forEach((row, index) => {
      row.querySelector('.environment-extra-index').textContent = index + 1;
    });
    if (!rows.length && dom.mapEffectEmpty.parentElement !== dom.mapEffectList) {
      dom.mapEffectList.append(dom.mapEffectEmpty);
    } else if (rows.length && dom.mapEffectEmpty.parentElement === dom.mapEffectList) {
      dom.mapEffectList.after(dom.mapEffectEmpty);
    }
    dom.mapEffectEmpty.hidden = rows.length > 0;
    document.querySelector('#add-map-effect').disabled = !mapEffectOptions?.length;
  }

  function renderMapEffectCatalog() {
    dom.mapEffectCatalogList.replaceChildren();
    (mapEffectOptions || []).forEach(effect => {
      const item = document.createElement('li');
      item.className = 'map-effect-catalog-item';
      const name = document.createElement('strong');
      name.textContent = effect.name;
      const description = document.createElement('p');
      description.textContent = effect.effect || '未提供效果说明';
      item.append(name, description);
      dom.mapEffectCatalogList.append(item);
    });
    if (!mapEffectOptions?.length) {
      const item = document.createElement('li');
      item.className = 'map-effect-catalog-empty';
      item.textContent = '暂无可用地图效果';
      dom.mapEffectCatalogList.append(item);
    }
    dom.mapEffectCatalog.hidden = !mapEffectCatalogOpen;
    dom.mapEffectCatalogToggle.setAttribute('aria-expanded', String(mapEffectCatalogOpen));
  }

  function toggleMapEffectCatalog() {
    mapEffectCatalogOpen = !mapEffectCatalogOpen;
    closeMapSelectPickers();
    renderMapEffectCatalog();
  }

  function addMapEffect(selected = '') {
    if (!mapEffectOptions?.length) return;
    const row = document.createElement('div');
    row.className = 'environment-extra-row map-effect-row';
    const index = document.createElement('span');
    index.className = 'environment-extra-index';
    const select = document.createElement('select');
    select.className = 'map-effect-select';
    select.setAttribute('aria-label', '地图效果');
    select.append(new Option('请选择地图效果', ''));
    mapEffectOptions.forEach(effect => {
      select.append(new Option(effect.name, effect.id));
    });
    if (selected && !mapEffectOptions.some(effect => effect.id === selected)) {
      select.append(new Option(`不可用效果：${selected}`, selected));
    }
    select.value = selected;
    const remove = document.createElement('button');
    remove.type = 'button';
    remove.className = 'environment-extra-remove';
    remove.setAttribute('aria-label', '删除地图效果');
    remove.textContent = '×';
    remove.addEventListener('click', () => {
      row.remove();
      updateMapEffectState();
    });
    row.append(index, select, remove);
    dom.mapEffectList.append(row);
    setupMapSearchablePicker(select);
    updateMapEffectState();
  }

  async function openMapEffectsDialog() {
    const node = selection.type === 'node' ? getNode(selection.id) : null;
    if (!node) return;
    const button = document.querySelector('#edit-node-effects');
    button.disabled = true;
    try {
      const response = await fetch('/api/map/effects');
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(payload.error || '无法读取地图效果');
      mapEffectOptions = Array.isArray(payload.effects) ? payload.effects : [];
      mapEffectNodeId = node.id;
      mapEffectCatalogOpen = false;
      dom.mapEffectPointName.textContent = `点位 ${node.name}`;
      dom.mapEffectList.replaceChildren();
      (node.map_effects || []).forEach(addMapEffect);
      updateMapEffectState();
      renderMapEffectCatalog();
      dom.mapEffectDialog.showModal();
    } catch (error) {
      showToast(error.message, true);
    } finally {
      button.disabled = false;
    }
  }

  function saveMapEffects() {
    const node = getNode(mapEffectNodeId);
    if (!node) {
      dom.mapEffectDialog.close('cancel');
      return;
    }
    const effectIds = [...dom.mapEffectList.querySelectorAll('.map-effect-select')]
      .map(select => select.value.trim())
      .filter(Boolean);
    if (new Set(effectIds).size !== effectIds.length) {
      showToast('同一节点不能重复添加地图效果', true);
      return;
    }
    node.map_effects = effectIds;
    closeMapSelectPickers();
    closeMapSearchablePickers();
    dom.mapEffectDialog.close('saved');
    showToast(`已保存 ${node.name} 的地图效果`);
  }

  function renderFleets(node) {
    dom.fleetList.replaceChildren();
    if (!node.enemy_fleets.length) {
      const empty = document.createElement('div');
      empty.className = 'condition-empty';
      empty.textContent = !isCombatNode(node)
        ? '无战斗点不配置敌方舰队'
        : '该点位尚未配置敌方舰队';
      dom.fleetList.append(empty);
      return;
    }
    node.enemy_fleets.forEach((fleet, fleetIndex) => {
      const card = document.querySelector('#map-fleet-template').content.firstElementChild.cloneNode(true);
      card.dataset.id = fleet.id;
      // Keep the fleet marker visual-only, matching the numbered ship slots.
      // Deletion remains available through the dedicated fleet action button.
      card.querySelector('.fleet-index').textContent = fleetIndex + 1;
      card.querySelector('.fleet-name-display').textContent = fleet.name;
      card.querySelector('.fleet-summary').textContent = fleetCompositionSummary(fleet);
      renderFleetStats(card.querySelector('.fleet-stats'), fleet);
      card.querySelector('.fleet-summary-open').addEventListener('click', () => openFleetEditor(node, fleet.id));
      card.querySelector('.remove-fleet').addEventListener('click', event => {
        event.stopPropagation();
        node.enemy_fleets.splice(fleetIndex, 1);
        renderNodes();
        renderNodeInspector(node);
      });
      const copyButton = card.querySelector('.copy-fleet');
      copyButton.disabled = node.enemy_fleets.length >= 3;
      copyButton.addEventListener('click', event => {
        event.stopPropagation();
        if (node.enemy_fleets.length >= 3) return;
        node.enemy_fleets.push(fleetData(
          uid('fleet'),
          `${fleet.name} 副本`,
          fleet.formation,
          fleet.ships.map(ship => ({ ...ship })),
        ));
        renderNodes();
        renderNodeInspector(node);
      });
      dom.fleetList.append(card);
    });
  }

  function fleetCompositionSummary(fleet) {
    const formation = FORMATIONS[fleet.formation] || '未知阵型';
    const labels = new Map(shipTypeOptions());
    const types = fleet.ships.map(ship => {
      const rawType = window.WSGRMapConfig?.getEnemyShipType(ship.cid) || '';
      const typeCode = String(rawType).match(/[A-Za-z]+/)?.[0] || '';
      return labels.get(typeCode) || typeCode || '待选择';
    });
    return formation + ' | ' + (types.length ? types.join(' ') : '未配置舰船');
  }

  function renderFleetStats(element, fleet) {
    const ships = fleet.ships.filter(ship => String(ship.cid || '').trim());
    element.textContent = '索敌 — | 制空 — | 航速 —';
    if (!ships.length) return;

    const requestFleet = {
      formation: fleet.formation,
      ships: ships.map(ship => ({ ...ship })),
    };
    const cacheKey = JSON.stringify(requestFleet);
    let request = fleetStatsCache.get(cacheKey);
    if (!request) {
      request = fetch('/api/map/fleet-summary', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fleet: requestFleet }),
      }).then(async response => {
        const payload = await response.json();
        if (!response.ok) throw new Error(payload.error || '无法计算敌方舰队概要');
        return payload;
      }).catch(error => {
        fleetStatsCache.delete(cacheKey);
        throw error;
      });
      fleetStatsCache.set(cacheKey, request);
    }
    request.then(summary => {
      if (!element.isConnected) return;
      const recon = Number(summary.recon || 0).toFixed(0);
      const aerial = Number(summary.aerial || 0).toFixed(2);
      const speed = Number(summary.speed || 0).toFixed(2);
      element.textContent = '索敌 ' + recon + ' | 制空 ' + aerial + ' | 航速 ' + speed;
    }).catch(() => {
      if (element.isConnected) element.textContent = '索敌 — | 制空 — | 航速 —';
    });
  }

  function openFleetEditor(node, fleetId) {
    const fleet = node.enemy_fleets.find(item => item.id === fleetId);
    if (!fleet || !window.WSGRMapFleetEditor) return;
    window.WSGRMapFleetEditor.open(fleet, {
      onChange(config) {
        fleet.name = config.name;
        fleet.formation = config.formation;
        fleet.ships = config.ships.map((ship, index) => ({ ...ship, loc: index + 1 }));
        renderNodes();
        renderFleets(node);
      },
      onDelete() {
        node.enemy_fleets = node.enemy_fleets.filter(item => item.id !== fleetId);
        renderNodes();
        renderNodeInspector(node);
      },
    });
  }

  function renderRouteInspector(route) {
    fillNodeSelect(document.querySelector('#route-from'), route.from);
    fillNodeSelect(document.querySelector('#route-to'), route.to);
    document.querySelector('#route-weight').value = String(route.weight);
    document.querySelector('#route-relation').value = route.relation;
    renderConditions(route);
  }

  function fillNodeSelect(select, selectedId) {
    select.replaceChildren();
    currentMap().nodes.forEach(node => {
      const option = document.createElement('option');
      option.value = node.id;
      option.textContent = `${node.name} · ${LEVEL_NAMES[node.level] || '点位'}`;
      option.selected = node.id === selectedId;
      select.append(option);
    });
  }

  function renderConditions(route) {
    dom.conditionList.replaceChildren();
    if (!route.conditions.length) {
      const empty = document.createElement('div');
      empty.className = 'condition-empty';
      empty.textContent = '暂未设置带路条件';
      dom.conditionList.append(empty);
      return;
    }
    route.conditions.forEach((condition, index) => {
      const card = document.querySelector('#map-condition-template').content.firstElementChild.cloneNode(true);
      const typeSelect = card.querySelector('.condition-type');
      typeSelect.value = condition.type;
      typeSelect.addEventListener('change', () => {
        condition.type = typeSelect.value;
        Object.assign(condition, defaultCondition(typeSelect.value));
        renderConditions(route);
        renderRoutes();
      });
      card.querySelector('.remove-condition').addEventListener('click', () => {
        route.conditions.splice(index, 1);
        renderConditions(route);
        renderRoutes();
      });
      renderConditionFields(card.querySelector('.condition-fields'), condition, route);
      dom.conditionList.append(card);
    });
    // Conditions can be added without a full map render. Enhance their
    // selects immediately so newly-created cards use the same picker as
    // cards restored after switching views.
    enhanceMapSelects();
  }

  function defaultCondition(type = 'num') {
    if (type === 'leader') return { type, name: 'BB', fun: 'is', value: '' };
    if (type === 'status') return { type, name: 'low_speed', fun: 'le', value: 27 };
    return { type: 'num', name: 'Ship', fun: 'ge', value: 1 };
  }

  function renderConditionFields(container, condition, route) {
    container.replaceChildren();
    if (condition.type === 'leader') {
      container.style.gridTemplateColumns = '1.25fr .75fr';
      const name = selectField('旗舰舰种', shipTypeOptions(), condition.name, true);
      const fun = selectField('判断', [['is', '是'], ['not', '不是']], condition.fun);
      bindConditionSelect(name.select, condition, 'name', route);
      bindConditionSelect(fun.select, condition, 'fun', route);
      container.append(name.label, fun.label);
      return;
    }
    container.style.gridTemplateColumns = 'minmax(0, 1.2fr) .8fr .8fr';
    const options = condition.type === 'status' ? STATUS_FIELDS : shipTypeOptions();
    const name = selectField(
      condition.type === 'status' ? '舰队属性' : '舰船数量',
      options,
      condition.name,
      true,
    );
    const fun = selectField('判断', NUMBER_OPERATORS, condition.fun);
    const valueLabel = document.createElement('label');
    valueLabel.innerHTML = '<span>阈值</span>';
    const value = document.createElement('input');
    value.type = 'text';
    value.inputMode = 'decimal';
    // Keep decimal values editable, but make arrow-key changes advance by 1.
    value.step = 'any';
    value.addEventListener('keydown', event => {
      if (event.key !== 'ArrowUp' && event.key !== 'ArrowDown') return;
      event.preventDefault();
      const current = Number(value.value);
      const next = (Number.isFinite(current) ? current : 0) + (event.key === 'ArrowUp' ? 1 : -1);
      value.value = String(next);
      value.dispatchEvent(new Event('input', { bubbles: true }));
    });
    value.value = condition.value;
    value.addEventListener('input', () => {
      const normalized = value.value.replace(/[。．]/g, '.');
      if (normalized !== value.value) value.value = normalized;
      condition.value = Number(normalized);
      renderRoutes();
    });
    valueLabel.append(value);
    bindConditionSelect(name.select, condition, 'name', route);
    bindConditionSelect(fun.select, condition, 'fun', route);
    container.append(name.label, fun.label, valueLabel);
  }

  function selectField(labelText, options, selected, searchable = false) {
    const label = document.createElement('label');
    const span = document.createElement('span');
    span.textContent = labelText;
    const select = document.createElement('select');
    options.forEach(([value, text]) => {
      const option = document.createElement('option');
      option.value = value;
      option.textContent = text;
      option.selected = value === selected;
      select.append(option);
    });
    label.append(span, select);
    if (searchable) setupMapSearchablePicker(select);
    return { label, select };
  }

  function bindConditionSelect(select, condition, key, route) {
    select.addEventListener('change', () => {
      condition[key] = select.value;
      renderRoutes();
    });
  }

  function nextNodeName() {
    const usedNames = new Set(
      currentMap().nodes
        .map(node => String(node.name || '').trim().toUpperCase())
        .filter(name => /^[A-Z]$/.test(name)),
    );
    for (let code = 65; code <= 90; code += 1) {
      const name = String.fromCharCode(code);
      if (!usedNames.has(name)) return name;
    }
    let suffix = 1;
    while (usedNames.has('A' + suffix)) suffix += 1;
    return 'A' + suffix;
  }

  function addNode() {
    const center = {
      x: WORLD_WIDTH / 2 - NODE_SIZE / 2,
      y: WORLD_HEIGHT / 2 - NODE_SIZE / 2,
    };
    const number = currentMap().nodes.length;
    const node = nodeData(
      uid('node'),
      nextNodeName(),
      'normal',
      clamp(center.x + number * 13, 18, WORLD_WIDTH - NODE_SIZE - 18),
      clamp(center.y + number * 13, 18, WORLD_HEIGHT - NODE_SIZE - 32),
      [],
    );
    currentMap().nodes.push(node);
    pushUndo({ type: 'add-node', nodeId: node.id });
    selection = { type: 'node', id: node.id };
    render();
  }

  function enterConnectMode() {
    interactionMode = 'connect';
    connectionSourceId = null;
    document.querySelector('#connect-nodes').classList.add('active');
    setModeCopy('连接点位', '先点击路线起点，再点击路线终点；按 Esc 退出');
    renderNodes();
  }

  function exitConnectMode() {
    interactionMode = 'select';
    connectionSourceId = null;
    document.querySelector('#connect-nodes').classList.remove('active');
    setModeCopy('选择与拖动', '拖动点位调整布局；点击点位或路线进行编辑');
    renderNodes();
  }

  function setModeCopy(title, hint) {
    dom.modeTitle.textContent = title;
    dom.modeHint.textContent = hint;
  }

  function deleteSelectedNode() {
    const node = selection.type === 'node' ? getNode(selection.id) : null;
    if (!node || node.id === currentMap().entrance) {
      showToast('入口节点不能删除', true);
      return;
    }
    const nodeIndex = currentMap().nodes.indexOf(node);
    const connectedRoutes = currentMap().routes
      .map((route, index) => ({ route, index }))
      .filter(item => item.route.from === node.id || item.route.to === node.id);
    pushUndo({
      type: 'delete-node',
      node: cloneMapData(node),
      index: nodeIndex,
      routes: cloneMapData(connectedRoutes),
    });
    currentMap().nodes = currentMap().nodes.filter(item => item.id !== node.id);
    currentMap().routes = currentMap().routes.filter(route => route.from !== node.id && route.to !== node.id);
    selection = { type: 'node', id: currentMap().entrance };
    render();
  }

  function deleteSelectedRoute() {
    const route = selection.type === 'route' ? getRoute(selection.id) : null;
    if (!route) return;
    pushUndo({
      type: 'delete-route',
      route: cloneMapData(route),
      index: currentMap().routes.indexOf(route),
    });
    currentMap().routes = currentMap().routes.filter(item => item.id !== route.id);
    selection = { type: 'node', id: route.from };
    render();
  }

  function addFleet() {
    const node = selection.type === 'node' ? getNode(selection.id) : null;
    if (!node || !isCombatNode(node) || node.enemy_fleets.length >= 3) return;
    const fleet = fleetData(
      uid('fleet'),
      `敌方编队 ${node.enemy_fleets.length + 1}`,
      1,
      [],
    );
    node.enemy_fleets.push(fleet);
    renderNodes();
    renderNodeInspector(node);
  }

  function addCondition() {
    const route = selection.type === 'route' ? getRoute(selection.id) : null;
    if (!route) return;
    route.conditions.push(defaultCondition('num'));
    renderConditions(route);
    renderRoutes();
  }

  function changeRouteEndpoint(key, nodeId) {
    const route = selection.type === 'route' ? getRoute(selection.id) : null;
    if (!route) return;
    const otherKey = key === 'from' ? 'to' : 'from';
    if (route[otherKey] === nodeId) {
      showToast('路线起点和终点不能相同', true);
      renderRouteInspector(route);
      return;
    }
    const duplicate = currentMap().routes.some(item => (
      item.id !== route.id
      && item.from === (key === 'from' ? nodeId : route.from)
      && item.to === (key === 'to' ? nodeId : route.to)
    ));
    if (duplicate) {
      showToast('相同方向的路线已经存在', true);
      renderRouteInspector(route);
      return;
    }
    route[key] = nodeId;
    render();
  }

  function applyMapDocument(document) {
    mapDocument = normalizeDocument(document);
    mapUserRules = createDefaultUserRules();
    clearUndoHistory();
    selection = { type: 'node', id: currentMap().entrance };
    exitConnectMode();
    render();
  }

  async function saveMapDocument() {
    try {
      const map = serializeDocument(normalizeDocument(serializeDocument(mapDocument)));
      const response = await fetch('/api/map/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ map }),
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(payload.error || '保存地图失败');
      showToast(`地图已保存为 ${payload.filename}`);
    } catch (error) {
      showToast(error.message, true);
    }
  }

  async function importYamlFile(file) {
    if (!file) return;
    try {
      const response = await fetch('/api/map/import', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: await file.text() }),
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(payload.error || '地图 YAML 解析失败');
      applyMapDocument(payload.map);
      showToast(`已导入 ${currentMap().nodes.length} 个点位和 ${currentMap().routes.length} 条路线`);
    } catch (error) {
      showToast(`导入失败：${error.message}`, true);
    }
  }

  function buildMapConfig(document = mapDocument) {
    const friendFleet = window.WSGRMapConfig?.getFriendFleet();
    if (!friendFleet || !friendFleet.ships.length) throw new Error('我方舰队不能为空');
    normalizeMapUserRules();
    return {
      battle_type: 'Map',
      friend_fleet: friendFleet,
      map: { mapid: String(document.map.mapid || '').trim() },
      user_rules: cloneMapData(mapUserRules),
    };
  }

  function normalizeDocument(input) {
    if (!input || typeof input !== 'object' || Array.isArray(input)) throw new Error('YAML 顶层必须是对象');
    if (!Array.isArray(input.nodes) || !input.nodes.length) throw new Error('nodes 必须至少包含一个点位');
    if (!Array.isArray(input.routes)) throw new Error('routes 必须是数组');
    const rawBuffs = input.buffs == null ? {} : input.buffs;
    if (typeof rawBuffs !== 'object' || Array.isArray(rawBuffs)) {
      throw new Error('buffs 必须是以点位名称为键的对象');
    }
    const names = new Set();
    let entrance = '';
    const nodes = input.nodes.map((rawNode, index) => {
      if (!rawNode || typeof rawNode !== 'object') throw new Error(`第 ${index + 1} 个点位无效`);
      const id = `node-${index + 1}`;
      const name = String(rawNode.name || '').trim();
      if (!name) throw new Error(`第 ${index + 1} 个点位缺少 name`);
      if (names.has(name)) throw new Error(`点位名称重复：${name}`);
      names.add(name);
      const fleets = Array.isArray(rawNode.enemy_fleets) ? rawNode.enemy_fleets : [];
      if (fleets.length > 3) throw new Error(`点位 ${name} 的敌方舰队超过 3 个`);
      const kind = String(rawNode.kind || '');
      if (kind !== 'entrance' && !NODE_KINDS.includes(kind)) {
        throw new Error('点位类型必须是 entrance、no_battle、resource_gain、resource_loss、normal、air、night、elite 或 boss');
      }
      if (kind === 'entrance') {
        if (entrance) throw new Error('地图只能包含一个入口点');
        entrance = id;
      }
      const battleType = battleTypeForKind(kind);
      const resourceNode = kind === 'resource_gain' || kind === 'resource_loss';
      const resource = String(rawNode.battle?.resource ?? 'oil');
      if (resourceNode && !RESOURCE_TYPES.has(resource)) {
        throw new Error(`点位 ${name} 的资源种类无效`);
      }
      const resourceAmount = Math.max(0, Math.trunc(Number(rawNode.battle?.amount) || 0));
      const rawEffects = rawBuffs[name] == null ? [] : rawBuffs[name];
      const mapEffects = typeof rawEffects === 'string' ? [rawEffects] : rawEffects;
      if (!Array.isArray(mapEffects) || !mapEffects.every(value => typeof value === 'string' && value.trim())) {
        throw new Error(`点位 ${name} 的 buffs 必须是效果标识列表`);
      }
      if (new Set(mapEffects).size !== mapEffects.length) {
        throw new Error(`点位 ${name} 的 buffs 不能重复`);
      }
      return {
        id,
        name,
        kind,
        level: kind === 'entrance' ? 0 : clamp(Math.trunc(Number(rawNode.level) || 2), 0, 5),
        level_auto: kind === 'entrance' || rawNode.level_auto !== false,
        position: {
          x: clamp(Number(rawNode.position?.x) || 0, 0, WORLD_WIDTH - NODE_SIZE),
          y: clamp(Number(rawNode.position?.y) || 0, 0, WORLD_HEIGHT - NODE_SIZE),
        },
        battle: {
          type: battleType,
          roundabout: !NON_COMBAT_BATTLE_TYPES.has(battleType) && kind !== 'boss' && Boolean(rawNode.battle?.roundabout),
          support: !NON_COMBAT_BATTLE_TYPES.has(battleType) && Boolean(rawNode.battle?.support),
          resource: resourceNode ? resource : undefined,
          amount: resourceNode ? resourceAmount : undefined,
        },
        enemy_fleets: (NON_COMBAT_BATTLE_TYPES.has(battleType) ? [] : fleets).map((rawFleet, fleetIndex) => {
          const ships = Array.isArray(rawFleet?.ships) ? rawFleet.ships : [];
          if (ships.length > 6) throw new Error(`点位 ${name} 的舰队 ${fleetIndex + 1} 超过 6 艘舰船`);
          return {
            id: `${id}-fleet-${fleetIndex + 1}`,
            name: String(rawFleet?.name || `敌方编队 ${fleetIndex + 1}`),
            formation: clamp(Math.trunc(Number(rawFleet?.formation) || 1), 1, 5),
            ships: ships.map((rawShip, shipIndex) => ({
              loc: shipIndex + 1,
              cid: String(rawShip?.cid ?? ''),
              name: String(rawShip?.name || ''),
              level: Math.max(1, Math.trunc(Number(rawShip?.level) || 1)),
              affection: clamp(Math.trunc(Number(rawShip?.affection) || 50), 0, 200),
              skill: Number(rawShip?.skill) === 0 ? 0 : 1,
            })),
          };
        }),
        map_effects: mapEffects.map(value => value.trim()),
      };
    });
    if (!entrance) throw new Error('地图必须包含一个 kind 为 entrance 的入口点');
    const unknownBuffNodes = Object.keys(rawBuffs).filter(name => !names.has(name));
    if (unknownBuffNodes.length) throw new Error(`buffs 引用了不存在的点位：${unknownBuffNodes.join('、')}`);
    const nodeIdByName = new Map(nodes.map(node => [node.name, node.id]));
    const routes = input.routes.map((rawRoute, index) => {
      const id = `route-${index + 1}`;
      const fromName = String(rawRoute?.from || '').trim();
      const toName = String(rawRoute?.to || '').trim();
      const from = nodeIdByName.get(fromName);
      const to = nodeIdByName.get(toName);
      if (!from || !to) throw new Error(`路线 ${index + 1} 引用了不存在的点位名称`);
      if (from === to) throw new Error(`路线 ${index + 1} 的起点和终点相同`);
      const conditions = Array.isArray(rawRoute?.conditions) ? rawRoute.conditions : [];
      return {
        id,
        from,
        to,
        weight: clamp(Math.round(Number(rawRoute?.weight) || 1), 1, 3),
        relation: rawRoute?.relation === 'any' || rawRoute?.relation === 'or' ? 'any' : 'all',
        conditions: conditions.map(raw => {
          const type = ['num', 'leader', 'status'].includes(raw?.type) ? raw.type : 'num';
          const defaults = defaultCondition(type);
          const name = String(raw?.name ?? defaults.name);
          if (type === 'num' && name === 'ANY') {
            throw new Error('任意舰船请使用 Ship，不再支持 ANY');
          }
          return {
            type,
            name,
            fun: String(raw?.fun ?? defaults.fun),
            value: type === 'leader' ? '' : Number(raw?.value ?? defaults.value),
          };
        }),
      };
    });
    const pairs = new Set();
    routes.forEach(route => {
      const pair = `${route.from}\u0000${route.to}`;
      if (pairs.has(pair)) throw new Error('存在重复的同向路线');
      pairs.add(pair);
    });
    const name = String(input.name || '未命名海图').trim();
    const mapid = name;
    if (!mapid || mapid === '.' || mapid === '..' || /[<>:"/\\|?*\u0000-\u001F]/.test(mapid) || /[. ]$/.test(mapid)) {
      throw new Error('mapid 不能为空，且不能包含路径或文件名保留字符');
    }
    const map = {
      mapid,
      name,
      entrance,
      canvas: { width: WORLD_WIDTH, height: WORLD_HEIGHT },
      nodes,
      routes,
    };
    recalculateNodeLevels(map);
    return { map };
  }

  function serializeDocument(document) {
    const map = document.map;
    const nodeNameById = new Map(map.nodes.map(node => [node.id, node.name]));
    const buffs = Object.fromEntries(map.nodes
      .filter(node => Array.isArray(node.map_effects) && node.map_effects.length)
      .map(node => [node.name, [...node.map_effects]]));
    return {
      mapid: String(map.name || '未命名海图').trim(),
      name: String(map.name || '未命名海图'),
      nodes: map.nodes.map(node => ({
        name: node.name,
        kind: node.kind,
        level: node.level,
        level_auto: node.level_auto !== false,
        position: { x: node.position.x, y: node.position.y },
        battle: {
          type: battleTypeForKind(node.kind),
          roundabout: canRoundabout(node) && Boolean(node.battle.roundabout),
          support: isCombatNode(node) && Boolean(node.battle.support),
          ...(isResourceNode(node) ? {
            resource: RESOURCE_TYPES.has(node.battle.resource) ? node.battle.resource : 'oil',
            amount: Math.max(0, Math.trunc(Number(node.battle.amount) || 0)),
          } : {}),
        },
        enemy_fleets: node.enemy_fleets.map(fleet => ({
          name: fleet.name,
          formation: fleet.formation,
          ships: fleet.ships.map(ship => ({
            loc: ship.loc,
            cid: ship.cid,
            name: ship.name,
            level: ship.level,
            affection: ship.affection ?? 50,
            skill: ship.skill ?? 1,
          })),
        })),
      })),
      routes: map.routes.map(route => ({
        from: nodeNameById.get(route.from),
        to: nodeNameById.get(route.to),
        weight: route.weight,
        relation: route.relation,
        conditions: route.conditions.map(condition => ({ ...condition })),
      })),
      ...(Object.keys(buffs).length ? { buffs } : {}),
    };
  }

  function clamp(value, minimum, maximum) {
    return Math.min(maximum, Math.max(minimum, value));
  }

  function renderStrategyProceedStops(values) {
    dom.strategyProceedStop.replaceChildren(...values.map((value, index) => {
      const label = document.createElement('label');
      label.textContent = `${index + 1}号位`;
      const select = document.createElement('select');
      select.dataset.strategyProceedStop = String(index);
      select.append(
        new Option('中破回港', '1'),
        new Option('大破回港', '2'),
        new Option('忽略', '-1'),
      );
      select.value = String(value);
      label.append(select);
      return label;
    }));
  }

  function renderStrategyNodePicker() {
    const selected = new Set(Array.isArray(mapUserRules.selected_nodes)
      ? mapUserRules.selected_nodes : []);
    const allNodes = mapUserRules.selected_nodes === 'all';
    dom.strategyNodePicker.replaceChildren(...strategyNodeNames().map(name => {
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = name;
      button.classList.toggle('selected', selected.has(name));
      button.addEventListener('click', () => {
        if (selected.has(name)) selected.delete(name);
        else selected.add(name);
        mapUserRules.selected_nodes = [...selected];
        renderStrategyNodePicker();
      });
      return button;
    }));
    dom.strategyNodePicker.setAttribute('aria-disabled', String(allNodes));
  }

  function renderStrategyScopes(selectedScope = dom.strategyScope.value || '__default__') {
    const scopes = strategyNodeNames();
    dom.strategyScope.replaceChildren(
      new Option('所有点位的默认策略', '__default__'),
      ...scopes.map(name => new Option(`${name} 点覆盖策略`, name)),
    );
    dom.strategyScope.value = scopes.includes(selectedScope) || selectedScope === '__default__'
      ? selectedScope : '__default__';
  }

  function updateStrategyRoundField() {
    const thresholdActive = dom.strategyRound.value === 'threshold';
    dom.strategyRoundThresholdField.hidden = !thresholdActive;
    dom.strategyRound.closest('.strategy-dropdown-grid')?.classList.toggle(
      'threshold-active',
      thresholdActive,
    );
  }

  function writeStrategyForm(scope = dom.strategyScope.value) {
    activeStrategyScope = scope;
    const settings = strategySettingsFor(scope);
    dom.strategyFormation.value = String(settings.formation);
    dom.strategyFormationRecon.value = String(settings.formation_if_recon_fails);
    dom.strategyLongMissile.checked = Boolean(settings.long_missile);
    dom.strategyNight.value = String(settings.night);
    if (typeof settings.round === 'number') {
      dom.strategyRound.value = 'threshold';
      dom.strategyRoundThreshold.value = String(settings.round);
    } else {
      dom.strategyRound.value = String(settings.round);
    }
    updateStrategyRoundField();
    dom.strategyRetreatRecon.checked = Boolean(settings.retreat_if_recon_fails);
    dom.strategyRetreatRound.checked = Boolean(settings.retreat_if_round_fails);
    dom.strategyProceed.checked = Boolean(settings.proceed);
    renderStrategyProceedStops(settings.proceed_stop);
    dom.strategyRules.value = formatStrategyRules(settings.rules);
    if (dom.strategyDialog.open) enhanceMapSelects(dom.strategyDialog);
  }

  function saveStrategyDraft() {
    const settings = readStrategyForm();
    if (activeStrategyScope === '__default__') {
      if (isSameStrategyValue(settings, mapUserRules.node_defaults)) {
        strategyDrafts.delete(activeStrategyScope);
      } else {
        strategyDrafts.set(activeStrategyScope, settings);
      }
      return;
    }
    const defaults = strategyDrafts.get('__default__') || mapUserRules.node_defaults;
    const overrides = Object.fromEntries(Object.entries(settings).filter(
      ([key, value]) => !isSameStrategyValue(value, defaults[key]),
    ));
    if (isSameStrategyValue(overrides, mapUserRules.node_args[activeStrategyScope] || {})) {
      strategyDrafts.delete(activeStrategyScope);
    } else {
      strategyDrafts.set(activeStrategyScope, overrides);
    }
  }

  function readStrategyForm() {
    const round = dom.strategyRound.value === 'threshold'
      ? clamp(Math.round(Number(dom.strategyRoundThreshold.value) || 0), 0, 100)
      : dom.strategyRound.value === 'true';
    const proceedStop = [...dom.strategyProceedStop.querySelectorAll('select')]
      .map(select => Number(select.value));
    return {
      formation: Number(dom.strategyFormation.value),
      formation_if_recon_fails: dom.strategyFormationRecon.value === 'false'
        ? false : Number(dom.strategyFormationRecon.value),
      long_missile: dom.strategyLongMissile.checked,
      night: dom.strategyNight.value === 'flag_alive'
        ? 'flag_alive' : dom.strategyNight.value === 'true',
      round,
      rules: parseStrategyRules(dom.strategyRules.value),
      retreat_if_recon_fails: dom.strategyRetreatRecon.checked,
      retreat_if_round_fails: dom.strategyRetreatRound.checked,
      proceed: dom.strategyProceed.checked,
      proceed_stop: proceedStop,
    };
  }

  function isSameStrategyValue(left, right) {
    return JSON.stringify(left) === JSON.stringify(right);
  }

  function openStrategyDialog() {
    normalizeMapUserRules();
    strategyDrafts.clear();
    activeStrategyScope = '__default__';
    dom.strategyAllNodes.checked = mapUserRules.selected_nodes === 'all';
    renderStrategyNodePicker();
    renderStrategyScopes(activeStrategyScope);
    writeStrategyForm(activeStrategyScope);
    enhanceMapSelects(dom.strategyDialog);
    dom.strategyDialog.showModal();
  }

  function saveStrategyDialog(event) {
    event.preventDefault();
    try {
      saveStrategyDraft();
      const defaultSettings = strategyDrafts.get('__default__');
      if (defaultSettings) mapUserRules.node_defaults = defaultSettings;
      [...strategyDrafts.entries()].filter(([scope]) => scope !== '__default__').forEach(([scope, overrides]) => {
        if (Object.keys(overrides).length) mapUserRules.node_args[scope] = overrides;
        else delete mapUserRules.node_args[scope];
      });
      if (dom.strategyAllNodes.checked) {
        mapUserRules.selected_nodes = 'all';
      } else if (!Array.isArray(mapUserRules.selected_nodes) || !mapUserRules.selected_nodes.length) {
        throw new Error('请至少选择一个要打的节点，或启用“全部点位”');
      }
      dom.strategyDialog.close();
      showToast('地图决策策略已应用');
    } catch (error) {
      showToast(error.message, true);
    }
  }

  function cancelStrategyDialog() {
    dom.strategyDialog.close('cancel');
    showToast('已取消地图决策设置，未应用修改');
  }

  function bindStaticEvents() {
    document.addEventListener('click', event => {
      if (!event.target.closest('.map-select-picker')) closeMapSelectPickers();
      if (!event.target.closest('.map-damage-picker')) {
        mapDamagePickerOpen = false;
        document.querySelectorAll('.map-damage-picker.open').forEach(picker => {
          picker.classList.remove('open');
        });
      }
    });
    dom.mapName.addEventListener('input', () => {
      currentMap().name = dom.mapName.value;
      currentMap().mapid = dom.mapName.value;
    });
    document.querySelector('#open-map-strategy').addEventListener('click', openStrategyDialog);
    document.querySelector('#close-map-strategy').addEventListener('click', cancelStrategyDialog);
    document.querySelector('#cancel-map-strategy').addEventListener('click', cancelStrategyDialog);
    dom.strategyDialog.addEventListener('cancel', event => {
      event.preventDefault();
      cancelStrategyDialog();
    });
    dom.strategyAllNodes.addEventListener('change', () => {
      if (dom.strategyAllNodes.checked) mapUserRules.selected_nodes = 'all';
      else mapUserRules.selected_nodes = strategyNodeNames();
      renderStrategyNodePicker();
    });
    dom.strategyScope.addEventListener('change', () => {
      try {
        saveStrategyDraft();
        writeStrategyForm(dom.strategyScope.value);
      } catch (error) {
        dom.strategyScope.value = activeStrategyScope;
        dom.strategyScope._mapPickerRefresh?.();
        showToast(error.message, true);
      }
    });
    dom.strategyRound.addEventListener('change', updateStrategyRoundField);
    dom.strategyForm.addEventListener('submit', saveStrategyDialog);
    const mapEpochRange = document.querySelector('#map-epoch-range');
    const mapEpochValue = document.querySelector('#map-epoch-value');
    const mapRunButton = document.querySelector('#run-map');
    let mapSimulationState = 'idle';
    let mapSimulationPollTimer = null;
    let mapStatusAbortController = null;
    let mapSimulationToggleInFlight = false;
    let mapSimulationDisplayFrozen = false;
    let latestMapSummary = null;
    let mapHistoryRecorded = false;
    let mapDamageFilter = 'all';
    let mapDamagePickerOpen = false;
    const mapSimulationIcon = (icon, retry = false) => retry
      ? '<svg class="retry-svg" viewBox="0 0 24 24" aria-hidden="true"><path d="M3.2 8.5V2.8m0 5.7h5.7M4.4 7.1a8.5 8.5 0 1 1-.6 8.8"/></svg>'
      : icon === 'loading'
        ? '<svg class="running-svg" viewBox="0 0 24 24" aria-hidden="true"><g><line x1="12" y1="2.8" x2="12" y2="6.8" opacity="1"/><line x1="18.5" y1="5.5" x2="15.7" y2="8.3" opacity=".86"/><line x1="21.2" y1="12" x2="17.2" y2="12" opacity=".72"/><line x1="18.5" y1="18.5" x2="15.7" y2="15.7" opacity=".58"/><line x1="12" y1="21.2" x2="12" y2="17.2" opacity=".44"/><line x1="5.5" y1="18.5" x2="8.3" y2="15.7" opacity=".3"/><line x1="2.8" y1="12" x2="6.8" y2="12" opacity=".2"/><line x1="5.5" y1="5.5" x2="8.3" y2="8.3" opacity=".12"/></g></svg>'
        : '<svg class="play-svg" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4v16l12-8z"/></svg>';
    const recordMapHistory = state => {
      if (mapHistoryRecorded || !state?.summary) return;
      if (!['complete', 'stopped'].includes(state.state)) return;
      const hasBossResult = (state.summary.boss_statistics || [])
        .some(boss => Number(boss.simulations || 0) > 0);
      if (!hasBossResult) return;
      window.dispatchEvent(new CustomEvent('wsgr:map-history', {
        detail: {
          mapName: currentMap().name || '未命名海图',
          summary: state.summary,
        },
      }));
      mapHistoryRecorded = true;
    };
    const setMapSimulationButton = (icon, label, retry = false) => {
      const iconClass = retry ? ' retry-icon' : icon === 'loading' ? ' running-icon' : ' play-icon';
      mapRunButton.innerHTML = `<span class="simulation-content"><span class="simulation-icon${iconClass}">${mapSimulationIcon(icon, retry)}</span><span>${label}</span></span><span class="stop-content" aria-hidden="true"><span class="simulation-icon stop-icon"><svg class="stop-svg" viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="6" width="12" height="12" rx="1"/></svg></span><span>停止模拟</span></span>`;
    };
    const mapApi = async (path, options = {}) => {
      const response = await fetch(path, {
        headers: { 'Content-Type': 'application/json' },
        ...options,
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || `请求失败（${response.status}）`);
      return payload;
    };
    const csvCell = value => `"${String(value ?? '').replaceAll('"', '""')}"`;
    const downloadMapReport = summary => {
      const resultFlags = ['SS', 'S', 'A', 'B', 'C', 'D'];
      const friendShipNames = Array.from(
        { length: 6 },
        (_, index) => summary.friend_ship_names?.[index] || `舰船${index + 1}`,
      );
      const resourceEntries = [
        ['燃油', 'oil', 1], ['弹药', 'ammo', 1], ['钢材', 'steel', 1],
        ['铝材', 'almn', 1], ['桶耗', 'repeat', 2], ['损管', 'dcitem', 2],
      ];
      const rate = value => `${Number(value || 0).toFixed(2)}%`;
      const optionalRate = value => value == null ? '—' : rate(value);
      const bosses = (summary.boss_statistics || [])
        .filter(entry => Number(entry.simulations || 0) > 0);
      const overallRows = [
        ['名称', currentMap().name || '未命名海图', ...bosses.map(entry => entry.name)],
        ['模拟次数', Number(summary.simulation_count || 0), ...bosses.map(entry => Number(entry.simulations || 0))],
        ['通关率', rate(summary.clear_rate), ...bosses.map(entry => optionalRate(entry.clear_rate))],
        ['Boss旗舰击沉率', rate(summary.boss_flagship_sink_rate), ...bosses.map(entry => optionalRate(entry.flagship_sink_rate))],
        ['资源消耗', Number(summary.resource_total || 0).toFixed(1), ...bosses.map(entry => Number(entry.resource_total || 0).toFixed(1))],
        ...resourceEntries.map(([label, key, digits]) => [
          label,
          Number(summary.supply?.[key] || 0).toFixed(digits),
          ...bosses.map(entry => Number(entry.supply?.[key] || 0).toFixed(digits)),
        ]),
      ];
      const rows = [
        ...overallRows,
        [],
        ['点位战果统计'],
        [
          '点位', '场次', '索敌率', '迂回率', ...resultFlags.map(flag => `${flag}概率`), '全体中破率', '全体大破率',
          ...friendShipNames.flatMap(name => [`${name}中破率`, `${name}大破率`]),
        ],
        ...(summary.node_statistics || [])
          .filter(entry => Number(entry.visits || 0) > 0)
          .map(entry => [
            entry.name,
            Number(entry.visits || 0),
            optionalRate(entry.recon_rate),
            optionalRate(entry.roundabout_rate),
            ...resultFlags.map(flag => optionalRate(entry.result_rates?.[flag])),
            optionalRate(entry.mid_damage_rate),
            optionalRate(entry.heavy_damage_rate),
            ...friendShipNames.flatMap((_, index) => {
              const hasShip = Boolean(summary.friend_ship_names?.[index]);
              return [
                hasShip ? optionalRate(entry.mid_damage_ship_rates?.[index]) : '—',
                hasShip ? optionalRate(entry.heavy_damage_ship_rates?.[index]) : '—',
              ];
            }),
          ]),
      ];
      const content = `\ufeff${rows.map(row => row.map(csvCell).join(',')).join('\n')}\n`;
      const filename = `${String(currentMap().name || '未命名海图').replace(/[\\/:*?"<>|]/g, '_')}_地图模拟战报.csv`;
      const link = document.createElement('a');
      link.href = URL.createObjectURL(new Blob([content], { type: 'text/csv;charset=utf-8' }));
      link.download = filename;
      link.click();
      window.setTimeout(() => URL.revokeObjectURL(link.href), 1000);
    };
    document.querySelector('#export-map-report').addEventListener('click', () => {
      if (!latestMapSummary) {
        showToast('请先完成至少一次地图模拟', true);
        return;
      }
      downloadMapReport(latestMapSummary);
    });
    const createMapDamagePicker = (friendShipNames, selectedValue, onChange) => {
      const picker = document.createElement('span');
      picker.className = 'editor-select-picker map-damage-picker';
      const select = document.createElement('select');
      select.setAttribute('aria-label', '中破和大破率筛选');
      select.append(new Option('全体', 'all'));
      friendShipNames.forEach((name, index) => select.append(new Option(name, String(index))));
      select.value = selectedValue;
      const toggle = document.createElement('button');
      toggle.type = 'button';
      toggle.className = 'editor-select-toggle';
      const value = document.createElement('span');
      toggle.append(value);
      const menu = document.createElement('span');
      menu.className = 'picker-menu';
      menu.setAttribute('role', 'listbox');
      const items = document.createElement('span');
      items.className = 'picker-menu-scroll';
      menu.append(items);
      const refresh = () => {
        value.textContent = select.selectedOptions[0]?.textContent || '';
        items.replaceChildren(...[...select.options].map(option => {
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
      toggle.addEventListener('pointerdown', event => {
        if (!event.isPrimary || (event.pointerType === 'mouse' && event.button !== 0)) return;
        event.preventDefault();
        event.stopPropagation();
        const opening = !picker.classList.contains('open');
        document.querySelectorAll('.map-damage-picker.open').forEach(item => {
          if (item !== picker) item.classList.remove('open');
        });
        refresh();
        picker.classList.toggle('open', opening);
        mapDamagePickerOpen = opening;
      });
      menu.addEventListener('pointerdown', event => {
        if (!event.isPrimary || (event.pointerType === 'mouse' && event.button !== 0)) return;
        const option = event.target.closest('button[data-value]');
        if (!option) return;
        event.preventDefault();
        event.stopPropagation();
        select.value = option.dataset.value;
        refresh();
        picker.classList.remove('open');
        mapDamagePickerOpen = false;
        onChange(select.value);
      });
      picker.append(select, toggle, menu);
      refresh();
      return picker;
    };
    const renderMapNodeStatistics = (container, entries, friendShipNames) => {
      const flags = ['SS', 'S', 'A', 'B', 'C', 'D'];
      const table = document.createElement('table');
      table.className = 'map-node-result-table';
      const header = document.createElement('thead');
      const filterIndex = Number(mapDamageFilter);
      if (mapDamageFilter !== 'all' && (!Number.isInteger(filterIndex) || !friendShipNames[filterIndex])) {
        mapDamageFilter = 'all';
      }
      header.innerHTML = `<tr><th rowspan="2">点位</th><th rowspan="2">场次</th><th rowspan="2">索敌率</th><th rowspan="2">迂回率</th>${flags.map(flag => `<th rowspan="2">${flag}</th>`).join('')}<th colspan="2" class="map-damage-filter-cell"><label>受损筛选 <span class="map-damage-picker-slot"></span></label></th></tr><tr><th>中破</th><th>大破</th></tr>`;
      header.querySelector('.map-damage-picker-slot').append(createMapDamagePicker(
        friendShipNames,
        mapDamageFilter,
        value => {
          mapDamageFilter = value;
          if (latestMapSummary) renderMapNodeStatistics(
            container,
            latestMapSummary.node_statistics || [],
            latestMapSummary.friend_ship_names || [],
          );
        },
      ));
      const body = document.createElement('tbody');
      // 场次表示实际到达并完成点位准备流程的次数；成功迂回不会产生
      // 战斗结果，但仍应计入场次与迂回率。
      entries.filter(entry => Number(entry.visits || 0) > 0).forEach(entry => {
        const visits = Number(entry.visits || 0);
        const rate = value => `${Number(value || 0).toFixed(2)}%`;
        const optionalRate = value => value == null ? '—' : rate(value);
        const midDamageRate = mapDamageFilter === 'all'
          ? entry.mid_damage_rate : entry.mid_damage_ship_rates?.[Number(mapDamageFilter)];
        const heavyDamageRate = mapDamageFilter === 'all'
          ? entry.heavy_damage_rate : entry.heavy_damage_ship_rates?.[Number(mapDamageFilter)];
        const row = document.createElement('tr');
        row.innerHTML = `<th>${escapeHtml(entry.name)}</th><td>${visits}</td><td>${optionalRate(entry.recon_rate)}</td><td>${optionalRate(entry.roundabout_rate)}</td>${flags.map(flag => `<td>${optionalRate(entry.result_rates?.[flag])}</td>`).join('')}<td>${optionalRate(midDamageRate)}</td><td>${optionalRate(heavyDamageRate)}</td>`;
        body.append(row);
      });
      table.append(header, body);
      container.replaceChildren(table);
    };
    const renderMapResourceStatistics = (container, summary) => {
      const entries = [
        ['燃油', 'oil', 1], ['弹药', 'ammo', 1], ['钢材', 'steel', 1],
        ['铝材', 'almn', 1], ['桶耗', 'repeat', 2], ['损管', 'dcitem', 2],
      ];
      const rows = [
        ['总体', summary.supply || {}],
        ...(summary.boss_statistics || [])
          .filter(entry => Number(entry.simulations || 0) > 0)
          .map(entry => [entry.name, entry.supply || {}]),
      ];
      const table = document.createElement('table');
      table.className = 'map-resource-result-table';
      table.innerHTML = `<thead><tr><th>名称</th>${entries.map(([label]) => `<th>${label}</th>`).join('')}</tr></thead><tbody>${rows.map(([name, supply]) => `<tr><th>${escapeHtml(name)}</th>${entries.map(([, key, digits]) => `<td>${Number(supply?.[key] || 0).toFixed(digits)}</td>`).join('')}</tr>`).join('')}</tbody>`;
      container.replaceChildren(table);
    };
    const renderMapSummary = summary => {
      if (!summary) return;
      latestMapSummary = summary;
      document.querySelector('#map-clear-rate').innerHTML = `${Number(summary.clear_rate || 0).toFixed(2)}<em>%</em>`;
      document.querySelector('#map-boss-sink-rate').innerHTML = `${Number(summary.boss_flagship_sink_rate || 0).toFixed(2)}<em>%</em>`;
      document.querySelector('#map-resource-total').textContent = Number(summary.resource_total || 0).toFixed(1);
      document.querySelector('#map-simulation-count').textContent = Number(summary.simulation_count || 0).toLocaleString('zh-CN');
      if (!mapDamagePickerOpen) {
        renderMapNodeStatistics(
          document.querySelector('#map-node-results'),
          summary.node_statistics || [],
          summary.friend_ship_names || [],
        );
      }
      renderMapResourceStatistics(document.querySelector('#map-resource-results'), summary);
      document.querySelector('#map-battle-detail').textContent = summary.battle_detail || '等待首场模拟完成…';
      document.querySelector('#map-result-breakdown').hidden = false;
      document.querySelector('#map-result-placeholder').hidden = true;
    };
    const resetMapResultDisplay = () => {
      document.querySelector('#map-clear-rate').innerHTML = '—<em>%</em>';
      document.querySelector('#map-boss-sink-rate').innerHTML = '—<em>%</em>';
      document.querySelector('#map-resource-total').textContent = '—';
      document.querySelector('#map-simulation-count').textContent = '—';
      document.querySelector('#map-node-results').replaceChildren();
      document.querySelector('#map-resource-results').replaceChildren();
      document.querySelector('#map-battle-detail').textContent = '';
      latestMapSummary = null;
      mapDamageFilter = 'all';
      mapDamagePickerOpen = false;
      document.querySelector('#map-result-breakdown').hidden = true;
      document.querySelector('#map-result-placeholder').hidden = false;
      mapRunButton.classList.remove('running', 'stopping');
      mapRunButton.style.removeProperty('--run-progress');
      setMapSimulationButton('play', '开始模拟');
    };
    const renderMapSimulationState = state => {
      recordMapHistory(state);
      if (mapSimulationDisplayFrozen) return;
      mapSimulationState = state.state;
      const completed = Number(state.live_completed ?? state.completed ?? 0);
      const target = Number(state.target || 0);
      const progress = Number(state.live_progress ?? state.progress ?? 0);
      renderMapSummary(state.summary);
      if (state.state === 'running' || state.state === 'stopping') {
        mapRunButton.classList.add('running');
        mapRunButton.classList.toggle('stopping', state.state === 'stopping');
        mapRunButton.style.setProperty('--run-progress', `${progress}%`);
        setMapSimulationButton(
          'loading',
          state.state === 'stopping'
            ? `正在停止模拟… ${completed} 次`
            : `正在模拟… ${completed} / ${target}`,
        );
        return;
      }
      mapRunButton.classList.remove('running', 'stopping');
      mapRunButton.style.removeProperty('--run-progress');
      if (state.state === 'idle') setMapSimulationButton('play', '开始模拟');
      else setMapSimulationButton('retry', '再次模拟', true);
      if (state.state === 'error') showToast(state.message || '地图模拟失败', true);
    };
    const pollMapSimulation = async () => {
      window.clearTimeout(mapSimulationPollTimer);
      mapStatusAbortController?.abort();
      const controller = new AbortController();
      mapStatusAbortController = controller;
      try {
        const state = await mapApi('/api/map-simulation/status', { signal: controller.signal });
        renderMapSimulationState(state);
        if (!mapSimulationDisplayFrozen && (state.state === 'running' || state.state === 'stopping')) {
          mapSimulationPollTimer = window.setTimeout(pollMapSimulation, 30);
        }
      } catch (error) {
        if (!mapSimulationDisplayFrozen && error.name !== 'AbortError') showToast(error.message, true);
      } finally {
        if (mapStatusAbortController === controller) mapStatusAbortController = null;
      }
    };
    const startMapSimulation = async () => {
      mapSimulationDisplayFrozen = false;
      mapHistoryRecorded = false;
      switchMapView('result');
      const epoch = Math.max(1, Number(mapEpochValue.value) || 1);
      renderMapSimulationState({
        state: 'running',
        live_completed: 0,
        live_progress: 0,
        target: epoch,
      });
      try {
        const validated = normalizeDocument(serializeDocument(mapDocument));
        const state = await mapApi('/api/map-simulation/start', {
          method: 'POST',
          body: JSON.stringify({
            config: buildMapConfig(validated),
            map: serializeDocument(validated),
            epoch,
          }),
        });
        renderMapSimulationState(state);
        mapSimulationPollTimer = window.setTimeout(pollMapSimulation, 30);
      } catch (error) {
        renderMapSimulationState({ state: 'error', message: error.message });
      }
    };
    const freezeMapSimulationDisplay = () => {
      if (mapSimulationDisplayFrozen || mapSimulationState !== 'running') return;
      mapSimulationDisplayFrozen = true;
      window.clearTimeout(mapSimulationPollTimer);
      mapStatusAbortController?.abort();
      mapRunButton.classList.remove('running', 'stopping');
      mapRunButton.style.removeProperty('--run-progress');
      setMapSimulationButton('retry', '再次模拟', true);
    };
    const resetMapSimulation = async () => {
      mapSimulationDisplayFrozen = true;
      window.clearTimeout(mapSimulationPollTimer);
      mapStatusAbortController?.abort();
      try {
        await mapApi('/api/map-simulation/reset', { method: 'POST', body: '{}' });
      } catch (error) {
        showToast(error.message, true);
      }
      mapSimulationState = 'idle';
      mapSimulationDisplayFrozen = false;
      resetMapResultDisplay();
    };
    const clearMapWorkspace = async () => {
      await resetMapSimulation();
      mapDocument = createDefaultDocument();
      mapUserRules = createDefaultUserRules();
      clearUndoHistory();
      selection = { type: 'node', id: currentMap().entrance };
      exitConnectMode();
      switchMapView('editor');
      render();
    };
    const stopMapSimulation = async () => {
      if (mapSimulationState !== 'running') return;
      mapSimulationState = 'stopping';
      try {
        const state = await mapApi('/api/map-simulation/stop', {
          method: 'POST',
          body: '{}',
        });
        mapSimulationState = state.state;
        recordMapHistory({ ...state, state: 'stopped' });
      } catch (error) {
        mapSimulationState = 'stopped';
        throw error;
      }
    };
    const updateMapEpoch = (value, manual = false) => {
      const minimum = manual ? 1 : Number(mapEpochRange.min);
      const epoch = Math.max(minimum, Math.min(1000000, Number(value) || minimum));
      mapEpochValue.value = epoch;
      if (manual) mapEpochRange.value = Math.max(Number(mapEpochRange.min), Math.min(epoch, Number(mapEpochRange.max)));
    };
    mapEpochRange.addEventListener('input', () => updateMapEpoch(mapEpochRange.value));
    mapEpochValue.addEventListener('input', () => updateMapEpoch(mapEpochValue.value, true));
    mapEpochValue.addEventListener('click', () => mapEpochValue.select());
    mapEpochValue.addEventListener('keydown', event => {
      if (event.key !== 'ArrowUp' && event.key !== 'ArrowDown') return;
      event.preventDefault();
      const current = Math.max(1, Number(mapEpochValue.value) || 1);
      const next = event.key === 'ArrowUp'
        ? (current < 1000 ? 1000 : Math.min(1000000, current + 1000))
        : (current <= 1000 ? 1 : Math.max(1, current - 1000));
      updateMapEpoch(next, true);
    });
    document.querySelector('#add-node').addEventListener('click', addNode);
    document.querySelector('#connect-nodes').addEventListener('click', () => {
      if (interactionMode === 'connect') exitConnectMode();
      else enterConnectMode();
    });
    dom.undoButton.addEventListener('click', undoLastMapEdit);
    dom.viewport.addEventListener('click', event => {
      if (event.target.closest('.map-node, .route-label, .route-hit')) return;
      selection = { type: null, id: null };
      render();
    });

    document.querySelector('#node-name').addEventListener('input', event => updateSelectedNode('name', event.target.value));
    document.querySelector('#node-level').addEventListener('change', event => {
      const node = getNode(selection.id);
      if (!node || node.id === currentMap().entrance) return;
      if (event.target.value === 'auto') {
        node.level_auto = true;
      } else {
        node.level_auto = false;
        node.level = clamp(Number(event.target.value), 0, 5);
      }
      render();
    });
    document.querySelector('#node-kind').addEventListener('change', event => {
      const node = getNode(selection.id);
      if (!node || node.id === currentMap().entrance) return;
      node.kind = NODE_KINDS.includes(event.target.value) ? event.target.value : 'normal';
      node.battle.type = battleTypeForKind(node.kind);
      if (!isCombatNode(node)) {
        node.enemy_fleets = [];
        node.battle.roundabout = false;
        node.battle.support = false;
      }
      if (isResourceNode(node)) {
        node.battle.resource = RESOURCE_TYPES.has(node.battle.resource) ? node.battle.resource : 'oil';
        node.battle.amount = Math.max(0, Math.trunc(Number(node.battle.amount) || 0));
      } else {
        delete node.battle.resource;
        delete node.battle.amount;
      }
      if (node.kind === 'boss') node.battle.roundabout = false;
      render();
    });
    document.querySelector('#node-roundabout').addEventListener('change', event => {
      const node = getNode(selection.id);
      if (node) {
        node.battle.roundabout = canRoundabout(node) && event.target.checked;
        renderNodes();
      }
    });
    document.querySelector('#node-support').addEventListener('change', event => {
      const node = getNode(selection.id);
      if (node && isCombatNode(node)) node.battle.support = event.target.checked;
    });
    document.querySelector('#node-resource-type').addEventListener('change', event => {
      const node = getNode(selection.id);
      if (node && isResourceNode(node) && RESOURCE_TYPES.has(event.target.value)) {
        node.battle.resource = event.target.value;
      }
    });
    document.querySelector('#node-resource-amount').addEventListener('input', event => {
      const node = getNode(selection.id);
      if (node && isResourceNode(node)) {
        node.battle.amount = Math.max(0, Math.trunc(Number(event.target.value) || 0));
      }
    });
    document.querySelector('#delete-node').addEventListener('click', deleteSelectedNode);
    document.querySelector('#edit-node-effects').addEventListener('click', () => { void openMapEffectsDialog(); });
    dom.mapEffectCatalogToggle.addEventListener('click', toggleMapEffectCatalog);
    document.querySelector('#add-fleet').addEventListener('click', addFleet);
    document.querySelector('#add-map-effect').addEventListener('click', () => addMapEffect());
    document.querySelector('#save-map-effects').addEventListener('click', saveMapEffects);
    document.querySelectorAll('[data-close-map-effects]').forEach(button => {
      button.addEventListener('click', () => {
        closeMapSelectPickers();
        closeMapSearchablePickers();
        dom.mapEffectDialog.close('cancel');
      });
    });

    document.querySelector('#route-from').addEventListener('change', event => changeRouteEndpoint('from', event.target.value));
    document.querySelector('#route-to').addEventListener('change', event => changeRouteEndpoint('to', event.target.value));
    document.querySelector('#route-weight').addEventListener('input', event => {
      const route = getRoute(selection.id);
      if (route) {
        route.weight = clamp(Math.round(Number(event.target.value) || 1), 1, 3);
        event.target.value = String(route.weight);
        renderRoutes();
      }
    });
    document.querySelector('#route-relation').addEventListener('change', event => {
      const route = getRoute(selection.id);
      if (route) {
        route.relation = event.target.value;
        renderRoutes();
      }
    });
    document.querySelector('#delete-route').addEventListener('click', deleteSelectedRoute);
    document.querySelector('#add-condition').addEventListener('click', addCondition);

    document.querySelector('#import-map').addEventListener('click', () => dom.yamlFile.click());
    dom.yamlFile.addEventListener('change', () => {
      void importYamlFile(dom.yamlFile.files[0]);
      dom.yamlFile.value = '';
    });
    document.querySelector('#export-map').addEventListener('click', saveMapDocument);
    document.querySelector('#reset-map').addEventListener('click', () => dom.confirmDialog.showModal());
    document.querySelector('#map-confirm-action').addEventListener('click', () => { void clearMapWorkspace(); });
    dom.mapViewButtons.forEach(button => {
      button.addEventListener('click', () => switchMapView(button.dataset.mapView));
    });
    mapRunButton.addEventListener('pointerdown', event => {
      if (!event.isPrimary || (event.pointerType === 'mouse' && event.button !== 0)) return;
      freezeMapSimulationDisplay();
    });
    mapRunButton.addEventListener('click', event => {
      event.preventDefault();
      if (mapSimulationToggleInFlight || mapSimulationState === 'stopping') return;
      mapSimulationToggleInFlight = true;
      const operation = mapSimulationState === 'running'
        ? stopMapSimulation()
        : startMapSimulation();
      void operation
        .catch(error => showToast(error.message, true))
        .finally(() => { mapSimulationToggleInFlight = false; });
    });
    void resetMapSimulation();

    window.addEventListener('keydown', event => {
      const editing = /^(INPUT|SELECT|TEXTAREA)$/.test(document.activeElement?.tagName);
      if (event.key === 'Escape' && interactionMode === 'connect') {
        exitConnectMode();
        return;
      }
      if ((event.key === 'Delete' || event.key === 'Backspace') && !editing) {
        if (selection.type === 'node') deleteSelectedNode();
        if (selection.type === 'route') deleteSelectedRoute();
      }
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'z' && !editing) {
        event.preventDefault();
        undoLastMapEdit();
      }
    });
  }

  function updateSelectedNode(key, value) {
    const node = selection.type === 'node' ? getNode(selection.id) : null;
    if (!node) return;
    node[key] = value;
    renderNodes();
    if (key === 'name') renderRoutes();
  }

  window.addEventListener('wsgr:bootstrap', event => {
    const labels = event.detail?.ship_labels;
    if (!labels || typeof labels !== 'object' || Array.isArray(labels)) return;
    const options = Object.entries(labels);
    if (!options.length) return;
    shipTypes = options;
    render();
  });

  window.WSGRMapEditor = {
    getDocument() {
      return serializeDocument(mapDocument);
    },
    loadDocument(document) {
      applyMapDocument(document);
    },
    getUserRules() {
      normalizeMapUserRules();
      return cloneMapData(mapUserRules);
    },
    loadUserRules(userRules) {
      loadMapUserRules(userRules);
    },
  };

  bindStaticEvents();
  updateUndoButton();
  switchMapView(activeMapView);
  render();
}());
