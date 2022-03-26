# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 安德烈亚多里亚-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身幸运值增加15，攻击时最大增加80%幸运值的火力，被攻击时最大增加80%幸运值的回避。"""


class Skill_110131_1(CommonSkill):
    """自身幸运值增加15"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='luck',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_110131_2(Skill):
    """攻击时最大增加80%幸运值的火力，被攻击时最大增加80%幸运值的回避"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            LuckBuff(
                timer=timer,
                name='fire'
            ),
            LuckBuff(
                timer=timer,
                name='evasion'
            )
        ]


class LuckBuff(StatusBuff):
    def __init__(self, timer, name):
        super().__init__(timer=timer,
                         name=name,
                         phase=AllPhase,
                         value=1,
                         bias_or_weight=0)

    def is_active(self, *args, **kwargs):
        self.value = np.ceil(
            (1 - np.random.random()) * 0.8
            * self.master.get_final_status('luck')
        )
        return True


skill = [Skill_110131_1, Skill_110131_2]
