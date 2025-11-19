# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 捷尔任斯基改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身装备的导弹装备火力值增加12点。
根据战斗点距离起始点的位置提升全队舰船战斗力，离初始点越远提升越多，
每层火力、鱼雷、命中、回避增加3点（演习、战役、决战、立体强袭、模拟演习为满层5层）。"""


class Skill_114301_1(CommonSkill):
    """自身装备的导弹装备火力值增加12点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(side=1,
                                  target=SelfTarget(master),
                                  equiptype=Missile)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]


class Skill_114301_2(Skill):
    """根据战斗点距离起始点的位置提升全队舰船战斗力，离初始点越远提升越多，
    每层火力、鱼雷、命中、回避增加3点（演习、战役、决战、立体强袭、模拟演习为满层5层）。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
        ]

    def activate(self, friend, enemy):
        buff_mul = self.timer.get_dist()
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= buff_mul
                tmp_target.add_buff(tmp_buff)


name = '德维纳波涛'
skill = [Skill_114301_1, Skill_114301_2]
