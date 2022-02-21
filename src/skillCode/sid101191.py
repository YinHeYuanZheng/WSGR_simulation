# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 皇家方舟-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_101191(Skill):
    """精准打击(3级)：皇家方舟攻击命中的敌人：回避降低30，被暴击率提升25%。"""
    # todo 目标检索
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [StatusBuff(
            name='evasion',
            phase=(AllPhase, ),
            value=30,
            bias_or_weight=0
        ), CoeffBuff(
            name='be_crit',
            phase=(AllPhase, ),
            value=0.25,
            bias_or_weight=2
        )
        ]

    def is_active(self, friend, enemy):

        return True


class Request_1(ATKRequest):
    def __bool__(self):

        pass


skill = [Skill_101191]
