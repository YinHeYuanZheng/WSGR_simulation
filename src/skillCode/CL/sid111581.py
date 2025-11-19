# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 圣胡安改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队轻巡、驱逐攻击时增加其自身20%对空值的火力值，U国舰船获得双倍效果。"""


class Skill_111581_1(Skill):
    """全队轻巡、驱逐攻击时增加其自身20%对空值的火力值，U国舰船获得双倍效果。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(CL, DD))
        self.buff = [
            AtkHitBuff(
                timer=timer,
                name='give_atk',
                phase=AllPhase,
                buff=[
                    AntiairBasedFire(
                        timer=timer,
                        name='fire',
                        phase=AllPhase,
                        value=0.2,
                        bias_or_weight=0
                    )
                ],
                side=1
            )
        ]


class AntiairBasedFire(DuringAtkBuff):
    """增加自身20%对空值的火力值，U国舰船获得双倍效果"""
    def change_value(self, *args, **kwargs):
        if self.master.status['country'] == 'U':
            self.value = 0.4 * self.master.get_final_status('antiair')
        else:
            self.value = 0.2 * self.master.get_final_status('antiair')


name = 'DP炮齐射'
skill = [Skill_111581_1]
