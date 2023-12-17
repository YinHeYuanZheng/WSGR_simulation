# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 亚尔古水手-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""征战四海(3级)：全阶段损失自身总生命值的30%血量后本场战斗获得一次100%的减伤（每次出击限发动一次）。
炮击战阶段我方每命中敌方单位一次，都会提升亚尔古水手5点火力值。"""


class Skill_104201_1(Skill):
    """全阶段损失自身总生命值的30%血量后本场战斗获得一次100%的减伤（每次出击限发动一次）。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialShield(
                timer=timer,
                phase=AllPhase,
            )
        ]

    def activate(self, friend, enemy):
        # 每次出击限发动一次, 所以不使用copy, 可以在整次出击保持exhaust值
        self.master.add_buff(self.buff[0])


class SpecialShield(DamageShield):
    def is_active(self, *args, **kwargs):
        lost_health_rate = self.master.status['health'] / \
                           self.master.status['standard_health']
        if lost_health_rate >= 0.3 and \
                self.master.got_damage > 0 and \
                self.exhaust > 0:
            self.exhaust -= 1
            return True
        else:
            return False


class Skill_104201_2(Skill):
    """炮击战阶段我方每命中敌方单位一次，都会提升亚尔古水手5点火力值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            SpecialAtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=ShellingPhase,
                buff=[
                    StatusBuff(
                        timer=timer,
                        name='fire',
                        phase=AllPhase,
                        value=5,
                        bias_or_weight=0
                    )
                ],
                target=master
            )
        ]


class SpecialAtkHitBuff(AtkHitBuff):
    def __init__(self, timer, name, phase, buff, target,
                 side=1, atk_request=None, bias_or_weight=3, rate=1):
        super().__init__(timer, name, phase, buff,
                         side, atk_request, bias_or_weight, rate)
        self.target = target

    def activate(self, atk, *args, **kwargs):
        buff0 = copy.copy(self.buff[0])
        self.target.add_buff(buff0)


name = '征战四海'
skill = [Skill_104201_1, Skill_104201_2]
