# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 伊吹-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""主力甲巡(3级)：队伍内每有一艘航速≥27节的舰船都会增加自身的4点火力值，上限五艘；
如果航速≥27节的舰船为中、小型船时，每艘额外增加15%暴击率。"""


class Skill_104511(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=4,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        high_speed = [ship for ship in friend.ship
                      if ship.get_final_status('speed') >= 27]  # 获取航速≥27节的舰船
        ms_ship = [ship for ship in high_speed
                   if isinstance(ship, (MidShip, SmallShip))]  # 获取航速≥27节的中、小型船

        buff0 = copy.copy(self.buff[0])
        buff0.value *= min(5, len(high_speed))  # 上限五艘
        self.master.add_buff(buff0)

        buff1 = copy.copy(self.buff[1])
        buff1.value *= min(5, len(ms_ship))  # 上限五艘
        self.master.add_buff(buff1)


skill = [Skill_104511]
