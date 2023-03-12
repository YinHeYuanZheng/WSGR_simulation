# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 卡约•杜伊里奥-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身幸运值提升15。炮击战阶段攻击时增加自身100%幸运值的额外伤害，被攻击时增加自身50%幸运值的装甲值。"""


class Skill_112111_1(CommonSkill):
    """自身幸运值提升15"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='luck',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_112111_2(Skill):
    """炮击战阶段攻击时增加自身100%幸运值的额外伤害，被攻击时增加自身50%幸运值的装甲值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            LuckExtraDamage(
                timer=timer,
                name='extra_damage',
                phase=AllPhase,
                value=1,
                bias_or_weight=0
            ),
            LuckBuff(
                timer=timer,
                name='get_atk',
                phase=AllPhase,
                buff=[
                    DuringAtkBuff(
                        timer=timer,
                        name='armor',
                        phase=AllPhase,
                        value=0.5,
                        bias_or_weight=0
                    )
                ],
                side=1
            ),
        ]


class LuckExtraDamage(CoeffBuff):
    """攻击时增加自身100%幸运值的额外伤害"""
    def change_value(self, *args, **kwargs):
        self.value = np.ceil(self.master.get_final_status('luck'))


class LuckBuff(AtkHitBuff):
    """被攻击时增加自身50%幸运值的装甲值。"""
    def activate(self, atk, *args, **kwargs):
        for tmp_buff in self.buff[:]:
            tmp_buff = copy.copy(tmp_buff)
            tmp_buff.value *= self.master.get_final_status('luck')
            self.master.add_buff(tmp_buff)


name = '幸运之舰'
skill = [Skill_112111_1, Skill_112111_2]
