# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 汉考克-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.equipment import *


class Skill_103741_1(Skill):
    """增加自身装备的轰炸机的轰炸值4点。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(side=1,
                                  target=SelfTarget(master),
                                  equiptype=(Bomber,))
        self.buff = [
            CommonBuff(
                timer=timer,
                name='bomb',
                phase=(AllPhase,),
                value=4,
                bias_or_weight=0
            )
        ]


class Skill_103741_2(Skill):
    """队伍中航母装母总数量小于3时，提升自身火力值10点；"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=(AllPhase,),
                value=10,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        target = TypeTarget(
            side=1,
            shiptype=(CV, AV)
        ).get_target(friend, enemy)
        return len(target) < 3


class Skill_103741_3(Skill):
    """队伍中航母装母总数量大于等于3时，提升自身装甲值9点与命中值9点。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=(AllPhase,),
                value=9,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=(AllPhase,),
                value=9,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        target = TypeTarget(
            side=1,
            shiptype=(CV, AV)
        ).get_target(friend, enemy)
        return len(target) >= 3


name = '多用途航母'
skill = [Skill_103741_1, Skill_103741_2, Skill_103741_3]
