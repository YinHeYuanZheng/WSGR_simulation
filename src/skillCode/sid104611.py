# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 无敌

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""单纵阵时增加自身 12% 的暴击率和 15 点装甲值。
梯形阵时首轮炮击提高自身 20% 被攻击概率，
且自身攻击命中后必暴击，暴击伤害提高 50%。
复纵阵时炮击战阶段提升自身 15 点装甲值和 9 点闪避值。
"""

class Skill_104611_1(Skill):
    """单纵阵时增加自身 12% 的暴击率和 15 点装甲值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target=SelfTarget(master)
        self.buff=[
            CoeffBuff(timer=timer,
                name="crit",
                phase=AllPhase,
                value=0.12,
                bias_or_weight=0,
            ),
            StatusBuff(timer=timer,
                name="armor",
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]
    def activate(self, friend, enemy):
        if(self.master.get_form() == 1):
            return super().activate(friend, enemy)
class Skill_104611_2(Skill):
    """梯形阵时首轮炮击提高自身 20% 被攻击概率，且自身攻击命中后必暴击，暴击伤害提高 50%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target=SelfTarget(master)
        self.buff=[
            MagnetBuff(timer=timer,
                phase=FirstShellingPhase,
                rate=0.2,
            ),
            SpecialBuff(timer=timer,
                name="must_crit",
                phase=FirstShellingPhase,
            ),
            AtkBuff(timer=timer,
                name="crit_coef",
                phase=FirstShellingPhase,
                value=0.5,
                bias_or_weight=0,

            )
        ]
    def activate(self, friend, enemy):
        if(self.master.get_form() == 3):
            return super().activate(friend, enemy)
        
class Skill_104611_3(Skill):
    """复纵阵时炮击战阶段提升自身 15 点装甲值和 9 点闪避值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target=SelfTarget(master)
        self.buff=[
            StatusBuff(timer=timer,
                phase=ShellingPhase,
                name="armor",
                value=15,
                bias_or_weight=0
            ),
            StatusBuff(timer=timer,
                name="evasion",
                phase=ShellingPhase,
                value=9,
                bias_or_weight=0
            )
        ]
    def activate(self, friend, enemy):
        if(self.master.get_form() == 2):
            return super().activate(friend, enemy)
skill = [Skill_104611_1,Skill_104611_2,Skill_104611_3]