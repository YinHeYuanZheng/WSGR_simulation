# -*- coding:utf-8 -*-
# Author:银河远征(AI supported)
# env:py38
"""Code-defined map effects referenced by standalone map YAML documents."""

from __future__ import annotations

from importlib import import_module
from pkgutil import iter_modules
import re
from types import ModuleType


_MAP_EFFECT_ID = re.compile(r"^map[A-Za-z0-9_]+$")


def _module_names() -> list[str]:
    """返回当前所有可用地图效果编号"""
    return sorted(
        module.name
        for module in iter_modules(__path__)
        if not module.ispkg and _MAP_EFFECT_ID.fullmatch(module.name)
    )


def _load_module(effect_id: str) -> ModuleType:
    """检查编号并加载对应模块"""
    normalized = str(effect_id).strip()
    if not _MAP_EFFECT_ID.fullmatch(normalized):
        raise ValueError(f"Invalid map effect id: {effect_id!r}")
    if normalized not in _module_names():
        raise ValueError(f"Unknown map effect: {normalized}")
    return import_module(f"{__name__}.{normalized}")


def load_map_effect(effect_id: str) -> tuple[str, list[type]]:
    """读取并验证技能文件中的 name、effect 和 skill。"""
    module = _load_module(effect_id)
    name = getattr(module, "name", None)
    effect = getattr(module, "effect", None)
    skills = getattr(module, "skill", None)
    if not isinstance(name, str) or not name.strip():
        raise ValueError(f"Map effect {effect_id!r} must define a non-empty name")
    if not isinstance(effect, str) or not effect.strip():
        raise ValueError(f"Map effect {effect_id!r} must define a non-empty effect")
    if not isinstance(skills, list) or not skills or not all(callable(item) for item in skills):
        raise ValueError(f"Map effect {effect_id!r} must define a non-empty skill list")
    return name.strip(), skills[:]


def map_effect_options() -> list[dict[str, str]]:
    """生成 WebUI 所需的地图效果编号、名称和效果说明。"""
    options = []
    for effect_id in _module_names():
        module = _load_module(effect_id)
        name, _ = load_map_effect(effect_id)
        options.append({
            "id": effect_id,
            "name": name,
            "effect": module.effect.strip(),
        })
    return options
