# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 射水鱼

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""必定优先攻击航母、轻母和装母，
攻击航母类单位(航母、轻母和装母)时，命中值增加10点，且暴击时伤害为习得技能前的1.2倍。"""


class Skill_111951(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=AllPhase,
                target=TypeTarget(side=0, shiptype=(CV, CVL, AV)),
                ordered=False
            ),
            AtkHitBuff(
                timer=timer,
                name='give_atk',
                phase=AllPhase,
                buff=[
                    DuringAtkBuff(
                        timer=timer,
                        name='accuracy',
                        phase=AllPhase,
                        value=10,
                        bias_or_weight=0
                    )
                ],
                side=1,
                atk_request=[BuffRequest_1]
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.2,
                atk_request=[BuffRequest_2]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (CV, CVL, AV))


class BuffRequest_2(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (CV, CVL, AV)) and \
               self.atk.coef['crit_flag']


name = '猎杀潜航'
skill = [Skill_111951]
