# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 塔林-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""坚持奋战(3级)：降低自身4点闪避值，增加自身15点火力值；
战斗中自身被命中过一次之后增加自身20%暴击率、20点火力值，20点装甲值（限昼战阶段）。"""


class Skill_114561_1(CommonSkill):
    """坚持奋战(3级)：降低自身4点闪避值，增加自身15点火力值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-4,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_114561_2(Skill):
    """战斗中自身被命中过一次之后增加自身20%暴击率、20点火力值，20点装甲值（限昼战阶段）"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            OnceAtkHitBuff(
                timer=timer,
                name='atk_be_hit',
                phase=AllPhase,
                buff=[
                    CoeffBuff(
                        timer=timer,
                        name='crit',
                        phase=DaytimePhase,
                        value=0.2,
                        bias_or_weight=0
                    ),
                    StatusBuff(
                        timer=timer,
                        name='fire',
                        phase=DaytimePhase,
                        value=20,
                        bias_or_weight=0
                    ),
                    StatusBuff(
                        timer=timer,
                        name='armor',
                        phase=DaytimePhase,
                        value=20,
                        bias_or_weight=0
                    )
                ],
                side=1
            )
        ]


class OnceAtkHitBuff(AtkHitBuff):
    def __init__(self, timer, name, phase, buff, side,
                 atk_request=None, bias_or_weight=3, rate=1):
        super().__init__(timer, name, phase, buff, side,
                         atk_request, bias_or_weight, rate)
        self.exhaust = 1

    def is_active(self, atk, *args, **kwargs):
        if self.exhaust == 0:
            return False

        if self.atk_request is None:
            return isinstance(self.timer.phase, self.phase) and \
                   self.rate_verify()

        return isinstance(self.timer.phase, self.phase) and \
               bool(self.atk_request[0](self.timer, atk)) and \
               self.rate_verify()

    def activate(self, atk, *args, **kwargs):
        if (self.name == 'atk_hit' and self.side == 1) or \
                (self.name == 'atk_be_hit' and self.side == 0):
            target = atk.atk_body
        else:
            target = atk.target

        for tmp_buff in self.buff[:]:
            tmp_buff = copy.copy(tmp_buff)
            target.add_buff(tmp_buff)

        self.exhaust -= 1


skill = [Skill_114561_1,Skill_114561_2]
