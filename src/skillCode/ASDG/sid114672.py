# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 鞍山-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队导驱火力值、装甲值、回避值和对空值增加8点，造成的伤害提高8%，当舰队旗舰为“四大金刚”时，额外再获得2倍效果。
自身编队相邻舰船射程增加1档，如果相邻舰船为C国舰船，则额外增加1档。"""


class Skill_114672_1(Skill):
    """全队导驱火力值、装甲值、回避值和对空值增加8点，造成的伤害提高8%，
    当舰队旗舰为“四大金刚”时，额外再获得2倍效果。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=ASDG)
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
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=.08
            )
        ]

    def activate(self, friend, enemy):
        correctLeaderFlag = False
        if friend.ship[0].status['tag'] == 'PLAN4':
            correctLeaderFlag = True
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                if correctLeaderFlag:
                    tmp_buff.value *= 3
                tmp_target.add_buff(tmp_buff)


class Skill_114672_2(Skill):
    """自身编队相邻舰船射程增加1档，如果相邻舰船为C国舰船，则额外增加1档。"""

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
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                if tmp_target.status['country'] == 'C':
                    tmp_buff.value *= 2
                tmp_target.add_buff(tmp_buff)


name = '四大金刚(联)'
skill = [Skill_114672_1, Skill_114672_2]
