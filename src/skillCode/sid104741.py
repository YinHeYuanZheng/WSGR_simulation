# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 72工程-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自身15点火力值，航空战阶段优先攻击对位敌人，命中过的对位敌人在炮击战阶段无法攻击。"""


class Skill_101471_1(CommonSkill):
    """增加自身15点火力值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=(AllPhase,),
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_101471_2(Skill):
    """航空战阶段优先攻击对位敌人,
    todo 命中过的对位敌人在炮击战阶段无法攻击"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_loc_target',
                phase=(AirPhase,),
                target=LocTarget(
                    side=0,
                    loc=[self.master.loc]
                ),
                ordered=True
            ),
        ]


skill = [Skill_101471_1, Skill_101471_2]
