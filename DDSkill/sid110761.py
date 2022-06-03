# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# Z21

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""降低敌方全体驱逐舰，轻巡洋舰和重巡洋舰的回避及装甲值各 12 点，当敌方队伍中存在战列舰或战列巡洋舰时，效果减半 """


class Skill_110761_1(Skill):
    """降低敌方全体驱逐舰，轻巡洋舰和重巡洋舰的回避及装甲值各 12 点，当敌方队伍中存在战列舰或战列巡洋舰时，效果减半"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=(DD, CL, CA))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-12,
                bias_or_weight=0
            ),
        ]
    def activate(self, friend, enemy):
        rate = 1
        if(len(TypeTarget(side=0, shiptype=(BB,BC)).get_target(friend, enemy)) != 0):rate = 0.5
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= rate
                tmp_target.add_buff(tmp_buff)
skill = [Skill_110761_1]