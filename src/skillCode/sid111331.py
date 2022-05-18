# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 青叶-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""如果敌方单位中存在昆西，则青叶全阶段优先攻击昆西。
当敌方单位没有昆西的情况下，闭幕雷击阶段，35%概率将目标变成旗舰。
增加自身鱼雷值20点。"""


class Skill_111331_1(Skill):
    """如果敌方单位中存在昆西，则青叶全阶段优先攻击昆西。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=AllPhase,
                target=CidTarget(side=0, cid_list=['10040', '11040']),
                ordered=True
            )
        ]

    def is_active(self, friend, enemy):
        quincy = CidTarget(side=0, cid_list=['10040', '11040']
                           ).get_target(friend, enemy)
        return len(quincy)


class Skill_111331_2(Skill):
    """当敌方单位没有昆西的情况下，闭幕雷击阶段，35%概率将目标变成旗舰。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_loc_target',
                phase=SecondTorpedoPhase,
                target=LocTarget(side=0, loc=[1]),
                ordered=True,
                rate=0.35
            )
        ]

    def is_active(self, friend, enemy):
        quincy = CidTarget(side=0, cid_list=['10040', '11040']
                           ).get_target(friend, enemy)
        return not len(quincy)


class Skill_111331_3(CommonSkill):
    """增加自身鱼雷值20点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]


skill = [Skill_111331_1, Skill_111331_2, Skill_111331_3]
