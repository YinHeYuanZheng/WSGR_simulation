# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 约翰斯顿

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""萨马岛斗士(3级)：提升自身10点装甲值，11点鱼雷值。鱼雷战阶段，命中中型或大型船时造成45%的额外伤害。
"""


class Skill_112801_1(CommonSkill):
    """提升自身10点装甲值，11点鱼雷值。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=11,
                bias_or_weight=0
            )
        ]


class Skill_112801_2(Skill):
    """鱼雷战阶段，命中中型或大型船时造成45%的额外伤害。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=TorpedoPhase,
                value=.45,
                bias_or_weight=0
            )
        ]


name = "萨马岛斗士"
skill = [Skill_112801_1, Skill_112801_2]
