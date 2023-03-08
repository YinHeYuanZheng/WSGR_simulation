# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 埃塞克斯-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""猎火鸡比赛(3级)：提升自身6点火力值。
战斗中当敌方有装母、航母或者轻母时，随机降低敌方一艘装母、航母或者轻母的火力值20点。"""


class Skill_102261_1(CommonSkill):
    """提升自身6点火力值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=(AllPhase,),
                value=6,
                bias_or_weight=0
            )
        ]


class Skill_102261_2(Skill):
    """战斗中当敌方有装母、航母或者轻母时，随机降低敌方一艘装母、航母或者轻母的火力值20点。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = RandomTypeTarget(side=0, shiptype=(AV, CV, CVL))

        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=(AllPhase,),
                value=-20,
                bias_or_weight=0
            )
        ]


name = '猎火鸡比赛'
skill = [Skill_102261_1, Skill_102261_2]
