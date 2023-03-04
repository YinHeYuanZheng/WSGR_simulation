# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 安德烈亚多里亚-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身幸运值提升15，攻击时增加自身80%幸运值的火力值，被攻击时增加自身80%幸运值的回避值。
当队伍中I国船≥3时，全队舰船攻击时增加自身50%幸运值的额外伤害。"""


class Skill_110131_1(CommonSkill):
    """自身幸运值提升15"""
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
    """攻击时增加自身80%幸运值的火力值，被攻击时增加自身80%幸运值的回避值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            LuckBuff(
                timer=timer,
                name='give_atk',
                phase=AllPhase,
                buff=[
                    DuringAtkBuff(
                        timer=timer,
                        name='fire',
                        phase=AllPhase,
                        value=0.8,
                        bias_or_weight=0
                    )
                ],
                side=1
            ),
            LuckBuff(
                timer=timer,
                name='get_atk',
                phase=AllPhase,
                buff=[
                    DuringAtkBuff(
                        timer=timer,
                        name='evasion',
                        phase=AllPhase,
                        value=0.8,
                        bias_or_weight=0
                    )
                ],
                side=1
            ),
        ]


class LuckBuff(AtkHitBuff):
    def activate(self, atk, *args, **kwargs):
        for tmp_buff in self.buff[:]:
            tmp_buff = copy.copy(tmp_buff)
            tmp_buff.value *= self.master.get_final_status('luck')
            self.master.add_buff(tmp_buff)


class Skill_110131_3(Skill):
    """当队伍中I国船≥3时，全队舰船攻击时增加自身50%幸运值的额外伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            LuckExtraDamage(
                timer=timer,
                name='extra_damage',
                phase=AllPhase,
                value=0.5,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        num_I = len(CountryTarget(side=1, country='I').get_target(friend, enemy))
        return num_I >= 3


class LuckExtraDamage(CoeffBuff):
    """攻击时增加自身50%幸运值的额外伤害"""
    def is_active(self, *args, **kwargs):
        self.value = np.ceil(0.5 * self.master.get_final_status('luck'))
        return isinstance(self.timer.phase, self.phase)


name = '幸运之星'
skill = [Skill_110131_1, Skill_110131_2, Skill_110131_3]
