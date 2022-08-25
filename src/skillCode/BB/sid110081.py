# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# BIG SEVEN

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""BIG SEVEN(3级)：炮击战阶段20%概率发动，对2个目标造成116%的伤害，
队伍中每有一艘 BIG SEVEN 舰船(罗德尼、纳尔逊、科罗拉多、马里兰、西弗吉尼亚、鲨、鲞)，
都会增加5%发动概率。"""


class Skill_110081(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MultipleAtkBuff(
                timer=timer,
                name='multi_attack',
                phase=ShellingPhase,
                num=2,
                rate=0.2,
                coef={'final_damage_buff': 0.16}
            )
        ]

    def activate(self, friend, enemy):
        buff_0 = copy.copy(self.buff[0])
        target_big_seven = TagTarget(side=1, tag='big_seven').get_target(friend, enemy)
        buff_0.rate = min(1., buff_0.rate + 0.05 * len(target_big_seven))
        self.master.add_buff(buff_0)


name = 'BIG SEVEN'
skill = [Skill_110081]
