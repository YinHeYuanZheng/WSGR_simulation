# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 密西西比-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自身12点火力值和36点制空值，全队索敌增加5点。
索敌成功时，炮击战阶段全队航速低于27节的舰船伤害提高30%，全队U国舰船伤害再额外提高30%"""


class Skill_106021_1(CommonSkill):
    """增加自身12点火力值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master=master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]


class Skill_106021_2(Skill):
    """增加自身36点制空值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master=master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_ctrl_buff',
                phase=AllPhase,
                value=36,
                bias_or_weight=0
            )
        ]


class Skill_106021_3(PrepSkill):
    """全队索敌增加5点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=5,
                bias_or_weight=0,
            )
        ]


class Skill_106021_4(Skill):
    """索敌成功时，炮击战阶段全队航速低于27节的舰船伤害提高30%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = StatusTarget(
            side=1,
            status_name='speed',
            fun='lt',
            value=27
        )
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.3,
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_recon_flag()


class Skill_106021_5(Skill):
    """索敌成功时，全队U国舰船伤害再额外提高30%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='U')
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.3,
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_recon_flag()


name = '观测炮击'
skill = [Skill_106021_1, Skill_106021_2, Skill_106021_3,
         Skill_106021_4, Skill_106021_5]