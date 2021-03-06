# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 梅肯-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""天狮星(3级)：射程变为长，炮击战阶段伤害增加25%，如果命中的是中、小型船，伤害增加25%。"""


class Skill_104381_1(CommonSkill):
    """射程变为长"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='range',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            )
        ]


class Skill_104381_2(Skill):
    """炮击战阶段伤害增加25%，如果命中的是中、小型船，伤害增加25%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.25
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.25,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (MidShip, SmallShip))


name = '天狮星'
skill = [Skill_104381_1, Skill_104381_2]
