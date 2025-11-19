# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 萤火虫改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""炮击战时40%概率发动，无视目标装甲对目标造成自身装甲80%的固定伤害，该次攻击必定命中。"""


class Skill_110821(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialAtkBuff_110821(
                timer=timer,
                phase=ShellingPhase,
                rate=0.4,
                coef={'must_hit': True},
            )
        ]


class SpecialAtkBuff_110821(SpecialAtkBuff):
    def active_start(self, atk: ATK, enemy, *args, **kwargs):
        def formula(cls):
            """造成自身装甲80%的固定伤害"""
            return np.ceil(cls.atk_body.get_final_status('armor') * 0.8)

        assert self.master is not None
        self.add_during_buff()  # 攻击时效果

        from types import MethodType
        atk.formula = MethodType(formula, atk)  # 修改伤害公式
        atk.set_coef(self.coef)  # 更新参数
        yield atk

        self.remove_during_buff()  # 去除攻击时效果
        self.add_end_buff()  # 攻击结束效果


name = '无畏撞击'
skill = [Skill_110821]
