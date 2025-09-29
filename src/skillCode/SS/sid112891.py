# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# U-81

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身命中值和鱼雷值增加12点，暴击率提高12%。
自身攻击航母、装母、轻母时伤害提高30%，
被自身命中的敌人回避值和装甲值降低12点，被暴击率提高12%。"""


class Skill_112891_1(CommonSkill):
    """自身命中值和鱼雷值增加12点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=12,
                bias_or_weight=0,
            ),
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=12,
                bias_or_weight=0,
            ),
        ]


class Skill_112891_2(Skill):
    """自身暴击率提高12%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.12,
                bias_or_weight=0
            )
        ]


class Skill_112891_3(Skill):
    """自身攻击航母、装母、轻母时伤害提高30%，
    被自身命中的敌人回避值和装甲值降低12点，被暴击率提高12%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=.3,
                atk_request=[ATK_request_1],
            ),
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=AllPhase,
                buff=[
                    StatusBuff(
                        timer=timer,
                        name='evasion',
                        phase=AllPhase,
                        value=-12,
                        bias_or_weight=0
                    ),
                    StatusBuff(
                        timer=timer,
                        name='armor',
                        phase=AllPhase,
                        value=-12,
                        bias_or_weight=0
                    ),
                    CoeffBuff(
                        timer=timer,
                        name='be_crit',
                        phase=AllPhase,
                        value=0.12,
                        bias_or_weight=0
                    )
                ],
                side=0
            ),
        ]


class ATK_request_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (CV, CVL, AV))


name = '狼群猎手'
skill = [Skill_112891_1, Skill_112891_2, Skill_112891_3]
