# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 密苏里改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自身30%暴击伤害，开幕导弹攻击敌方的导弹必定有一枚导弹命中且暴击；
炮击战时，降低自身5%的火力值。"""


class Skill_112091_1(Skill):
    """增加自身30%暴击伤害，炮击战时，降低自身5%的火力值。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=ShellingPhase,
                value=-0.05,
                bias_or_weight=1
            )
        ]


class Skill_112091_2(Skill):
    """开幕导弹攻击敌方的导弹必定有一枚导弹命中且暴击"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(
            side=1,
            target=SelfTarget(master),
            equiptype=Missile
        )
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='must_hit',
                phase=FirstMissilePhase
            ),
            SpecialBuff(
                timer=timer,
                name='must_crit',
                phase=FirstMissilePhase
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        missile = np.random.choice(target)  # 任意选择一枚
        for tmp_buff in self.buff[:]:
            tmp_buff = copy.copy(tmp_buff)
            missile.add_buff(tmp_buff)


skill = [Skill_112091_1, Skill_112091_2]
