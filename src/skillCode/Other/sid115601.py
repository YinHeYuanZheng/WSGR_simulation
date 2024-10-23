# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 石勒苏益格-荷尔施泰因改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自身所装备的主炮类装备15点火力值。
攻击航速小于自身的敌人时最终伤害增加50%。"""


class Skill_115601_1(CommonSkill):
    """增加自身所装备的主炮类装备15点火力值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(
            side=1,
            target=SelfTarget(master),
            equiptype=MainGun
        )
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_115601_2(Skill):
    """攻击航速小于自身的敌人时最终伤害增加50%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.5,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.target.get_final_status('speed') < \
               self.atk.atk_body.get_final_status('speed')


name = '凯撒炮术'
skill = [Skill_115601_1, Skill_115601_2]
