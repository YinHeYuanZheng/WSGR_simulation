# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 鹦鹉螺改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身耐久值增加3点，回避值增加15点。
自身优先攻击敌方驱逐舰，攻击驱逐时暴击率提高20%。
敌方要塞、机场、港口火力值和命中值降低50%，受到的伤害提高50%。"""


class Skill_113662_1(CommonSkill):
    """自身耐久值增加3点，回避值增加15点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='health',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_113662_2(Skill):
    """自身优先攻击敌方驱逐舰，攻击驱逐时暴击率提高20%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=AllPhase,
                target=TypeTarget(side=0, shiptype=DD),
                ordered=False
            ),
            AtkBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, DD)


class Skill_113662_3(Skill):
    """敌方要塞、机场、港口火力值和命中值降低50%，受到的伤害提高50%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=(Fortness, Airfield, Port))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=-0.5,
                bias_or_weight=1
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=0.5
            )
        ]


name = '两栖奇袭'
skill = [Skill_113662_1, Skill_113662_2, Skill_113662_3]
