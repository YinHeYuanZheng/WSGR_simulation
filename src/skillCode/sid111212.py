# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 企业改-2

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *

"""大E(3级)：增加自身闪避值10点、火力值15点与暴击率20%，首轮炮击必中。炮击战阶段，优先攻击敌方耐久值最高的单位，被命中的单位降低装甲值10点与火力值10点。
"""

class Skill_111212(CommonSkill):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.target = SelfTarget(master)

        self.buff = [CommonBuff(
            name='evasion',
            phase=(AllPhase,),
            value=10,
            bias_or_weight=0
        ), CommonBuff(
            name='fire',
            phase=(AllPhase,),
            value=15,
            bias_or_weight=0
        ), CoeffBuff(
            name='crit',
            phase=(AllPhase,),
            value=0.20,
            bias_or_weight=0
        )]


# todo 炮击战锁头
skill = [Skill_111212]
