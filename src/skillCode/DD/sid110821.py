# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 萤火虫改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import MagicAtk

"""炮击战时40%概率发动，无视目标装甲对目标造成自身装甲80%的固定伤害，该次攻击必定命中。"""


class Skill_110821(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialAtkBuff(
                timer=timer,
                phase=ShellingPhase,
                rate=0.4,
                atk_type=MagicAtk_110821
            )
        ]


class MagicAtk_110821(MagicAtk):
    def formula(self):
        return np.ceil(self.atk_body.get_final_status('armor') * 0.8)


name = '无畏撞击'
skill = [Skill_110821]
