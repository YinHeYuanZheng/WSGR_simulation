# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 奥里斯坎尼-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身火力值和命中值增加15点。
全队埃塞克斯级航母舰载机威力提升10%，队伍中每有1艘埃塞克斯级航母都会再额外提升4%"""


class Skill_106271_1(CommonSkill):
    """自身火力值和命中值增加15点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0,
            ),
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=15,
                bias_or_weight=0,
            ),
        ]


class Skill_106271_2(Skill):
    """全队埃塞克斯级航母舰载机威力提升10%，队伍中每有1艘埃塞克斯级航母都会再额外提升4%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TagTarget(side=1, tag='essex')
        self.buff = [
            CoeffBuff(
                timer=self.timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=2
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        num_essex = len(target)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value += 0.04 * num_essex
                tmp_target.add_buff(tmp_buff)


name = '先行试验'
skill = [Skill_106271_1, Skill_106271_2]
