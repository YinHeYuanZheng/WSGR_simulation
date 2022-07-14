# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 巴夫勒尔

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""新锐装备(3级)：自身在航空战阶段受到伤害减少80%；
鱼雷战阶段额外发射一枚鱼雷，伤害为正常的85%。"""


class Skill_113061(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AirPhase,
                value=-0.8,
            ),
            SpecialBuff_barfleur(
                timer=timer,
                name='multi_torpedo_attack',
                phase=SecondTorpedoPhase,
            )
        ]


class SpecialBuff_barfleur(SpecialBuff):
    """鱼雷战阶段额外发射一枚鱼雷，伤害为正常的85%"""
    def activate(self, *args, **kwargs):
        # 添加一个只生效一次的临时终伤buff，数值为-15%
        buff0 = DuringFinDmgBuff_1(
            timer=self.timer,
            name='final_damage_buff',
            phase=SecondTorpedoPhase,
            value=-0.15,
        )
        self.master.add_buff(buff0)


class DuringFinDmgBuff_1(FinalDamageBuff):
    def is_during_buff(self):
        return True


name = '新锐装备'
skill = [Skill_113061]
