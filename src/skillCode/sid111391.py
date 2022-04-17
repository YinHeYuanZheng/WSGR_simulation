# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 彭萨科拉改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import TorpedoAtk

"""灰色幽灵(3级)：遭受鱼雷攻击时受到伤害减少30%，回避值降低15点，增加自身火力与装甲20点"""


class Skill_111391(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-0.3,
                atk_request=[ATKRequest_1]
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
        ]


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, TorpedoAtk)


skill = [Skill_111391]
