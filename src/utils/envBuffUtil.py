# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 环境加成

import copy
import json
import os
import re
import pandas as pd
import yaml
from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
import src.wsgr.ship as rship
import src.wsgr.phase as rphase


COLUMN_MAP = {
    '名称': 'name',
    '国籍': 'country',
    '舰种': 'shiptype',
    '备注': 'description',
    '生效': 'valid',
    '火力': 'fire',
    '鱼雷': 'torpedo',
    '装甲': 'armor',
    '对空': 'antiair',
    '对潜': 'antisub',
    '命中': 'accuracy',
    '回避': 'evasion',
    '索敌': 'recon',
    '航速': 'speed',
    '幸运': 'luck',
    '暴击': 'crit',
    '伤害提升': 'final_damage_buff',
    '受伤降低': 'final_damage_debuff',
    '无视战损': 'ignore_damaged',
    '无视补给': 'ignore_supply',
    '必中': 'must_hit',
    '参与阶段': 'act_phase',
}

ENVIRONMENT_SHEETS = {
    'engineering': '工程局',
    'extras': '额外加成',
    'dish': '菜谱',
    'collections': '摆件',
    'car': '赛车',
}
_ENVIRONMENT_SHEET_CACHE = {}
ENV_CID_EXPR_RE = re.compile(r'Cid\((.*)\)')


def default_user_settings():
    """Return settings that preserve the simulator's previous behaviour."""
    return {
        'engineering': True,
        'collections': [],
        'dish': None,
        'car': {
            'name': None,
            'country': '',
        },
        'extras': [],
    }


def _read_environment_sheets(file_path):
    absolute_path = os.path.abspath(file_path)
    stat = os.stat(absolute_path)
    cache_key = (absolute_path, stat.st_mtime_ns, stat.st_size)
    cached = _ENVIRONMENT_SHEET_CACHE.get(cache_key)
    if cached is not None:
        return cached

    sheets = {}
    for key, sheet_name in ENVIRONMENT_SHEETS.items():
        df = pd.read_excel(
            file_path, sheet_name=sheet_name,
            keep_default_na=False, dtype=str,
        )
        df.rename(columns=COLUMN_MAP, inplace=True)
        sheets[key] = [row.to_dict() for _, row in df.iterrows()]
    _ENVIRONMENT_SHEET_CACHE.clear()
    _ENVIRONMENT_SHEET_CACHE[cache_key] = sheets
    return sheets


def environment_options(file_path):
    """Return JSON-friendly choices for the WebUI."""
    sheets = _read_environment_sheets(file_path)
    return {
        key: [
            {
                'id': str(row.get('name', '')),
                'label': str(row.get('description') or row.get('name') or ''),
            }
            for row in rows
            if row.get('name')
        ]
        for key, rows in sheets.items()
        if key != 'engineering'
    }


def _normalise_selected_ids(value, allowed, label, maximum=None):
    if value is None:
        values = []
    elif isinstance(value, list):
        values = [str(item).strip() for item in value if str(item).strip()]
    else:
        raise ValueError(f'{label}必须为列表')
    values = list(dict.fromkeys(values))
    if maximum is not None and len(values) > maximum:
        raise ValueError(f'{label}最多选择{maximum}项')
    unknown = [item for item in values if item not in allowed]
    if unknown:
        raise ValueError(f'{label}包含未知项目：{", ".join(unknown)}')
    return values


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


def normalise_user_settings(settings, file_path):
    """Validate and normalise persisted environment settings."""
    if settings is None:
        settings = {}
    if not isinstance(settings, dict):
        raise ValueError('全局增益设置必须为对象')

    sheets = _read_environment_sheets(file_path)
    allowed = {
        key: {str(row.get('name', '')) for row in rows if row.get('name')}
        for key, rows in sheets.items()
    }
    result = default_user_settings()
    engineering = settings.get('engineering', result['engineering'])
    if isinstance(engineering, str):
        engineering = engineering.strip().lower() not in ('', '0', 'false', 'off', 'no')
    result['engineering'] = bool(engineering)
    result['collections'] = _normalise_selected_ids(
        settings.get('collections'), allowed['collections'], '摆件', maximum=3,
    )
    result['extras'] = _normalise_selected_ids(
        settings.get('extras'), allowed['extras'], '额外加成',
    )

    dish = settings.get('dish')
    dish = None if dish in (None, '') else str(dish).strip()
    if dish is not None and dish not in allowed['dish']:
        raise ValueError(f'菜谱包含未知项目：{dish}')
    result['dish'] = dish

    car_settings = settings.get('car') or {}
    if not isinstance(car_settings, dict):
        raise ValueError('赛车设置必须为对象')
    car_name = car_settings.get('name')
    car_name = None if car_name in (None, '') else str(car_name).strip()
    if car_name is not None and car_name not in allowed['car']:
        raise ValueError(f'赛车包含未知项目：{car_name}')
    country = str(car_settings.get('country') or '').strip()
    if car_name is not None and not country:
        raise ValueError('选择赛车增益后必须填写国籍')
    result['car'] = {
        'name': car_name,
        'country': country if car_name is not None else '',
    }
    return result


def load_user_settings(settings_path, file_path):
    if not os.path.exists(settings_path):
        return default_user_settings()
    with open(settings_path, 'r', encoding='utf-8') as file:
        return normalise_user_settings(yaml.safe_load(file), file_path)


def save_user_settings(settings, settings_path, file_path):
    settings = normalise_user_settings(settings, file_path)
    os.makedirs(os.path.dirname(settings_path), exist_ok=True)
    temporary_path = settings_path + '.tmp'
    with open(temporary_path, 'w', encoding='utf-8') as file:
        yaml.safe_dump(settings, file, allow_unicode=True, sort_keys=False)
    os.replace(temporary_path, settings_path)
    return settings


class AllTarget(Target):
    """针对双方全体(可指定筛选类型)"""

    def __init__(self, side=None, target: Target = None):
        super().__init__(side)
        self.target = target

    def get_target(self, friend, enemy):
        if self.target is not None:
            target_1 = self.target.get_target(friend, enemy)
            target_0 = self.target.get_target(enemy, friend)
            return target_1 + target_0
        else:
            if isinstance(friend, Fleet):
                friend = friend.ship
            if isinstance(enemy, Fleet):
                enemy = enemy.ship
            return friend + enemy


class Normal_map9_lock_buff(PrepSkill):
    """9图解封锁buff"""
    def __init__(self, timer):
        class LeaderSurviveBuff(FinalDamageBuff):
            def is_active(self, *args, **kwargs):
                leader = self.master.master.ship[0]
                return leader.damaged <= 3

        super().__init__(timer, master=None)
        self.target = LocTarget(side=0, loc=[2,3,4,5,6])
        self.buff = [
            LeaderSurviveBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-0.1
            )
        ]


def _parse_environment_cids(value, environment_name='环境增益'):
    """解析环境表“舰种”列中的 Cid(...) 目标表达式。"""
    match = ENV_CID_EXPR_RE.fullmatch(value)
    if match is None:
        if value.startswith('Cid'):
            raise ValueError(
                f'{environment_name}: 舰种列 Cid 语法错误，应填写 Cid(编号)'
            )
        return None

    raw_value = match.group(1).strip()
    if not raw_value:
        raise ValueError(f'{environment_name}: 舰种列 Cid 不能为空')
    try:
        cid_value = json.loads(raw_value)
    except json.JSONDecodeError:
        cid_value = raw_value
    try:
        return _normalize_cid(cid_value)
    except ValueError as exc:
        raise ValueError(
            f'{environment_name}: 舰种列 Cid 配置错误: {exc}'
        ) from exc


def _build_environment_target(config):
    """根据国籍和舰种/Cid配置构建仅作用于我方的目标。"""
    target_list = []
    country = str(config.get('country', '')).strip()
    if country:
        target_list.append(CountryTarget(side=1, country=country))

    shiptype = str(config.get('shiptype', '')).strip()
    if shiptype:
        cid_list = _parse_environment_cids(
            shiptype, str(config.get('name') or '环境增益')
        )
        if cid_list is not None:
            target_list.append(CidTarget(side=1, cid_list=cid_list))
        else:
            try:
                types = tuple(
                    getattr(rship, name.strip())
                    for name in shiptype.split(',')
                    if name.strip()
                )
            except AttributeError as exc:
                raise ValueError(
                    f'{config.get("name") or "环境增益"}: 未知舰种 {shiptype}'
                ) from exc
            if types:
                target_list.append(TypeTarget(side=1, shiptype=types))

    if len(target_list) > 1:
        return CombinedTarget(side=1, target_list=target_list)
    if len(target_list) == 1:
        return target_list[0]
    return Target(side=1)


def dynamic_init(self, timer, config: dict):
    super(self.__class__, self).__init__(timer, master=None)

    # --- Target 构建 ---
    self.target = _build_environment_target(config)

    # --- Buff 构建 ---
    self.buff = []

    # A. 基础属性 (StatusBuff)
    status_name_list = ['fire', 'torpedo', 'armor', 'antiair', 'antisub',
                        'accuracy', 'evasion', 'recon', 'speed', 'luck'
                        ]
    for name in status_name_list:
        val = config.get(name)
        if val != '':
            self.buff.append(
                StatusBuff(
                    timer=timer,
                    name=name,
                    phase=AllPhase,
                    value=float(val),
                    bias_or_weight=0
                )
            )

    # B. 暴击 (CoeffBuff)
    crit_val = config.get('crit')
    if crit_val != '':
        self.buff.append(
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=float(crit_val),
                bias_or_weight=0
            )
        )

    # C. 伤害加成/减免 (FinalDamageBuff)
    for name in ['final_damage_buff', 'final_damage_debuff']:
        val = config.get(name)
        if val == '':
            continue

        # 将全角标点符号转为半角
        val = val.replace('：', ':')
        val = val.replace('；', ';')

        # 尝试解析字典格式，如 ShellingPhase:0.1;
        try:
            val_data = {k: float(v) for k, v in (item.split(':') for item in val.split(';'))}
        except:
            raise ValueError(f'{type(self).__name__}: {name} 填写格式错误')
        if isinstance(val_data, dict):
            for p_name, p_val in val_data.items():
                # 使用 getattr 动态获取阶段
                assert p_name in rphase.__all__, f'{type(self).__name__}: {name} 阶段填写错误'
                phase = getattr(rphase, p_name)
                self.buff.append(
                    FinalDamageBuff(
                        timer=timer,
                        name=name,
                        phase=phase,
                        value=p_val
                    )
                )

    # D. 特殊效果 (SpecialBuff)
    for name in ['ignore_damaged', 'ignore_supply', 'must_hit', 'act_phase']:
        val = config.get(name)
        if val == '':
            continue
        # 如果单元格填了 TRUE/1 等
        if val in ['1', 'TRUE', 'True']:
            assert name not in ['must_hit', 'act_phase'], f'{type(self).__name__}: {name} 填写格式错误'
            self.buff.append(
                SpecialBuff(
                    timer=timer,
                    name=name,
                    phase=AllPhase
                )
            )
        else:
            try:
                phase = getattr(rphase, val)
            except:
                raise Exception(f'{type(self).__name__}: {name} 阶段填写错误')
            self.buff.append(
                SpecialBuff(
                    timer=timer,
                    name=name,
                    phase=phase
                )
            )


def create_skill_class(cls, config):
    """
    使用 type() 动态创建一个类，就像写了 class Name(Skill): ... 一样
    """

    # 将当前的配置行固化到初始化函数中
    def wrapped_init(self, timer):
        dynamic_init(self, timer, config)

    # 参数：类名，父类元组，属性字典
    return type(cls, (PrepSkill,), {"__init__": wrapped_init})


def load_env_buffs(file_path, settings_path=None):
    """从Excel读取并返回技能实例列表"""
    sheets = _read_environment_sheets(file_path)
    selected_configs = []
    if settings_path is None or not os.path.exists(settings_path):
        for rows in sheets.values():
            selected_configs.extend(
                config for config in rows
                if str(config.get('valid', '')).strip().lower() not in ('', '0', 'false')
            )
    else:
        settings = load_user_settings(settings_path, file_path)
        if settings['engineering']:
            selected_configs.extend(
                config for config in sheets['engineering']
                if str(config.get('valid', '')).strip().lower() not in ('', '0', 'false')
            )

        selected = {
            'collections': set(settings['collections']),
            'extras': set(settings['extras']),
            'dish': {settings['dish']} if settings['dish'] else set(),
            'car': {settings['car']['name']} if settings['car']['name'] else set(),
        }
        for category, names in selected.items():
            for config in sheets[category]:
                if config.get('name') not in names:
                    continue
                config = copy.deepcopy(config)
                if category == 'car':
                    config['country'] = settings['car']['country']
                selected_configs.append(config)

    env_skills = []
    for i, config in enumerate(selected_configs):
        name = config.get('name', f'DynamicSkill_{i+1}').replace(' ', '_')
        # 过滤非法字符确保符合Python类名规范(支持字符：字母、数字、下划线)
        safe_class_name = "".join(c for c in name if c.isalnum() or c == "_")

        # 创建类(不是实例!)
        SkillClass = create_skill_class(safe_class_name, config)
        env_skills.append(SkillClass)
    return env_skills


def reload_env_buffs():
    """服务端更新设置后重新加载env"""
    additional_env = env[len(_configured_env):]
    _configured_env[:] = load_env_buffs(data_file, user_settings_file)
    env[:] = [*_configured_env, *additional_env]
    return env


curDir = os.path.dirname(__file__)
srcDir = os.path.dirname(curDir)
dependDir = os.path.join(os.path.dirname(srcDir), 'depend')
data_file = os.path.join(dependDir, r'environment/environment.xlsx')
user_settings_file = os.path.join(dependDir, r'environment/user_settings.yaml')
_configured_env = load_env_buffs(data_file, user_settings_file)
env = _configured_env.copy()
env += []
