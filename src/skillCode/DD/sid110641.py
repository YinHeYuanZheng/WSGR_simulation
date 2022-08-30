# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 吹雪改-1

from src.wsgr.formulas import TorpedoAtk
from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身的鱼雷攻击有 30% 额外概率触发暴击。
当队伍中特型驱逐舰的数量在4艘或4艘以上时，提升队伍中所有特型驱逐舰的鱼雷，命中，回避 7 点。"""


class Skill_110641_1(Skill):
    """自身的鱼雷攻击有 30% 额外概率触发暴击。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=.3,
                bias_or_weight=0,
                atk_request=ATK_request_1
            )
        ]


class ATK_request_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, TorpedoAtk)


class Skill_110641_2(Skill):
    """当队伍中特型驱逐舰的数量在4艘或4艘以上时，提升队伍中所有特型驱逐舰的鱼雷，命中，回避 7 点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TagTarget(side=1, tag='fubuki')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=7,
                bias_or_weight=0,
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=7,
                bias_or_weight=0,
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=7,
                bias_or_weight=0,
            )
        ]

    def is_active(self, friend, enemy):
        count = len(self.target.get_target(friend, enemy))
        return count >= 4


name = '水雷战队'
skill = [Skill_110641_1, Skill_110641_2]
