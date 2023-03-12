# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 勃艮第-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""炮击战阶段自身攻击时提升敌方50%火力值的额外伤害,被自身命中过的敌方攻击时降低50%的火力值。"""


class Skill_105471_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FireExtraDamage(
                timer=timer,
                name='extra_damage',
                phase=AllPhase,
                value=0.5,
                bias_or_weight=0
            ),
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=ShellingPhase,
                buff=[
                    StatusBuff(
                        timer=timer,
                        name='fire',
                        phase=ShellingPhase,
                        value=-0.5,
                        bias_or_weight=1
                    )
                ],
                side=0
            )
        ]


class FireExtraDamage(AtkBuff):
    def change_value(self, *args, **kwargs):
        try:
            atk = kwargs['atk']
        except:
            atk = args[0]
        self.value = np.ceil(atk.target.get_final_status('fire') * 0.5)


name = '主炮突刺'
skill = [Skill_105471_1]
