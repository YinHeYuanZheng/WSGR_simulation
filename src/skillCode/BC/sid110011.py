# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 胡德-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队提高10%暴击率和暴击伤害，全队E国舰船额外提高10%暴击率和暴击伤害。
自身为舰队旗舰时，首轮炮击阶段自身会首先进行攻击并且伤害提高50%，
如果命中的是战列或者重巡，则额外提高50%伤害。"""


class Skill_110011_1(Skill):
    """全队提高10%暴击率和暴击伤害，全队E国舰船额外提高10%暴击率和暴击伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                # E国船两倍
                if tmp_target.status['country'] == 'E':
                    tmp_buff.value *= 2
                tmp_target.add_buff(tmp_buff)


class Skill_110011_2(Skill):
    """自身为舰队旗舰时，首轮炮击阶段自身会首先进行攻击并且伤害提高50%，
    如果命中的是战列或者重巡，则额外提高50%伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='range_buff',
                phase=FirstShellingPhase,
                value=50,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=FirstShellingPhase,
                value=0.5,
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=FirstShellingPhase,
                value=0.5,
                atk_request=[ATKRequest_1]
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (BB, CA))


name = '皇家海军的荣耀'
skill = [Skill_110011_1, Skill_110011_2]
