# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 高波改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身被攻击概率提升30%。中破时可免疫1次伤害。
鱼雷战阶段，攻击力不会因为自身的耐久损伤而降低，且必定暴击，可额外发射2枚鱼雷，
攻击命中的敌方单位无法行动，被暴击率提高25%。"""


class Skill_112581_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MagnetBuff(
                timer=timer,
                phase=AllPhase,
                rate=0.3
            ),
            Shield_112581(
                timer=timer,
                phase=AllPhase,
            ),
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=SecondTorpedoPhase,
            ),
            SpecialBuff(
                timer=timer,
                name='must_crit',
                phase=SecondTorpedoPhase,
            ),
            MultipleTorpedoAtkBuff(
                timer=timer,
                name='multi_torpedo_attack',
                phase=SecondTorpedoPhase,
                num=2,
                rate=1
            ),
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=SecondTorpedoPhase,
                buff=[
                    ActPhaseBuff(
                        timer=timer,
                        name='not_act_phase',
                        phase=AllPhase
                    ),
                    CoeffBuff(
                        timer=timer,
                        name='be_crit',
                        phase=AllPhase,
                        value=0.25,
                        bias_or_weight=0
                    )
                ],
                side=0
            )
        ]


class Shield_112581(DamageShield):
    def is_active(self, *args, **kwargs):
        if self.master.damaged == 2 and self.exhaust > 0:
            self.exhaust -= 1
            return True
        else:
            return False


name = '塔萨法隆格的幽灵'
skill = [Skill_112581_1]
