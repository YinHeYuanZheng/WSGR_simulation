# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 拉菲

from src.wsgr.formulas import AirAtk
from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""技能效果随技能等级提升而增加
Lv.1: 昼战时攻击力不会因为自身受到的HP损伤而降低
Lv.2: 根据所受到损伤提升暴击率
Lv.3: 中破状态下免疫航空攻击"""


class Skill_111831(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=DaytimePhase,
            ),
            HealthBasedBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=.8,
                bias_or_weight=0,
            ),
            SpecialBuff(
                timer=timer,
                name='shield',
                phase=AllPhase,
                atk_request=[ATKRequest1],
            )
        ]


class HealthBasedBuff(CoeffBuff):
    def change_value(self, *args, **kwargs):
        total_health = self.master.status['standard_health']
        health = self.master.status['health']
        self.value = 0.8 * \
                     (total_health - health) / \
                     (total_health - 1)


class ATKRequest1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, AirAtk) and \
               (self.atk.target.damaged == 2 or self.atk.target.damaged == 3)


name = '不惧神风'
skill = [Skill_111831]
