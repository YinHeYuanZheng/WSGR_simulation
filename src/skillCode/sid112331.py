# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 最上改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
"""航空掩护(3级)：增加自身索敌值12点，提升我方全体命中值12点。提升我方中型船10%暴击率，如果是J国中型船提升双倍。
"""

class Skill_112331_1(CommonSkill):
    """增加自身索敌值12点"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.buff = [CommonBuff(
            name='recon',
            phase=(AllPhase,),
            value=12,
            bias_or_weight=0
        )]


class Skill_112331_2(CommonSkill):
    """提升我方全体命中值12点"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = Target(side=1)
        self.buff = [CommonBuff(
            name='accuracy',
            phase=(AllPhase,),
            value=12,
            bias_or_weight=0
        )]


class Skill_112331_3(Skill):
    """提升我方中型船10%暴击率"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = TypeTarget(side=1, shiptype=('CL', 'CVL', 'CA', 'CAV', 'CLT'))
        self.buff = [CoeffBuff(
            name='crit',
            phase=(AllPhase,),
            value=0.1,
            bias_or_weight=0
        )]


class Skill_112331_4(Skill):
    """如果是J国中型船提升双倍%暴击率"""

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        # todo 国籍检测
        self.target = TypeTarget(side=1, shiptype=('CL', 'CVL', 'CA', 'CAV', 'CLT'))
        self.buff = [CoeffBuff(
            name='crit',
            phase=(AllPhase,),
            value=0.1,
            bias_or_weight=0
        )]


skill = [Skill_112331_1, Skill_112331_2, Skill_112331_3, Skill_112331_4]
