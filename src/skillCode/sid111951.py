# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 射水鱼

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""必定优先攻击正规航母和装甲航母，攻击航母类单位(轻航，正规航母，装甲航母)时，命中值增加 10 点，且暴击时伤害为习得技能前的 1.2 倍。"""


class Skill_111951_1(Skill):
    """必定优先攻击正规航母和装甲航母"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master, side=1)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=AllPhase,
                target=TypeTarget(side=0, shiptype=[CV,CVL,AV]),
                ordered=False
            ),
        ]
class Skill_111951_2(Skill):
    def __init__(self, timer, master):
        "攻击航母类单位(轻航，正规航母，装甲航母)时，命中值增加 10 点，且暴击时伤害为习得技能前的 1.2 倍。"
        super().__init__(timer, master)
        "wait to be done"
skill = [Skill_111951_1,]
