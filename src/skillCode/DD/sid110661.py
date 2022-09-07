# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 初雪改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import SpecialAtk

"""自身火力值增加 10 点，鱼雷值和回避减少 5 点；
炮击战时 30% 概率对敌方水上单位(优先攻击航母)触发特殊攻击，
造成火力值 100% 的伤害且必定命中。(大破无法发动)
"""


class Skill_110661_1(CommonSkill):
    """自身火力值增加 10 点，鱼雷值和回避减少 5 点；"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=-5,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-5,
                bias_or_weight=0
            )
        ]


class Skill_110661_2(Skill):
    """炮击战时 30% 概率对敌方水上单位(优先攻击航母)触发特殊攻击，
    造成火力值 100% 的伤害且必定命中。(大破无法发动)"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialAtkBuff(
                timer=timer,
                phase=ShellingPhase,
                rate=.3,
                during_buff=[
                    PriorTargetBuff(
                        timer=timer,
                        name='prior_type_target',
                        phase=ShellingPhase,
                        target=TypeTarget(side=0, shiptype=CV),
                        ordered=False
                    )
                ],
                atk_type=SpecialAtk_1,
                undamaged=True
            )
        ]


class SpecialAtk_1(SpecialAtk):
    def formula(self):
        return np.ceil(self.atk_body.get_final_status('fire'))


name = '零距炮击'
skill = [Skill_110661_1, Skill_110661_2]
