# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 加贺改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_110231(Skill):
    """舰攻队出击(3级)：开幕航空战阶段提升自身12%暴击率，炮击战阶段提升自身命中率12%"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.buff = [CoeffBuff(
            name='crit',
            phase=('AirPhase',),
            value=0.12,
            bias_or_weight=0,
        ), CoeffBuff(  # todo 加成命中率，阶段为炮击战
            name='',
            phase=('',),
            value=0.12,
            bias_or_weight=0,
        )]

    def is_active(self, friend, enemy):
        return True


skill = [Skill_110231]
