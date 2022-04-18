# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 伏尔塔改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""高速小队(3级)：增加相邻两个单位（限驱逐舰和轻巡）的航速4点和回避值12点，命中敌方时会造成额外20点伤害；
当伟大的庞贝位于舰队中时，额外增加自身和伟大的庞贝两个单位的命中值15点和15暴击率。"""


class Skill_113351_1(PrepSkill):
    """增加相邻两个单位（限驱逐舰和轻巡）的航速4点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1, master=master, radius=1, direction='near', shiptype=(CL, DD)
        )

        self.buff = [
            StatusBuff(
                timer=timer,
                name='speed',
                phase=AllPhase,
                value=4,
                bias_or_weight=0
            )
        ]


class Skill_113351_2(Skill):
    """增加相邻两个单位（限驱逐舰和轻巡）的回避值12点，命中敌方时会造成额外20点伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1, master=master, radius=1, direction='near', shiptype=(CL, DD)
        )

        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='extra_damage',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]


class Skill_113351_3(Skill):
    """当伟大的庞贝位于舰队中时，额外增加自身和伟大的庞贝两个单位的命中值15点和15暴击率"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.target_2 = None
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        for tmp_ship in friend:
            if tmp_ship.cid == '10337' or tmp_ship.cid == '11337':
                self.target_2 = tmp_ship
                return True
        return False

    def activate(self, friend, enemy):
        if self.target_2 is None:
            return
        target = self.target.get_target(friend, enemy)
        for tmp_buff in self.buff[:]:
            target.add_buff(tmp_buff)
            self.target_2.add_buff(tmp_buff)


skill = [Skill_113351_1, Skill_113351_2, Skill_113351_3]
