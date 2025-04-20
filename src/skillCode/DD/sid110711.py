# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 电改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""炮击战时35%概率发动，无视目标装甲对目标造成目标当前耐久值50%伤害（上限200点），
该次攻击必定命中（该技能大破状态不能发动）。"""


class Skill_110711(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialAtkBuff_110711(
                timer=timer,
                phase=ShellingPhase,
                rate=0.35,
                coef={'must_hit': True},
                undamaged=True
            )
        ]


class SpecialAtkBuff_110711(SpecialAtkBuff):
    def active_start(self, atk: ATK, enemy, *args, **kwargs):
        def formula(cls):
            """造成目标当前耐久值50%伤害（上限200点）"""
            damage = np.ceil(cls.target.status['health'] * 0.5)
            return min(damage, 200.)

        assert self.master is not None
        self.add_during_buff()  # 攻击时效果

        from types import MethodType
        atk.formula = MethodType(formula, atk)  # 修改伤害公式
        atk.set_coef(self.coef)  # 更新参数
        yield atk

        self.remove_during_buff()  # 去除攻击时效果
        self.add_end_buff()  # 攻击结束效果


name = '无意撞击'
skill = [Skill_110711]
