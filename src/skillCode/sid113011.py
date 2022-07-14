# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 马汉

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""航母援护(3级)：随机增加编队内两艘航空母舰的闪避值12点，雷击战时有40%概率造成30点额外固定伤害
"""


class Skill_113011_1(Skill):
    """随机增加编队内两艘航空母舰的闪避值12点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(master, CV)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        if len(target) > 2:
            target = np.random.choice(target, 2, replace=False)
        for tmp_target in target:
            tmp_buff = copy.copy(self.buff[0])
            tmp_target.add_buff(tmp_buff)


class Skill_113011_2(Skill):
    """雷击战时有40%概率造成30点额外固定伤害"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='extra_damage',
                phase=TorpedoPhase,
                value=20,
                bias_or_weight=0,
                rate=0.4
            )
        ]


name = "航母援护"
skill = [Skill_113011_1, Skill_113011_2]
