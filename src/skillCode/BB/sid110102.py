# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 威尔士亲王-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""敌方全体舰船装甲值和回避值降低12点。
炮击战阶段自身优先攻击位置排在前方的敌方战列，自身攻击战列时攻击威力不会因耐久损伤而降低。"""


class Skill_110102_1(Skill):
    """敌方全体舰船装甲值和回避值降低12点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=0)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-12,
                bias_or_weight=0
            )
        ]


class Skill_110102_2(Skill):
    """炮击战阶段自身优先攻击位置排在前方的敌方战列，自身攻击战列时攻击威力不会因耐久损伤而降低。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=ShellingPhase,
                target=TypeTarget(side=0, shiptype=BB),
                ordered=True
            ),
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=ShellingPhase,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, BB)


name = '关键一击'
skill = [Skill_110102_1, Skill_110102_2]
