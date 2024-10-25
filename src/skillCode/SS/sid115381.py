# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 伊-25

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""根据玩家总出征数（上限40000次）增加自身最多12点鱼雷值和回避值。
装备索敌值的2倍视为鱼雷值。"""


class Skill_115381_1(CommonSkill):
    """增加自身最多12点鱼雷值和回避值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]


class Skill_115381_2(CommonSkill):
    """装备索敌值的2倍视为鱼雷值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=2,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        e_recon = self.master.get_equip_status('recon')
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= e_recon
                tmp_target.add_buff(tmp_buff)


name = '大洋巡弋'
skill = []
