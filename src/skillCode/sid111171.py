# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 大凤改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *

"""穿梭轰炸(3级)：队伍中该舰下方位置的3艘航母（轻航，正规航母，装甲航母）增加回避6点，并且炮击战可进行二次攻击，但二次攻击的伤害减低50%。
"""
class Skill_111171(Skill):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.buff = [StatusBuff(
            name='accuracy',
            phase=(AllPhase, ),
            value=6,
            bias_or_weight=0
        )]

    def is_active(self, friend, enemy):
        return True


skill = [Skill_111171]