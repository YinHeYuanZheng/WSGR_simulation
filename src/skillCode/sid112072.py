# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 南达科他-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""混战(3级)：增加自身与旗舰12点火力值和20点装甲值。
    敌方全队平均火力低于南达科他自身火力值时，炮击战阶段增加自身与旗舰20%炮击伤害，
    敌方全队平均火力值高于南达科他火力值时，增加自身与旗舰18%暴击率。
"""


class Skill_112072_1(Skill):
    """增加自身12点火力值和20点装甲值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ), StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]


class Skill_112072_2(Skill):
    """增加旗舰12点火力值和20点装甲值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = LocTarget(side=1, loc=[1])

        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ), StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]


class Skill_112072_3(Skill):
    """敌方全队平均火力低于南达科他自身火力值时，炮击战阶段增加自身20%炮击伤害"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=(ShellingPhase,),
                value=0.2
            )
        ]

    def is_active(self, friend, enemy):
        return enemy.get_final_status["fire"] < self.master.get_final_status["fire"]


class Skill_112072_4(Skill):
    """敌方全队平均火力低于南达科他自身火力值时，炮击战阶段增加旗舰20%炮击伤害"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = LocTarget(side=1, loc=[1])

        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=(ShellingPhase,),
                value=0.2
            )
        ]

    def is_active(self, friend, enemy):
        return enemy.get_final_status["fire"] < self.master.get_final_status["fire"]


class Skill_112072_5(Skill):
    """敌方全队平均火力值高于南达科他火力值时，增加自身18%暴击率"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=(AllPhase,),
                value=0.18,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return enemy.get_final_status["fire"] > self.master.get_final_status["fire"]


class Skill_112072_6(Skill):
    """敌方全队平均火力值高于南达科他火力值时，增加旗舰18%暴击率"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = LocTarget(side=1, loc=[1])

        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=(AllPhase,),
                value=0.18,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return enemy.get_final_status["fire"] > self.master.get_final_status["fire"]


skill = [Skill_112072_1, Skill_112072_2, Skill_112072_3, Skill_112072_4, Skill_112072_5, Skill_112072_6]
