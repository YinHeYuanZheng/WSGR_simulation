# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 诺福克改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队驱逐增加5点鱼雷值和回避值，U国驱逐额外提升5点鱼雷值和回避值。
自身攻击潜艇时命中率提高20%，降低敌方潜艇15点命中值，敌方随机一艘潜艇在先制鱼雷阶段无法行动。"""


class Skill_114961_1(Skill):
    """全队驱逐增加5点鱼雷值和回避值，U国驱逐额外提升5点鱼雷值和回避值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=DD)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                if tmp_target.status['country'] == 'U':
                    tmp_buff.value *= 2
                tmp_target.add_buff(tmp_buff)


class Skill_114961_2(Skill):
    """自身攻击潜艇时命中率提高20%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0,
                atk_request=[ATKRequest_1]
            )
        ]


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, SS)


class Skill_114961_3(Skill):
    """降低敌方潜艇15点命中值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=SS)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-15,
                bias_or_weight=0
            ),
        ]


class Skill_114961_4(Skill):
    """敌方随机一艘潜艇在先制鱼雷阶段无法行动。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = RandomTypeTarget(side=0, shiptype=SS)
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name='not_act_phase',
                phase=FirstTorpedoPhase
            )
        ]


name = '新锐战力'
skill = [Skill_114961_1, Skill_114961_2, Skill_114961_3, Skill_114961_4]
