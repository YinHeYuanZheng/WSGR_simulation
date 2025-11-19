# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 昆西-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身和敌方旗舰被攻击概率提高25%。
自身中破时可免疫2次伤害，火力值增加25点，暴击率提高25%，攻击威力不会因耐久损伤而降低。
炮击战阶段25%概率发动，攻击敌方舰队旗舰，该次攻击必中且无视敌方装甲，
队伍中每有1艘U国重巡都会给该攻击提高25%发动概率和伤害。"""


class Skill_110402_1(Skill):
    """自身和敌方旗舰被攻击概率提高25%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = LocTarget(side=0, loc=[1])
        self.buff = [
            MagnetBuff(
                timer=timer,
                phase=AllPhase,
                rate=0.25
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        target.append(self.master)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_target.add_buff(tmp_buff)


class Skill_110402_2(Skill):
    """自身中破时可免疫2次伤害，火力值增加25点，暴击率提高25%，攻击威力不会因耐久损伤而降低。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MidDamagedBuff_1(
                timer=timer,
                phase=AllPhase,
                exhaust=2,
            ),
            MidDamagedBuff_2(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            ),
            MidDamagedBuff_3(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=.25,
                bias_or_weight=0
            ),
            MidDamagedBuff_4(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase,
            ),
        ]


class MidDamagedBuff_1(DamageShield):
    def is_active(self, *args, **kwargs):
        if self.master.damaged == 2:
            return super().is_active(*args, **kwargs)
        else:
            return False


class MidDamagedBuff_2(StatusBuff):
    def is_active(self, *args, **kwargs):
        if self.master.damaged == 2:
            return super().is_active(*args, **kwargs)
        else:
            return False


class MidDamagedBuff_3(CoeffBuff):
    def is_active(self, *args, **kwargs):
        if self.master.damaged == 2:
            return super().is_active(*args, **kwargs)
        else:
            return False


class MidDamagedBuff_4(SpecialBuff):
    def is_active(self, *args, **kwargs):
        if self.master.damaged == 2:
            return super().is_active(*args, **kwargs)
        else:
            return False


class Skill_110402_3(Skill):
    """炮击战阶段25%概率发动，攻击敌方舰队旗舰，该次攻击必中且无视敌方装甲，
    队伍中每有1艘U国重巡都会给该攻击提高25%发动概率和伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialAtkBuff(
                timer=timer,
                phase=ShellingPhase,
                rate=0.25,
                during_buff=[
                    CoeffBuff(
                        timer=timer,
                        name='ignore_armor',
                        phase=ShellingPhase,
                        value=-1,
                        bias_or_weight=1
                    )
                ],
                target=LocTarget(side=0, loc=[1]),
                coef={'must_hit': True,
                      'final_damage_buff': 1}
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        u_ca = CombinedTarget(
            side=1,
            target_list=[
                CountryTarget(side=1, country='U'),
                TypeTarget(side=1, shiptype=CA)
            ]
        ).get_target(friend, enemy)
        for tmp_target in target:
            buff_0 = copy.copy(self.buff[0])
            buff_0.rate += 0.25 * len(u_ca)
            buff_0.coef['final_damage_buff'] += 0.25 * len(u_ca)
            tmp_target.add_buff(buff_0)


name = '旗舰杀手0V0'
skill = [Skill_110402_1, Skill_110402_2, Skill_110402_3]
