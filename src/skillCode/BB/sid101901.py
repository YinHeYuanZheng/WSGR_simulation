# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 土佐-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队航速低于27节的舰船装甲值和回避值增加6点。
自身相邻舰船射程增加1档，装甲值增加12点。
全队J国舰船火力值增加6点，暴击率提高6%。
当队伍中只有J国舰船时，自身攻击敌方时无视目标100%的装甲值。"""


class Skill_101901_1(Skill):
    """全队航速低于27节的舰船装甲值和回避值增加6点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = StatusTarget(
            side=1,
            status_name='speed',
            fun='lt',
            value=27
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            )
        ]


class Skill_101901_2(Skill):
    """自身相邻舰船射程增加1档，装甲值增加12点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='near'
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='range_buff',
                phase=AllPhase,
                value=1,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
        ]


class Skill_101901_3(Skill):
    """全队J国舰船火力值增加6点，暴击率提高6%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='J')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.06,
                bias_or_weight=0
            )
        ]


class Skill_101901_4(Skill):
    """当队伍中只有J国舰船时，自身攻击敌方时无视目标100%的装甲值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='ignore_armor',
                phase=AllPhase,
                value=-1,
                bias_or_weight=1
            )
        ]

    def is_active(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        for ship in friend:
            if ship.status['country'] != 'J':
                return False
        return True


name = '全炮效力射'
skill = [Skill_101901_1, Skill_101901_2, Skill_101901_3, Skill_101901_4]
