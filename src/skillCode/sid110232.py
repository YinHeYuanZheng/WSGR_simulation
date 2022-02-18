# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 加贺改-2

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_110231(Skill):
    """此技能在舰队舰船数大于等于4时生效。
    当队伍的平均航速大于加贺自身航速时，提升自身装甲值12点、对空值12点；
    当队伍的平均航速等于加贺自身航速时，两种效果皆生效。"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.buff = [StatusBuff(
            name='armor',
            phase=('AllPhase',),
            value=12,
            bias_or_weight=0,
        ), StatusBuff(
            name='antiair',
            phase=('AllPhase',),
            value=12,
            bias_or_weight=0,
        ), ]

    def is_active(self, friend, enemy):
    # todo 判断航速
        return True


class Skill_110231_1(Skill):
    """此技能在舰队舰船数大于等于4时生效。
    当队伍平均航速小于加贺自身航速时，提升自身轰炸机20%的威力；"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.buff = [CoeffBuff(
            name='air_bomb_atk_buff',
            phase=('AirPhase',),
            value=0.2,
            bias_or_weight=2,
        ), CoeffBuff(
            name='air_atk_buff',
            phase=('AirPhase',),
            value=0.2,
            bias_or_weight=2,
        )]

    def is_active(self, friend, enemy):
        # todo 判断航速
        return True


skill = [Skill_110231,Skill_110231_1]
