# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 信浓改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import *


class Skill_112231_1(Skill):
    """降低处于本舰上方位置的3艘舰船所受到的航空攻击伤害35%，并提高12点对空值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=3,
            direction='up',
        )
        self.buff = [
            FinalDamageBuff(
                timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-0.35,
                atk_request=[BuffRequest_1]
            ),
            StatusBuff(
                timer,
                name='antiair',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, AirAtk)


class Skill_112231_2(PrepSkill):
    """提高处于本舰上方位置的3艘舰船12点索敌值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=3,
            direction='up',
        )
        self.buff = [
            StatusBuff(
                timer,
                name='recon',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]


name = '穿梭支援'
skill = [Skill_112231_1, Skill_112231_2]
