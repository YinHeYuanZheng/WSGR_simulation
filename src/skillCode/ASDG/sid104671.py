# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 鞍山

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.equipment import *

"""增强自身所装备导弹装备的8点火力值与5点突防值。自己和队伍内导驱开幕导弹阶段增加16%伤害。"""


class Skill_104671_1(CommonSkill):
    """增强自身所装备导弹装备的8点火力值与5点突防值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(side=1,
                                  target=SelfTarget(master),
                                  equiptype=Missile)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='missile_atk',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]


class Skill_104671_2(Skill):
    """自己和队伍内导驱开幕导弹阶段增加16%伤害"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=ASDG)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=FirstMissilePhase,
                value=0.16
            )
        ]


name = '力争上游'
skill = [Skill_104671_1, Skill_104671_2]
