# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 让巴尔-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""
Lv.1: 降低自身30%被攻击概率。
Lv.2: 战斗中随机选择我方任意一艘自身以外的中、大型船，获得其技能（战斗外增加属性效果及演习内战斗不生效）。
Lv.3:如果这个技能包含有概率发动的效果，则变为100%发动。
"""


class Skill_102991_1(Skill):
    """降低自身30%被攻击概率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            UnMagnetBuff(
                timer=timer,
                phase=AllPhase,
                rate=0.3
            )
        ]


class Skill_102991_2(PrepSkill):
    """战斗中随机选择我方任意一艘自身以外的中、大型船，获得其技能
    如果这个技能包含有概率发动的效果，则变为100%发动。"""
    def activate(self, friend, enemy):
        # 自身以外的中、大型船
        mid_large = TypeTarget(
            side=1,
            shiptype=(MidShip, LargeShip)
        ).get_target(friend, enemy)
        if self.master in mid_large:
            mid_large.remove(self.master)

        target = np.random.choice(mid_large)
        _skill = target.get_raw_skill()  # 获得其技能
        for skillClass in _skill:
            tmp_skill = skillClass(self.timer, self.master)
            tmp_skill.change_rate(1)  # 变为100%发动
            if tmp_skill.is_active(friend, enemy):
                tmp_skill.activate(friend, enemy)


name = '旁观者'
skill = [Skill_102991_1, Skill_102991_2]
