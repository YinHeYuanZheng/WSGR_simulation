# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 玛丽亚皇后-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队航速低于27节的舰船火力、装甲、命中、回避增加25点，攻击航速高于27节的敌人时伤害提高25%。
提高自身30%被攻击概率，自身大破时，免疫伤害，全队S国舰船暴击伤害提高60%。"""


class Skill_112151_1(Skill):
    """全队航速低于27节的舰船火力、装甲、命中、回避增加25点，攻击航速高于27节的敌人时伤害提高25%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = StatusTarget(
            side=1,
            status_name='speed',
            fun='lt',
            value=27
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.25,
                atk_request=[ATKRequest_1]
            )
        ]


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.target.get_final_status('speed') > 27


class Skill_112151_2(Skill):
    """提高自身30%被攻击概率，自身大破时，免疫伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MagnetBuff(
                timer=timer,
                phase=AllPhase,
                rate=0.3,
            ),
            SevereDamagedShield(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-1
            )
        ]


class SevereDamagedShield(FinalDamageBuff):
    def is_active(self, *args, **kwargs):
        if self.master.damaged == 3:
            return True
        else:
            return False


class Skill_112151_3(Skill):
    """自身大破时，全队S国舰船暴击伤害提高60%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='S')
        self.buff = [
            SevereDamagedBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.6,
                bias_or_weight=0,
                check_target=master
            )
        ]


class SevereDamagedBuff(CoeffBuff):
    def __init__(self, check_target, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.check_target = check_target

    def is_active(self, *args, **kwargs):
        if self.check_target.damaged == 3:
            return True
        else:
            return False


name = '黑海皇后'
skill = [Skill_112151_1, Skill_112151_2, Skill_112151_3]
