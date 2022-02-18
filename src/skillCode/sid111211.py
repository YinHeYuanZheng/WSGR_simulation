# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 企业改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *

"""独木成林(3级)：增加自身回避20点，并且队伍中没有其余航母（航母，轻母，装母）存在时，自身射程变更为长,火力加成55点
"""
class Skill_111211(Skill):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.target = SelfTarget(master)

        self.buff = [CommonBuff(
            name='evasion',
            phase=(AllPhase,),
            value=20,
            bias_or_weight=0
        )]


class Skill_111211_1(Skill):
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.request = [Request_1]
        self.range = 3 - master.status.range
        self.buff = [StatusBuff(
            name='range',
            phase=(AllPhase,),
            value=self.range,
            bias_or_weight=0
        ), StatusBuff(
            name='fire',
            phase=(AllPhase,),
            value=55,
            bias_or_weight=0
        )]

    def is_active(self, friend, enemy):
        return bool(self.request[0](self.master, friend, enemy))


class Request_1(Request):
    def __bool__(self):
        num = TypeTarget(side=1, shiptype=('CV', 'CVL', 'AV')).get_target(self.friend, self.enemy)
        return num == 1


skill = [Skill_111211, Skill_111211_1]
