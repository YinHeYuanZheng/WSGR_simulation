# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 追赶者改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
"""反潜护航(3级)：降低敌方所有潜艇单位的命中值8点，回避值5点（多个单位携带此技能不重复生效）。
"""
#todo 重复技能不生效


class Skill_110241(Skill):
    def __init__(self, master):
        # 降低敌方所有潜艇单位的命中值8点，回避值5点（多个单位携带此技能不重复生效）。
        super().__init__(master)
        self.master = master
        self.target = TypeTarget(side=0, shiptype=('SS', 'SC'))
        self.buff = [
            StatusBuff(
                name='accuracy',
                phase=(AllPhase, ),
                value=-8,
                bias_or_weight=0
            ),
            StatusBuff(
                name='evasion',
                phase=(AllPhase, ),
                value=-5,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return True


skill = [Skill_110241]
