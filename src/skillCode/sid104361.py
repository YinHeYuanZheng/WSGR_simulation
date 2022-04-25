# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 十三号战舰

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""队伍内每有一个航速大于等于 27 的单位时都会增加自身 3 点火力值。

增加队伍内全体战列 7 点火力值、战巡（不含自身）7% 暴击率，
当其作为旗舰时，对J国舰船效果双倍。"""

class Skill_104361_1(Skill):
    """队伍内每有一个航速大于等于 27 的单位时都会增加自身 3 点火力值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.buff=[
            StatusBuff(timer=timer,
                name="fire",
                phase=AllPhase,
                value=0,
                bias_or_weight=0,
            )
        ]
    def activate(self, friend, enemy):
        buff = copy.copy(self.buff[0])
        #火力 buff 初值为 0 ，一个航速 >= 27 的单位 + 3
        for ship in friend:
            ship.get_final_status(name="speed") >= 27
            buff.value += 3
        self.master.add_buff(buff)
class Skill_104361_2(Skill):
    """增加队伍内全体战列 7 点火力值"""
    """当其作为旗舰时，对 J 国舰船效果双倍"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        #target 在 activate 中已实现
        self.buff=[
            StatusBuff(timer=timer,
                name="fire",
                phase=AllPhase,
                value=7,
                bias_or_weight=0
            )
        ]
    def activate(self, friend, enemy):
        all_bb = TypeTarget(side=1,shiptype=BB).get_target(friend,enemy)
        for bb in all_bb:
            this_buff = copy.copy(self.buff[0])
            if(bb.status['country'] == 'J' and self.master.loc == 1):
                this_buff.value *= 2
            bb.add_buff(this_buff)
class Skill_104361_3(Skill):
    """战巡（不含自身）7% 暴击率"""
    """当其作为旗舰时，对 J 国舰船效果双倍"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        #target 在 activate 中已实现
        self.buff=[
            CoeffBuff(timer=timer,
                name="crit",
                phase=AllPhase,
                value=0.07,
                bias_or_weight=0
            )
        ]
    def activate(self, friend, enemy):
        all_bc = TypeTarget(side=1,shiptype=BC).get_target(friend,enemy)
        all_target = []
        #筛选出不是自身的 bc
        for bc in all_bc:
            if(bc != self.master):
                all_target.append(bc)
        for target in all_target:
            this_buff = copy.copy(self.buff[0])
            if(self.master.loc == 1 and target.status["country"] == 'J'):
                this_buff.value *= 2
            target.add_buff(this_buff)

skill = [Skill_104361_1,Skill_104361_2,Skill_104361_3]