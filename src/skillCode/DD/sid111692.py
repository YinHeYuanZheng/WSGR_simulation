# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 丹阳改-祥瑞

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""旗舰不为自身时，自身的幸运值按一定百分比转为旗舰的火力值(16%)点、对空值(30%)点和回避值(30%)点。
旗舰为自身时，增加除自身外全队的回避值10点和对空值15点。"""


class Skill_111692_1(Skill):
    """旗舰不为自身时，自身的幸运值按一定百分比转为旗舰的火力值(16%)点、对空值(30%)点和回避值(30%)点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = LocTarget(side=1, loc=[1])
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=.16,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=.3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=.3,
                bias_or_weight=0
            ),
        ]
        
    def activate(self, friend, enemy):
        luck = self.master.get_final_status('luck')
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= luck
                tmp_target.add_buff(tmp_buff)
    
    def is_active(self, friend, enemy):
        return self.master.loc != 1


class Skill_111692_2(Skill):
    """旗舰为自身时，增加除自身外全队的回避值10点和对空值15点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = LocTarget(side=1, loc=[2, 3, 4, 5, 6])
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1
    

name = '祥瑞'
skill = [Skill_111692_1, Skill_111692_2]
