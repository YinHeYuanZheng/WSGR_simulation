# -*- coding:utf-8 -*-
# Author:银河远征(AI supported)
# env:py38

"""将装备数据库“特效配置”单元格转换为 EquipSkill 类。

配置语法速查：
    hit_rate:0.1                       普通词条，使用默认阶段
    hit_rate:0.1,AirPhase              普通词条，覆盖生效阶段
    entry1;entry2                      同一层级的多个配置项
    {crit:0.1;hit_rate:0.05}           合并为一个技能的最终词条组
    Cid(533,{crit:0.1;hit_rate:0.05})  包装并合并最终词条组
    Country(C,ShipType(CLT,{...}))     包装器嵌套，不使用大括号
    pierce_coef:0.05,stack             覆盖特殊不叠加规则
    pierce_coef:0.05,stack,ShellingPhase
    @013:0.1                           定向调用现有 Python 装备技能

解析器只负责有限的声明式语法，不执行单元格中的任意 Python 表达式。
无法通过注册词条和包装器表达的技能应继续使用 @esid 定向。
"""

from dataclasses import dataclass
import importlib
import json
import re
from typing import Any, Optional, Union

import src.wsgr.phase as rphase
import src.wsgr.ship as rship
from src.wsgr.skill import EquipEffect, EquipSkill, SelfTarget, Target


# 普通词条注册表。phase 和 bias_or_weight 对应现有 Buff 接口；
# effect_type=3/4 沿用 Ship.add_buff 中“同类取最高值”的特殊规则。
EFFECT_REGISTRY = {
    'pierce_coef': {'phase': 'AllPhase', 'bias_or_weight': 0, 'effect_type': 3},
    'uplimit_buff': {'phase': 'ShellingPhase', 'bias_or_weight': 0, 'effect_type': 4},
    'hit_rate': {'phase': 'AllPhase', 'bias_or_weight': 0},
    'miss_rate': {'phase': 'AllPhase', 'bias_or_weight': 0},
    'crit': {'phase': 'AllPhase', 'bias_or_weight': 0},
    'power_buff': {'phase': 'AllPhase', 'bias_or_weight': 2},
    'final_damage_buff': {'phase': 'AllPhase', 'bias_or_weight': 2},
    'air_ctrl_buff': {'phase': 'AirPhase', 'bias_or_weight': 0},
    'air_atk_buff': {'phase': 'AirPhase', 'bias_or_weight': 2},
    'air_bomb_atk_buff': {'phase': 'AirPhase', 'bias_or_weight': 2},
    'air_dive_atk_buff': {'phase': 'AirPhase', 'bias_or_weight': 2},
}

# 条件和目标包装器会递归向内部叶子词条传递状态。
WRAPPER_NAMES = {'Cid', 'Country', 'Tag', 'ShipType', 'Side'}

# 匹配 PascalCase(...) 包装器、捕获包装器内容、匹配 Python 定向。
WRAPPER_EXPR_RE = re.compile(r'[A-Z][A-Za-z0-9_]*\(.*\)')
WRAPPER_RE = re.compile(r'([A-Z][A-Za-z0-9_]*)\((.*)\)')
PYTHON_ENTRY_RE = re.compile(r'@(?:esid)?(\d+)(?::(.*))?')


@dataclass(frozen=True)
class Condition:
    """包装器添加的一个装备技能生效条件。"""

    name: str
    value: Any


@dataclass(frozen=True)
class ParseContext:
    """递归解析包装器时向内部传递的条件和目标。"""

    conditions: tuple[Condition, ...] = ()
    side: Optional[int] = None

    def with_condition(self, name: str, value: Any):
        return ParseContext(
            conditions=self.conditions + (Condition(name, value),),
            side=self.side,
        )

    def with_side(self, side: int):
        return ParseContext(conditions=self.conditions, side=side)


@dataclass(frozen=True)
class EffectEntry:
    """一个可直接构造 EquipEffect 的普通词条。"""

    name: str
    value: float
    phase: Optional[str]
    conditions: tuple[Condition, ...] = ()
    side: Optional[int] = None
    stackable: bool = False


@dataclass(frozen=True)
class PythonEntry:
    """一个定向调用现有 esid 模块的配置项。"""

    esid: str
    values: tuple[Any, ...] = ()
    conditions: tuple[Condition, ...] = ()
    side: Optional[int] = None


@dataclass(frozen=True)
class GroupEntry:
    """合并进同一个 EquipSkill 的最终普通词条组。"""

    entries: tuple[EffectEntry, ...]


ParsedEntry = Union[EffectEntry, PythonEntry, GroupEntry]


class EquipConfigError(ValueError):
    """带装备编号和原始配置文本的装备特效配置错误。"""


class ConfigEffectType(int):
    """可比较的动态特效编号，调试输出格式为 ``eid.词条序号``。

    Ship.add_buff 需要将 effect_type 与数字 2/3/4 比较，因此这里继承
    int 保持现有判定兼容；数据库装备加载时同时保存 eid 作为可读标签。
    """

    def __new__(cls, eid, index):
        eid_text = str(eid)
        eid_value = int(eid_text) if eid_text.isdigit() else 0
        value = 100000000 + eid_value * 1000 + index
        instance = int.__new__(cls, value)
        instance.eid = eid_text
        instance.index = index
        return instance

    def __repr__(self):
        return f'{self.eid}.{self.index:03d}'

    __str__ = __repr__


# Parser

def _split_top_level(text, delimiter):
    """仅在最外层切分文本，忽略括号、大括号、数组和引号内的分隔符。"""
    result = []
    start = 0
    stack = []
    quote = None
    escaped = False
    pairs = {')': '(', '}': '{', ']': '['}

    for index, char in enumerate(text):
        if quote is not None:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == quote:
                quote = None
            continue

        if char in '"\'':
            quote = char
        elif char in '({[':
            stack.append(char)
        elif char in ')}]':
            if not stack or stack.pop() != pairs[char]:
                raise ValueError(f'装备特效配置括号不匹配: {text}')
        elif char == delimiter and not stack:
            result.append(text[start:index].strip())
            start = index + 1

    if quote is not None or stack:
        raise ValueError(f'装备特效配置括号或引号不完整: {text}')
    result.append(text[start:].strip())
    return [item for item in result if item]


def _parse_value(text):
    """解析 JSON 标量或数组；未加引号的接口名称保留为字符串。"""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _normalize_cid(value):
    """将三位友方 Cid 展开为未改造和改造编号，五位 Cid 直接使用。"""
    values = value if isinstance(value, list) else [value]
    values = [str(item).zfill(3) for item in values]
    lengths = {len(item) for item in values}

    if len(lengths) != 1:
        raise ValueError('Cid 包装器不能混用三位和五位编号')
    if lengths == {3}:
        if not all(item.isdigit() for item in values):
            raise ValueError('三位 Cid 必须为数字')
        return [cid for item in values for cid in (f'10{item}', f'11{item}')]
    if lengths == {5}:
        if not all(item.isdigit() and item[0] in ['0', '1'] for item in values):
            raise ValueError('五位 Cid 必须以 0 或 1 开头')
        return values
    raise ValueError('Cid 包装器只接受三位或五位编号')


def _is_group(entry):
    return entry.startswith('{') and entry.endswith('}')


def _parse_entries(
    text: str,
    context: Optional[ParseContext] = None,
) -> list[ParsedEntry]:
    """按分号拆分同层级配置，并将每项分发给对应解析函数。"""
    context = ParseContext() if context is None else context
    entries = []
    for raw_entry in _split_top_level(text, ';'):
        entries.extend(_parse_single_entry(raw_entry, context))
    return entries


def _parse_single_entry(
    raw_entry: str,
    context: ParseContext,
) -> list[ParsedEntry]:
    """根据配置项外形分流到组、包装器、Python 定向或普通词条。"""
    if _is_group(raw_entry):
        return _parse_group(raw_entry[1:-1], context, require_multiple=True)

    wrapper = WRAPPER_RE.fullmatch(raw_entry)
    if wrapper:
        return _parse_wrapper(wrapper, context)

    if raw_entry.startswith('@'):
        return [_parse_python_entry(raw_entry, context)]

    return [_parse_effect_entry(raw_entry, context)]


def _parse_group(
    text: str,
    context: ParseContext,
    require_multiple: bool,
) -> list[ParsedEntry]:
    """解析大括号内容，并在最终普通词条达到两个时合并为 GroupEntry。"""
    raw_entries = _split_top_level(text, ';')
    if require_multiple and len(raw_entries) < 2:
        raise ValueError('顶层大括号必须包裹两个或更多普通词条')

    parsed = _parse_entries(text, context)
    has_wrapper = any(WRAPPER_EXPR_RE.fullmatch(entry) for entry in raw_entries)
    has_non_wrapper = any(
        not WRAPPER_EXPR_RE.fullmatch(entry) for entry in raw_entries
    )
    if has_wrapper and has_non_wrapper:
        raise ValueError('大括号不可同时包裹普通词条和包装器')
    if has_wrapper:
        return parsed

    if all(isinstance(entry, EffectEntry) for entry in parsed):
        if len(parsed) >= 2:
            return [GroupEntry(tuple(parsed))]
        return parsed

    if len(parsed) == 1 and isinstance(parsed[0], PythonEntry):
        return parsed

    if any(isinstance(entry, (EffectEntry, PythonEntry)) for entry in parsed):
        raise ValueError('合并技能的大括号只能包裹普通词条')
    return parsed


def _parse_wrapper(match: re.Match, context: ParseContext) -> list[ParsedEntry]:
    """解析一个包装器，并使用更新后的 ParseContext 递归解析内部配置。"""
    name, content = match.groups()
    if name not in WRAPPER_NAMES:
        raise ValueError(f'未知装备特效包装器: {name}')

    args = _split_top_level(content, ',')
    if len(args) != 2:
        raise ValueError(f'{name} 包装器必须填写条件和被包装内容两个参数')

    value = _parse_value(args[0])
    wrapped = args[1]
    if name == 'Side':
        if value not in [0, 1]:
            raise ValueError('Side 只能填写 0 或 1')
        next_context = context.with_side(value)
    else:
        value = _normalize_cid(value) if name == 'Cid' else value
        next_context = context.with_condition(name, value)

    return _parse_wrapped_content(name, wrapped, next_context)


def _parse_wrapped_content(
    wrapper_name: str,
    wrapped: str,
    context: ParseContext,
) -> list[ParsedEntry]:
    """解析包装器内部；普通词条必须有大括号，嵌套包装器则直接填写。"""
    if _is_group(wrapped):
        return _parse_group(wrapped[1:-1], context, require_multiple=False)
    if WRAPPER_EXPR_RE.fullmatch(wrapped):
        return _parse_entries(wrapped, context)
    raise ValueError(
        f'{wrapper_name} 包裹普通词条时必须使用大括号，'
        '包裹包装器时直接填写包装器'
    )


def _parse_python_entry(raw_entry: str, context: ParseContext) -> PythonEntry:
    """解析 @013、@esid013、@013:0.1 或 @013:0.1,0.2。"""
    match = PYTHON_ENTRY_RE.fullmatch(raw_entry)
    if match is None:
        raise ValueError(f'Python 装备特效定向格式错误: {raw_entry}')

    values = ()
    if match.group(2):
        values = tuple(
            _parse_value(value)
            for value in _split_top_level(match.group(2), ',')
        )
    return PythonEntry(
        esid=match.group(1).zfill(3),
        values=values,
        conditions=context.conditions,
        side=context.side,
    )


def _parse_effect_entry(raw_entry: str, context: ParseContext) -> EffectEntry:
    """解析一个普通词条及其数值、stack 和阶段参数。"""
    parts = _split_top_level(raw_entry, ':')
    if len(parts) != 2:
        raise ValueError(f'普通装备特效格式错误: {raw_entry}')

    name = parts[0]
    if name not in EFFECT_REGISTRY:
        raise ValueError(f'未知装备特效词条: {name}')

    value, stackable, phase = _parse_effect_options(
        name, _split_top_level(parts[1], ',')
    )
    return EffectEntry(
        name=name,
        value=value,
        phase=phase,
        conditions=context.conditions,
        side=context.side,
        stackable=stackable,
    )


def _parse_effect_options(name, args):
    """解析普通词条的数值、可选 stack 和可选阶段。"""
    if not 1 <= len(args) <= 3:
        raise ValueError(f'{name} 最多只能填写数值、stack和阶段三个参数')

    value = float(_parse_value(args[0]))
    stackable = False
    phase = None

    if len(args) == 2:
        if args[1] == 'stack':
            stackable = True
        else:
            phase = args[1]
    elif len(args) == 3:
        if args[1] != 'stack':
            raise ValueError(f'{name} 的第二个参数必须为 stack')
        stackable = True
        phase = args[2]

    return value, stackable, phase


def parse_equip_config(config: str) -> list[ParsedEntry]:
    """公开解析入口：将单元格配置解析为带类型的配置项。"""
    if not isinstance(config, str) or not config.strip():
        return []
    return _parse_entries(config.strip())


# Validator

def _phase(name):
    """将配置中的现有 Phase 类名转换为对应类。"""
    try:
        return getattr(rphase, name)
    except AttributeError as exc:
        raise ValueError(f'未知装备特效阶段: {name}') from exc


def _validate_ship_type(value):
    values = value if isinstance(value, list) else [value]
    try:
        for item in values:
            getattr(rship, item)
    except AttributeError as exc:
        raise ValueError(f'未知舰种: {value}') from exc


def _validate_entry(entry: ParsedEntry):
    """提前检查原本会延迟到技能实例化阶段才发现的配置错误。"""
    if isinstance(entry, GroupEntry):
        for child in entry.entries:
            _validate_entry(child)
        return
    if not isinstance(entry, EffectEntry):
        return

    registry = EFFECT_REGISTRY[entry.name]
    _phase(entry.phase or registry['phase'])
    for condition in entry.conditions:
        if condition.name == 'ShipType':
            _validate_ship_type(condition.value)


# Builder

def _match_condition(master, condition):
    """判断装备携带者是否满足一个条件包装器。"""
    values = (
        condition.value
        if isinstance(condition.value, list)
        else [condition.value]
    )
    if condition.name == 'Cid':
        return master.cid in values
    if condition.name == 'Country':
        return master.status['country'] in values
    if condition.name == 'Tag':
        return master.status['tag'] in values
    if condition.name == 'ShipType':
        _validate_ship_type(condition.value)
        return isinstance(master, tuple(getattr(rship, item) for item in values))
    raise ValueError(f'未知装备特效条件: {condition.name}')


def _conditions_active(master, conditions):
    return all(_match_condition(master, condition) for condition in conditions)


def _target(master, side):
    """未指定 Side 时作用于装备者；指定后作用于对应舰队全体。"""
    return SelfTarget(master) if side is None else Target(side=side)


def _build_effect(timer, entry, effect_type):
    """根据一个普通叶子词条创建 EquipEffect。"""
    registry = EFFECT_REGISTRY[entry.name]
    # 穿甲和攻击上限默认使用固定编号取最高值；stack 改用动态编号。
    effect_type = (
        effect_type if entry.stackable
        else registry.get('effect_type', effect_type)
    )
    return EquipEffect(
        timer=timer,
        effect_type=effect_type,
        name=entry.name,
        phase=_phase(entry.phase or registry['phase']),
        value=entry.value,
        bias_or_weight=registry['bias_or_weight'],
    )


def _build_equip_skill(entries, effect_types):
    """根据一组最终普通词条动态创建一个 EquipSkill 子类。"""
    first_entry = entries[0]

    class ConfigEquipSkill(EquipSkill):
        def __init__(self, timer, master, value):
            super().__init__(timer, master, value)
            self.target = _target(master, first_entry.side)
            self.buff = []
            if _conditions_active(master, first_entry.conditions):
                self.buff.extend(
                    _build_effect(timer, entry, effect_type)
                    for entry, effect_type in zip(entries, effect_types)
                )

    effect_label = '_'.join(str(effect_type) for effect_type in effect_types)
    ConfigEquipSkill.__name__ = f'ConfigEquipSkill_{effect_label}'
    return ConfigEquipSkill


def _build_python_skill(entry, eid, config):
    """包装现有 esid 技能，使配置参数、条件和目标仍可作用于它。"""
    module = importlib.import_module(f'src.skillCode.Equipment.esid{entry.esid}')
    result = []

    for base_skill in module.skill:
        class ConfigPythonSkill(base_skill):
            def __init__(self, timer, master, value):
                try:
                    values = entry.values if entry.values else value
                    super().__init__(timer, master, values)
                    if not _conditions_active(master, entry.conditions):
                        self.buff = []
                    if entry.side is not None:
                        self.target = _target(master, entry.side)
                except EquipConfigError:
                    raise
                except Exception as exc:
                    raise EquipConfigError(
                        f"装备 {eid} 的特效配置错误: {exc}\n配置内容: {config}"
                    ) from exc

        ConfigPythonSkill.__name__ = f'ConfigPythonSkill_esid{entry.esid}'
        result.append(ConfigPythonSkill)

    return result


def load_equip_config(config, eid='config'):
    """解析并验证配置，再转换为可写入 Equipment._skill 的技能类列表。"""
    try:
        parsed_entries = parse_equip_config(config)
        for entry in parsed_entries:
            _validate_entry(entry)

        skills = []
        effect_index = 0
        for entry in parsed_entries:
            if isinstance(entry, PythonEntry):
                skills.extend(_build_python_skill(entry, eid, config))
                continue

            entries = entry.entries if isinstance(entry, GroupEntry) else (entry,)
            effect_types = []
            for _ in entries:
                effect_index += 1
                effect_types.append(ConfigEffectType(eid, effect_index))
            skills.append(_build_equip_skill(entries, effect_types))
        return skills
    except EquipConfigError:
        raise
    except Exception as exc:
        raise EquipConfigError(
            f"装备 {eid} 的特效配置错误: {exc}\n配置内容: {config}"
        ) from exc
