# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 但丁-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身攻击要塞、机场、港口时增加40%伤害。
全队主力舰增加10点火力值、12点装甲值，I国舰船获得双倍效果。"""


class Skill_105321_1(Skill):
    """自身攻击要塞、机场、港口时增加40%伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.4,
                atk_request=[ATKRequest_1]
            )
        ]


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (Fortness, Aircraft, Port))


class Skill_105321_2(Skill):
    """全队主力舰增加10点火力值、12点装甲值，I国舰船获得双倍效果。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=MainShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                if tmp_target.status['country'] == 'I':
                    tmp_buff.value *= 2
                tmp_target.add_buff(tmp_buff)



name = '最初三联'
skill = [Skill_105321_1, Skill_105321_2]
