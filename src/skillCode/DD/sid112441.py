# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 灵敏改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""根据玩家总出征数（上限60000次）最多增加自身30点火力值、索敌值、命中值和对空值。
炮击战阶段有30%概率对敌方造成必中攻击，并增加自身50%幸运值的额外伤害。"""


class Skill_112441_1(CommonSkill):
    """根据玩家总出征数（上限60000次）最多增加自身30点火力值、索敌值、命中值和对空值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            ),
        ]


class Skill_112441_2(Skill):
    """炮击战阶段有30%概率对敌方造成必中攻击，并增加自身50%幸运值的额外伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialAtkBuff(
                timer=timer,
                phase=ShellingPhase,
                rate=0.3,
                during_buff=[
                    LuckExtraDamage(
                        timer=timer,
                        name='extra_damage',
                        phase=ShellingPhase,
                        value=0.5,
                        bias_or_weight=0
                    )
                ],
                coef={'must_hit': True}
            )
        ]


class LuckExtraDamage(AtkBuff):
    def change_value(self, *args, **kwargs):
        luck = self.master.status['luck']
        self.value = np.ceil(luck * 0.5)


name = '近卫'
skill = [Skill_112441_1, Skill_112441_2]
