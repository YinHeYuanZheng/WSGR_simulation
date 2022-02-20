# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 信浓改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.formulas import *


class Skill_112231(Skill):
    """降低处于本舰上方位置的3艘舰船所受到的航空攻击伤害35%，
    并提高12点对空值和索敌值。"""
    def __init__(self, master):
        super().__init__(master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=3,
            direction='up',
        )
        self.buff = [
            FinalDamageBuff(
                name='final_damage_debuff',
                phase=(AllPhase,),
                value=-0.35,
                atk_request=[BuffRequest_1],
            ),
            StatusBuff(
                name='antiair',
                phase=(AllPhase, ),
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                name='recon',
                phase=(AllPhase, ),
                value=12,
                bias_or_weight=0
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, AirAtk)


skill = [Skill_112231]
