# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# L20-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加全队9点命中值、9点装甲值。
首轮炮击阶段被L20命中的单位会降低15点装甲值，并且该单位昼战阶段不再行动（对旗舰无效）。"""


class Skill_104501_1(Skill):
    """增加全队9点命中值、9点装甲值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            )
        ]


class Skill_104501_2(Skill):
    """首轮炮击阶段被L20命中的单位会降低15点装甲值，并且该单位昼战阶段不再行动（对旗舰无效）"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=FirstShellingPhase,
                buff=[
                    StatusBuff(
                        timer=timer,
                        name='armor',
                        phase=AllPhase,
                        value=-15,
                        bias_or_weight=0
                    ),
                    ActPhaseBuff(
                        timer=timer,
                        name='not_act_phase',
                        phase=DaytimePhase,
                    )
                ],
                side=0,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.target.loc != 1


skill = [Skill_104501_1, Skill_104501_2]
