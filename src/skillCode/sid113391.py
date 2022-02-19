# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 帝国改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_113391(Skill):
    """增加开幕和炮击战阶段伤害20%。"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                name='',  # todo 终伤倍率
                phase=(AirPhase,),  # todo 还有炮击战
                value=0.2,
                bias_or_weight=2
            )
        ]




skill = [Skill_113391]
