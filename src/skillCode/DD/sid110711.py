# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 电改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import MagicAtk

"""炮击战时35%概率发动，无视目标装甲对目标造成目标当前耐久值50%伤害（上限200点），
该次攻击必定命中（该技能大破状态不能发动）。"""


class Skill_110711(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialAtkBuff(
                timer=timer,
                phase=ShellingPhase,
                rate=0.35,
                atk_type=MagicAtk_110711,
                undamaged=True
            )
        ]


class MagicAtk_110711(MagicAtk):
    def formula(self):
        damage = np.ceil(self.target.status['health'] * 0.5)
        return min(damage, 200)


name = '无意撞击'
skill = [Skill_110711]
