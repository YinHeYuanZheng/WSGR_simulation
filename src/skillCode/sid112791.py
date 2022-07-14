# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 塞缪尔•罗伯茨

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""投石器(3级)：提升自身10点火力值，3点航速。自身射程变为长，炮击战阶段击中敌方大型或中型船时，有40%概率无视敌方所有装甲值。
"""


class Skill_112791(CommonSkill):
    """提升自身10点火力值，3点航速。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=(AllPhase,),
                value=10,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='speed',
                phase=(AllPhase,),
                value=3,
                bias_or_weight=0
            )
        ]


class Skill_112791_2(Skill):
    """自身射程变为长，炮击战阶段击中敌方大型或中型船时，有40%概率无视敌方所有装甲值。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='range',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            AtkBuff(
                timer=timer,
                name='ignore_armor',
                phase=ShellingPhase,
                value=1,
                bias_or_weight=1,
                atk_request=[Request_1],
                rate=0.4
            )
        ]


class Request_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (LargeShip, MidShip))


name = '投石器'
skill = [Skill_112791, Skill_112791_2]
