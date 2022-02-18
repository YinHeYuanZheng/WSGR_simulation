# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 萨拉托加改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_110231(Skill):
    """罗宾(3级)：队伍中每1艘萨拉托加以外的航空母舰、轻型航空母舰、装甲航母，都会为萨拉托加增加7%的舰载机威力。
    E国翻倍"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        _target = TypeTarget(side=1,shiptype=('CV', 'CVL', 'AV')).get_target(self.friend, self.enemy)
        number = 0
        for tar in _target:
            if tar.status.country == 'E':
                number += 0.14
            else:
                number += 0.07
        self.buff = [
            CoeffBuff(
                name='air_atk_buff',
                phase=('AirPhase', ),
                value=number,
                bias_or_weight=2
            )
        ]

    def is_active(self, friend, enemy):
        return True


skill = [Skill_110231]