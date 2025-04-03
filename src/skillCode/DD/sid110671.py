# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 深雪改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import TorpedoAtk

"""鱼雷+30，回避+15。
炮击战35%概率发动，此次攻击变为鱼雷攻击，暴击率提高30%。
该效果触发后，自身回避-15，鱼雷战阶段不参与攻击。"""


class Skill_110671_1(CommonSkill):
    """鱼雷+30，回避+15。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_110671_2(Skill):
    """炮击战35%概率发动，此次攻击变为鱼雷攻击，暴击率提高30%。
    该效果触发后，自身回避-15，鱼雷战阶段不参与攻击。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialAtkBuff_110671_2(
                timer=timer,
                phase=ShellingPhase,
                rate=0.35,
                atk_type=TorpedoAtk,
                coef={'crit': 0.3},
                end_buff=[
                    ActPhaseBuff(
                        timer=timer,
                        name='not_act_phase',
                        phase=SecondTorpedoPhase
                    ),
                    StatusBuff(
                        timer=timer,
                        name='evasion',
                        value=-15,
                        phase=AllPhase,
                        bias_or_weight=0
                    )
                ]
            )
        ]


class SpecialAtkBuff_110671_2(SpecialAtkBuff):
    """使用雷击公式的炮击
    20250329再次确认"""
    def get_def_list(self, atk_type, enemy):
        from src.wsgr.formulas import NormalAtk
        def_list = super().get_def_list(NormalAtk, enemy)
        return def_list


name = '水雷强袭'
skill = [Skill_110671_1, Skill_110671_2]
