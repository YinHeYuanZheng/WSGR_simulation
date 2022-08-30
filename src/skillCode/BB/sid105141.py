# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 近江-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身与相邻上方舰船增加8点火力值和装甲值，如果相邻上方为J国舰船，则该船获得两倍效果。
炮击战阶段50%概率发动，对敌方造成130%伤害。"""


class Skill_105141_1(Skill):
    """自身与相邻上方舰船增加8点火力值和装甲值，如果相邻上方为J国舰船，则该船获得两倍效果。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='up'
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                if tmp_target.status['country'] == 'J':
                    tmp_buff.value *= 2
                tmp_target.add_buff(tmp_buff)

        for tmp_buff in self.buff[:]:
            tmp_buff = copy.copy(tmp_buff)
            self.master.add_buff(tmp_buff)


class Skill_105141_2(Skill):
    """炮击战阶段50%概率发动，对敌方造成130%伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.3,
                rate=0.5
            )
        ]


name = '战列线决战'
skill = [Skill_105141_1, Skill_105141_2]
