# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 塔什干

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""高速规避(3级)：增加4点自身航速，增加25点回避值。
"""


class Skill_111921(CommonSkill):
    """增加4点自身航速，增加25点回避值。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CommonBuff(
                timer=timer,
                name='speed',
                phase=AllPhase,
                value=4,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            )
        ]


name = '高速规避'
skill = [Skill_111921]
