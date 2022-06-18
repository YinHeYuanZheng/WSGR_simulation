# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 基辅


from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""舰队前卫(3级)：增加自身10点闪避值，鱼雷战阶段增加20%伤害；增加队伍内高速舰9点火力值。
"""


class Skill_113231_1(CommonBuff):
    """增加自身10点闪避值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]


class Skill_113231_2(Skill):
    """鱼雷战阶段增加20%伤害"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=TorpedoPhase,
                value=0.2
            )
        ]


class Skill_113231_3(Skill):
    """增加队伍内高速舰9点火力值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = StatusTarget(side=1,
                                   status_name='speed',
                                   fun='ge',
                                   value=27)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            )
        ]


name = "舰队前卫"
skill = [Skill_113231_1, Skill_113231_2, Skill_113231_3]
