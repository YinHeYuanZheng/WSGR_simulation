# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 祥凤改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""降低敌方队伍内全部轻巡、重巡20点防空值、12点闪避值和12点命中值。
    炮击战阶段自身受到航母、装母攻击的概率增加20%。"""


class Skill_110241_1(Skill):
    """降低敌方队伍内全部轻巡、重巡20点防空值、12点闪避值和12点命中值。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=(CL, CA))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=(AllPhase,),
                value=-20,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=(AllPhase,),
                value=-12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=(AllPhase,),
                value=-12,
                bias_or_weight=0
            )
        ]


class Skill_110241_2(Skill):
    """炮击战阶段自身受到航母、装母攻击的概率增加20%。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MagnetBuff(
                timer,
                phase=(ShellingPhase,),
                master=master,
                rate=0.2,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.atk_body, (CV, AV))


skill = [Skill_110241_1, Skill_110241_2]
