# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 维纳斯

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""队伍中驱逐舰数量大于等于3时，增加自身25点鱼雷值；
鱼雷战阶段，命中中型或大型船时有50%概率造成20点额外固定伤害"""


class Skill_111751_1(Skill):
    """队伍中驱逐舰数量大于等于3时，增加自身25点鱼雷值；"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            ),
        ]
    
    def is_active(self, friend, enemy):
        count = len(TypeTarget(side=1, shiptype=DD).get_target(friend, enemy))
        return count >= 3


class Skill_111751_2(Skill):
    """鱼雷战阶段，命中中型或大型船时有50%概率造成20点额外固定伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='extra_damage',
                phase=SecondTorpedoPhase,
                value=20,
                bias_or_weight=0,
                atk_request=[ATK_Request1],
                rate=.5
            )
        ]


class ATK_Request1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (LargeShip, MidShip))


name = '编队鱼雷战'
skill = [Skill_111751_1, Skill_111751_2]
