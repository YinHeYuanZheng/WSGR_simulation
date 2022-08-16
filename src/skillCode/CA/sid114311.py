# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 什罗普郡-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身每次攻击都会使我方任意一角色获得免疫一次攻击的效果，
战斗全阶段每受到一次攻击都会使我方任意一角色增加15%暴击伤害。"""


class Skill_114311(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff_All(
                timer=timer,
                name='give_atk',
                phase=AllPhase,
                buff=[
                    SpecialBuff(
                        timer=timer,
                        name='shield',
                        phase=AllPhase,
                        exhaust=1
                    )
                ],
                side=1
            ),
            AtkHitBuff_All(
                timer=timer,
                name='get_atk',
                phase=AllPhase,
                buff=[
                    CoeffBuff(
                        timer=timer,
                        name='crit_coef',
                        phase=AllPhase,
                        value=0.15,
                        bias_or_weight=0
                    )
                ],
                side=1
            )
        ]


class AtkHitBuff_All(AtkHitBuff):
    def activate(self, atk, *args, **kwargs):
        target_list = [ship for ship in self.master.master.ship if ship.damaged < 4]
        target = np.random.choice(target_list)
        buff = copy.copy(self.buff[0])
        target.add_buff(buff)


name = '红色蔷薇'
skill = [Skill_114311]
