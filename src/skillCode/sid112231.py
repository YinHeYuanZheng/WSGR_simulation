# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 信浓改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_112231_1(Skill):
    """本舰上方位置的3艘舰船提高12点对空值和索敌值。"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)  # todo 目标选择
        self.buff = [StatusBuff(
                name='antiair',
                phase=(AllPhase, ),
                value=12,
                bias_or_weight=0
            ), StatusBuff(
                name='recon',
                phase=(AllPhase, ),
                value=12,
                bias_or_weight=0
            )

        ]

    def is_active(self, friend, enemy):
        return True


class Skill_112231_2(Skill):
    """降低处于本舰上方位置的3艘舰船所受到的航空攻击伤害35%，"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)  # todo 目标选择
        self.request = [Request_1]
        self.buff = [
            CoeffBuff(
                name='',  # todo 终伤倍率
                phase=(AllPhase,),
                value=0.35,
                bias_or_weight=2,
            )
        ]

    def is_active(self, friend, enemy):
        return bool(self.request[0](self.master, friend, enemy))


class Request_1(Request):
    def __bool__(self):
        # todo 检测是否为航空攻击
        return True


skill = [Skill_112231_1, Skill_112231_2]
