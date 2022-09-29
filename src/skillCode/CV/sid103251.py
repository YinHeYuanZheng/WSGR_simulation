# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 列克星敦(cv-16)-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import AirAtk

"""蓝色幽灵(3级)：增加自身所携带轰炸机15%的威力，
受到航空攻击时有25%概率免疫该次伤害。"""


class Skill_103251_1(Skill):
    """增加自身所携带轰炸机15%的威力"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_bomb_atk_buff',
                phase=(AirPhase,),
                value=0.15,
                bias_or_weight=2)
        ]


class Skill_103251_2(Skill):
    """受到航空攻击时有25%概率免疫该次伤害"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-1,
                atk_request=[BuffRequest_1],
                rate=0.25
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, AirAtk)


name = '蓝色幽灵'
skill = [Skill_103251_1, Skill_103251_2]
