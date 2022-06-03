# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 白雪

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""炮击战时 50% 概率代替队伍中的特型驱逐舰承受攻击并免疫本次伤害。当吹雪为旗舰时，提升其及自身的装甲值 8 点。
"""


class Skill_110651_1(Skill):
    """炮击战时 50% 概率代替队伍中的特型驱逐舰承受攻击并免疫本次伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            TankBuff(
                timer=timer,
                phase=ShellingPhase,
                target=TagTarget(side=1, tag='fubuki'),
                value=-1,
                rate=.5,
            )
        ]
class Skill_110651_2(Skill):
    def __init__(self, timer, master):
        "当吹雪为旗舰时，提升其及自身的装甲值 8 点"
        super().__init__(timer, master)
        self.target = LocTarget(side=1, loc=[self.master.loc, 1])
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=8,
                bias_or_weight=0,
            ),
        ]
    def is_active(self, friend, enemy):
        flag_ship = LocTarget(side=1, loc=[1])[0]
        #11064 是吹雪的 cid
        return flag_ship.cid == '11064'
skill = [Skill_110651_1, Skill_110651_2]