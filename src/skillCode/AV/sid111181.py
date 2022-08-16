# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 齐柏林伯爵改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""斯图卡(3级)：当队伍中战列数量大于2时，增加全队战列舰9%暴击率，9点命中值；
当队伍中没有战列时，增加自身25%暴击率，20点装甲值。炮击战阶段，被齐柏林命中的非旗舰单位在炮击战阶段不再行动。
"""


class Skill_111181_1(Skill):
    """当队伍中战列数量大于2时，增加全队战列舰9%暴击率，9点命中值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(BB,))
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.09,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        number = len(
            TypeTarget(
                side=1,
                shiptype=BB
            ).get_target(friend, enemy)
        )
        return number > 2


class Skill_111181_2(Skill):
    """当队伍中没有战列时，增加自身25%暴击率，20点装甲值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.25,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        number = len(
            TypeTarget(
                side=1,
                shiptype=BB
            ).get_target(friend, enemy)
        )
        return number == 0


class Skill_111181_3(Skill):
    """炮击战阶段，被齐柏林命中的非旗舰单位在炮击战阶段不再行动。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=ShellingPhase,
                buff=[
                    ActPhaseBuff(
                        timer=timer,
                        name='not_act_phase',
                        phase=ShellingPhase
                    )
                ],
                side=0,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.target.loc != 1


name = '斯图卡'
skill = [Skill_111181_1, Skill_111181_2, Skill_111181_3]


