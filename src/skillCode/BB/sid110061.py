# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 俾斯麦-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""炮击战阶段50%概率发动,攻击对方舰队旗舰并增加20%护甲穿透，增加30点额外伤害且必定命中。
当队伍中存在重巡时，首轮炮击阶段免疫受到的第一次攻击。"""


class Skill_110061_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialAtkBuff(
                timer=timer,
                phase=ShellingPhase,
                rate=0.5,
                during_buff=[
                    CoeffBuff(
                        timer=timer,
                        name='pierce_coef',
                        phase=ShellingPhase,
                        value=0.2,
                        bias_or_weight=0
                    ),
                    CoeffBuff(
                        timer=timer,
                        name='extra_damage',
                        phase=ShellingPhase,
                        value=30,
                        bias_or_weight=0
                    )
                ],
                target=LocTarget(side=0, loc=[1]),
                coef={'must_hit': True}
            )
        ]

    # def is_active(self, friend, enemy):
    #     return self.master.loc == 1


class Skill_110061_2(Skill):
    """当队伍中存在重巡时，首轮炮击阶段免疫受到的第一次攻击。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='shield',
                phase=FirstShellingPhase,
                exhaust=1)
        ]

    def is_active(self, friend, enemy):
        count = len(TypeTarget(side=1, shiptype=CA).get_target(friend, enemy))
        return count


name = '旗舰杀手'
skill = [Skill_110061_1, Skill_110061_2]
