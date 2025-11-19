# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 纽波特纽斯-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""超额(3级)：炮击战阶段有35%概率造成敌方总血量20%的额外伤害。
该技能触发一次之后，纽波特纽斯火力降低10%（火力降低不会继承到夜战）。"""


class Skill_103881(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialAtkBuff(
                timer=timer,
                phase=ShellingPhase,
                rate=0.35,
                during_buff=[
                    HealthExtraDamage(
                        timer=timer,
                        name='extra_damage',
                        phase=ShellingPhase,
                        value=0.2,
                        bias_or_weight=0,
                    )
                ],
                end_buff=[
                    StatusBuff(
                        timer=timer,
                        name='fire',
                        phase=DaytimePhase,
                        value=-0.1,
                        bias_or_weight=1
                    )
                ]
            )
        ]


class HealthExtraDamage(AtkBuff):
    def change_value(self, *args, **kwargs):
        try:
            atk = kwargs['atk']
        except:
            atk = args[0]
        self.value = np.ceil(atk.target.status['standard_health'] * 0.2)


name = '超额'
skill = [Skill_103881]
