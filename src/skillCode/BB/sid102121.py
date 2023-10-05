# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 利托里奥-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队I国舰船火力值和命中值增加12点，装甲值和回避值增加15点。
当维内托位于队伍中时，利托里奥和维内托攻击力提升20%，全队维内托级舰船全阶段免疫1次伤害。"""


class Skill_102121_1(Skill):
    """全队I国舰船火力值和命中值增加12点，装甲值和回避值增加15点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='I')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
        ]


class Skill_102121_2(Skill):
    """当维内托位于队伍中时，利托里奥和维内托攻击力提升20%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.target_2 = None
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='power_buff',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=2
            )
        ]

    def is_active(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        for tmp_ship in friend:
            # 维内托cid = 10112/11112
            if tmp_ship.cid == '10112' or tmp_ship.cid == '11112':
                self.target_2 = tmp_ship
                return True
        return False

    def activate(self, friend, enemy):
        if self.target_2 is None:
            return
        target = self.target.get_target(friend, enemy)
        for tmp_buff in self.buff[:]:
            buff_1 = copy.copy(tmp_buff)
            target.add_buff(buff_1)
            buff_2 = copy.copy(tmp_buff)
            self.target_2.add_buff(buff_2)


class Skill_102121_3(Skill):
    """当维内托位于队伍中时，全队维内托级舰船全阶段免疫1次伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TagTarget(side=1, tag='veneto',)
        self.buff = [
            OnceFinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-1
            )
        ]

    def is_active(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        for tmp_ship in friend:
            # 维内托cid = 10112/11112
            if tmp_ship.cid == '10112' or tmp_ship.cid == '11112':
                return True
        return False


class OnceFinalDamageBuff(FinalDamageBuff):
    """仅限一次的终伤buff"""
    def __init__(self, timer, name, phase, value):
        super().__init__(timer, name, phase, value)
        self.exhaust = 1

    def is_active(self, *args, **kwargs):
        if self.exhaust == 0:
            return False
        else:
            self.exhaust -= 1
            return True


name = '381警告！'
skill = [Skill_102121_1, Skill_102121_2, Skill_102121_3]
