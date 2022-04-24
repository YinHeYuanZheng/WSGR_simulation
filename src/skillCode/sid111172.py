# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 大凤改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_111172(Skill):
    """队伍中该舰下方位置的3艘航母（轻航，正规航母，装甲航母）增加回避6点
    并且炮击战可进行二次攻击，但二次攻击的伤害减低50%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=3,
            direction='down',
            expand=True,
            shiptype=(CVL, CV, AV)
        )

        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=(AllPhase,),
                value=6,
                bias_or_weight=0
            ),
            ActPhaseBuff(
                timer=timer,
                name='act_phase',
                phase=SecondShellingPhase,
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=SecondShellingPhase,
                value=-0.5,
            )
        ]


skill = [Skill_111172]
