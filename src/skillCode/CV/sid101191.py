# -*- coding:utf-8 -*-
# Author:zzhh225
# Edited by: 银河远征(20260410)
# env:py38
# 皇家方舟-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.equipment import *

"""精准打击(3级)：自身命中率提高30%，携带的轰炸机轰炸值增加6点。
被自身攻击命中的敌人回避值和装甲值减少30点，被暴击率提高30%。"""


class Skill_101191_1(CommonSkill):
    """携带的轰炸机轰炸值增加6点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(
            side=1,
            target=SelfTarget(master),
            equiptype=Bomber,
        )
        self.buff = [
            CommonBuff(
                timer=timer,
                name='bomb',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            )
        ]


class Skill_101191_2(Skill):
    """自身命中率提高30%；攻击命中的敌人回避值和装甲值减少30点，被暴击率提高30%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0
            ),
            AtkHitBuff(
                timer,
                name='atk_hit',
                phase=AllPhase,
                buff=[
                    StatusBuff(
                        timer,
                        name='evasion',
                        phase=AllPhase,
                        value=-30,
                        bias_or_weight=0
                    ),
                    StatusBuff(
                        timer,
                        name='armor',
                        phase=AllPhase,
                        value=-30,
                        bias_or_weight=0
                    ),
                    CoeffBuff(
                        timer,
                        name='be_crit',
                        phase=AllPhase,
                        value=0.3,
                        bias_or_weight=0
                    )
                ],
                side=0
            )
        ]


name = '精准打击'
skill = [Skill_101191_1, Skill_101191_2]
