# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 爱斯基摩人

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.equipment import Torpedo, DepthMine
from src.wsgr.formulas import TorpedoAtk

"""每次出征可以免疫1次鱼雷攻击，提升35%自身所装备鱼雷的鱼雷值和反潜装备的反潜值。"""


class Skill_110871_1(Skill):
    """每次出征可以免疫1次鱼雷攻击"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='shield',
                phase=AllPhase,
                exhaust=1,
                atk_request=[ATK_Request_1]
            )
        ]

    def activate(self, friend, enemy):
        self.master.add_buff(self.buff[0])


class ATK_Request_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, TorpedoAtk)


class Skill_110871_2(CommonSkill):
    """提升35%自身所装备鱼雷的鱼雷值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(
            side=1,
            target=SelfTarget(master),
            equiptype=Torpedo
        )
        self.buff = [
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=0.35,
                bias_or_weight=1
            )
        ]


class Skill_110871_3(CommonSkill):
    """提升35%自身所装备反潜装备的反潜值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(
            side=1,
            target=SelfTarget(master),
            equiptype=DepthMine
        )
        self.buff = [
            CommonBuff(
                timer=timer,
                name='antisub',
                phase=AllPhase,
                value=0.35,
                bias_or_weight=1
            )
        ]


name = '征战四方'
skill = [Skill_110871_1, Skill_110871_2, Skill_110871_3]
