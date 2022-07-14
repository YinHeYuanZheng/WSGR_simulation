# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 机灵

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""海峡勇者(3级)：增加自身索敌值15点，火力值15点。鱼雷战阶段命中对应位置敌人时有50%几率造成额外25%伤害。
"""


class Skill_111851_1(CommonSkill):
    """增加自身索敌值15点，火力值15点。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CommonBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_111851_2(Skill):
    """鱼雷战阶段命中对应位置敌人时有50%几率造成额外25%伤害。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.3,
                atk_request=[ATKRequest_1]
            )
        ]


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.target.loc == self.atk.atk_body.loc


name = '海峡勇者'
skill = [Skill_111851_1, Skill_111851_2]
