# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 企业改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_111212_1(CommonSkill):
    """增加自身闪避值10点、火力值15点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=(AllPhase,),
                value=10,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='fire',
                phase=(AllPhase,),
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_111212_2(Skill):
    """增加自身暴击率20%，首轮炮击必中"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=(AllPhase,),
                value=0.20,
                bias_or_weight=0
            ),
            # todo 首轮炮击必中
        ]


# todo 炮击战阶段，优先攻击敌方耐久值最高的单位，被命中的单位降低装甲值10点与火力值10点
skill = [Skill_111212_1, Skill_111212_2]
