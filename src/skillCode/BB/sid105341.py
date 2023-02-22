# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 24型-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身携带装备的命中值的160%视为火力值，40%视为装甲值。
自身为旗舰且索敌成功后，首轮炮击阶段自身无法攻击，
当我方舰船普通攻击命中敌方时，会对可以攻击的该敌方进行一次自身75%伤害的特殊攻击。
首轮炮击阶段自身无视战损"""


class Skill_105341_1(CommonSkill):
    """自身携带装备的命中值的160%视为火力值，40%视为装甲值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=1.6,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=0.4,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        e_accuracy = self.master.get_equip_status('accuracy')
        for tmp_buff in self.buff[:]:
            tmp_buff = copy.copy(tmp_buff)
            tmp_buff.value *= e_accuracy
            self.master.add_buff(tmp_buff)


class Skill_105341_2(Skill):
    """自身为旗舰且索敌成功后，首轮炮击阶段自身无法攻击，
    当我方舰船普通攻击命中敌方时，会对可以攻击的该敌方进行一次自身75%伤害的特殊攻击。
    首轮炮击阶段自身无视战损"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name='not_act_phase',
                phase=FirstShellingPhase
            ),
            ChaseAtkBuff(
                timer=timer,
                phase=FirstShellingPhase,
                coef={'final_damage_buff': -0.25}
            ),
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=FirstShellingPhase
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1 and \
               self.master.get_recon_flag()


name = '旋转木马'
skill = [Skill_105341_1, Skill_105341_2]
