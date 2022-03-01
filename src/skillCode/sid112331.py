# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 最上改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_112331_1(CommonSkill):
    """增加自身索敌值12点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [CommonBuff(
            timer=timer,
            name='recon',
            phase=(AllPhase,),
            value=12,
            bias_or_weight=0
        )]


class Skill_112331_2(Skill):
    """提升我方全体命中值12点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer,
                name='accuracy',
                phase=(AllPhase,),
                value=12,
                bias_or_weight=0
            )
        ]


class Skill_112331_3(Skill):
    """提升我方中型船10%暴击率，如果是J国中型船提升双倍暴击率"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(MidShip,))
        self.buff = [
            CoeffBuff(
                timer,
                name='crit',
                phase=(AllPhase,),
                value=0.1,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_ship in target:
            if tmp_ship.status['country'] == 'J':
                tmp_ship.add_buff(
                    CoeffBuff(
                        timer=self.timer,
                        name='crit',
                        phase=(AllPhase,),
                        value=0.2,
                        bias_or_weight=0
                    )
                )
            else:
                tmp_ship.add_buff(
                    CoeffBuff(
                        timer=self.timer,
                        name='crit',
                        phase=(AllPhase,),
                        value=0.1,
                        bias_or_weight=0
                    )
                )


skill = [Skill_112331_1, Skill_112331_2, Skill_112331_3]
