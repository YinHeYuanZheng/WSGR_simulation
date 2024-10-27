# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 亚拉巴马-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身编队左边相邻舰船射程增加1档。全队大型船暴击率提升8%。
当队伍中还存在其她南达科他级舰船(南达科他BB-57、印第安纳BB-58、马萨诸塞BB-59)时，
增加自身和上述舰船火力值和装甲值12点。"""


class Skill_105231_1(Skill):
    """自身编队左边相邻舰船射程增加1档。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='up',
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='range_buff',
                phase=AllPhase,
                value=1,
                bias_or_weight=0
            )
        ]


class Skill_105231_2(Skill):
    """全队大型船暴击率提升8%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=LargeShip)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.08,
                bias_or_weight=0
            )
        ]


class Skill_105231_3(Skill):
    """当队伍中还存在其她南达科他级舰船(南达科他BB-57、印第安纳BB-58、马萨诸塞BB-59)时，
    增加自身和上述舰船火力值和装甲值12点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TagTarget(side=1, tag='south_dakota')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        if self.master in target:
            target.remove(self.master)  # 去除自身
        return len(target)


name = '重炮火力'
skill = [Skill_105231_1, Skill_105231_2, Skill_105231_3]
