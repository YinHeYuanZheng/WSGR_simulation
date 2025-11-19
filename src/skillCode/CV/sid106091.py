# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 香格里拉-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""根据战斗点距离起始点的位置提升自身战斗力，离初始点越远战斗力越高，
每层提高自身9%舰载机威力和命中率(演习、战役、决战、立体强袭、模拟演习为满层5层)。
当队伍中存在大黄蜂时，自身和大黄蜂暴击伤害提高50%。"""


class Skill_106091_1(Skill):
    """根据战斗点距离起始点的位置提升自身战斗力，离初始点越远战斗力越高，
    每层提高自身9%舰载机威力和命中率(演习、战役、决战、立体强袭、模拟演习为满层5层)。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master=master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.09,
                bias_or_weight=2,
            ),
            CoeffBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=0.09,
                bias_or_weight=0,
            )
        ]

    def activate(self, friend, enemy):
        buff_mul = self.timer.get_dist()
        for tmp_buff in self.buff[:]:
            tmp_buff = copy.copy(tmp_buff)
            tmp_buff.value *= buff_mul
            self.master.add_buff(tmp_buff)


class Skill_106091_2(Skill):
    """当队伍中存在大黄蜂时，自身和大黄蜂暴击伤害提高50%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master=master)
        self.target_2 = None
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.5,
                bias_or_weight=1
            )
        ]

    def is_active(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        for tmp_ship in friend:
            # 大黄蜂cid = 10031/11031
            if tmp_ship.cid == '10031' or tmp_ship.cid == '11031':
                self.target_2 = tmp_ship
                return True
        return False

    def activate(self, friend, enemy):
        if self.target_2 is None:
            return
        tmp_target = self.target.get_target(friend, enemy)[0]
        for tmp_buff in self.buff[:]:
            buff_1 = copy.copy(tmp_buff)
            tmp_target.add_buff(buff_1)
            buff_2 = copy.copy(tmp_buff)
            self.target_2.add_buff(buff_2)


name = '香格里拉'
skill = [Skill_106091_1, Skill_106091_2]