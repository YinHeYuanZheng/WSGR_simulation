# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 俾斯麦-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身增加20点火力值、装甲值和命中值，攻击战巡时造成两倍伤害。
炮击战阶段100%概率发动，攻击对方舰队旗舰并增加40%护甲穿透和50点额外伤害且必定命中。
当队伍中存在重巡时，自身可免疫1次伤害。"""


class Skill_110061_1(CommonSkill):
    """自身增加20点火力值、装甲值和命中值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
        ]


class Skill_110061_2(Skill):
    """炮击战阶段100%概率发动，攻击对方舰队旗舰并增加40%护甲穿透和50点额外伤害且必定命中。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialAtkBuff(
                timer=timer,
                phase=ShellingPhase,
                rate=1,
                during_buff=[
                    CoeffBuff(
                        timer=timer,
                        name='pierce_coef',
                        phase=ShellingPhase,
                        value=0.4,
                        bias_or_weight=0
                    ),
                    CoeffBuff(
                        timer=timer,
                        name='extra_damage',
                        phase=ShellingPhase,
                        value=50,
                        bias_or_weight=0
                    )
                ],
                target=LocTarget(side=0, loc=[1]),
                coef={'must_hit': True}
            )
        ]


class Skill_110061_3(Skill):
    """当队伍中存在重巡时，首轮炮击阶段免疫受到的第一次攻击。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            DamageShield(
                timer=timer,
                phase=AllPhase,
            )
        ]

    def is_active(self, friend, enemy):
        count = len(TypeTarget(side=1, shiptype=CA).get_target(friend, enemy))
        return count


name = '旗舰杀手'
skill = [Skill_110061_1, Skill_110061_2, Skill_110061_3]
