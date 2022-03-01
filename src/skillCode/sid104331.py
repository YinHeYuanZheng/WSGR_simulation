# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 提康德罗加-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import *
from src.wsgr.equipment import *

"""制空权(3级)：自身受到航母单位攻击时降低20%的伤害（限开幕与炮击战阶段）。
自身和其上方最近的一艘航母，装母，轻母单位在制空权均势，优势，确保时舰载机伤害增加10%。"""


class Skill_104331_1(Skill):
    """自身受到航母单位攻击时降低20%的伤害（限开幕与炮击战阶段）"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=(AirPhase, ShellingPhase),
                value=-0.2,
                bias_or_weight=2,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, AirAtk)


class Skill_104331_2(Skill):
    """自身和其上方最近的一艘航母，装母，轻母单位在制空权均势，优势，确保时舰载机伤害增加10%。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='up',
            master_include=True,
            expand=True,
            shiptype=(CV, AV, CVL)
        )

        self.buff = [
            AtkBuff(
                timer=timer,
                name='air_atk_buff',
                phase=(AllPhase,),
                value=0.1,
                bias_or_weight=2,
                atk_request=[BuffRequest_2]
            )
        ]


class BuffRequest_2(ATKRequest):
    def __bool__(self):
        if self.atk.atk_body.side == 1:
            air_con_flag = self.timer.air_con_flag
        else:
            air_con_flag = 6 - self.timer.air_con_flag
        return air_con_flag <= 3


skill = [Skill_104331_1, Skill_104331_2]
