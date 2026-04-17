# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 米切尔改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from AADG_common import *

"""终极粉碎(3级)：敌方每有1艘主力舰，都会增加自身10点火力值和装甲值。
自身攻击时增加自身50%火力值的额外伤害。受到15点以上伤害时，伤害将降低到15点。
炮击战阶段优先攻击对位敌人，自身受到伤害后对攻击的敌人发动反击，
该次反击的攻击威力不会因耐久损伤而降低且必定命中（大破无法发动）。
自身装备的发射器会视为反潜装备，其索敌值视为对潜值。
"""


class Skill_116181_1(Skill):
    """敌方每有1艘主力舰，都会增加自身10点火力值和装甲值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
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
                value=10,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        count = len(TypeTarget(side=0, shiptype=MainShip).get_target(friend, enemy))
        if count == 0:
            return
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= count
                tmp_target.add_buff(tmp_buff)


class Skill_116181_2(Skill):
    """自身攻击时增加自身50%火力值的额外伤害。受到15点以上伤害时，伤害将降低到15点。
    炮击战阶段优先攻击对位敌人，自身受到伤害后对攻击的敌人发动反击，
    该次反击的攻击威力不会因耐久损伤而降低且必定命中（大破无法发动）。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FireExtraDamage(
                timer=timer,
                name='extra_damage',
                phase=AllPhase,
                value=0,
                bias_or_weight=0
            ),
            CapShield(
                timer=timer,
                phase=AllPhase,
                cap_value=15
            ),
            PriorTargetBuff(
                timer=timer,
                name='prior_loc_target',
                phase=ShellingPhase,
                target=LocTarget(side=0, loc=[master.loc]),
                ordered=False
            ),
            HitBack(
                timer=timer,
                phase=ShellingPhase,
                coef={'ignore_damaged': True,
                      'must_hit': True},
                exhaust=None
            )
        ]


class FireExtraDamage(AtkBuff):
    """攻击时额外伤害 = ceil(自身火力 × 50%)"""
    def change_value(self, *args, **kwargs):
        try:
            atk = kwargs['atk']
        except KeyError:
            atk = args[0]
        self.value = np.ceil(atk.source.get_final_status('fire') * 0.5)


class CapShield(CoeffBuff):
    """伤害上限：超过 cap_value 的伤害降低到 cap_value"""
    def __init__(self, timer, phase, cap_value,
                 name='reduce_damage', value=0, bias_or_weight=0, rate=1):
        super().__init__(timer, name, phase, value, bias_or_weight, rate)
        self.cap_value = cap_value

    def change_value(self, damage, *args, **kwargs):
        self.value = max(0, damage - self.cap_value)


name = '终极粉碎'
skill = [Skill_116181_1, Skill_116181_2, AADGCommonSkill]
