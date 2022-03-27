# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 乌尔里希·冯·胡滕-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""德式设计(3级)：提升自身装甲值10点，航空战时增加15%被暴击率。
炮击战时免疫受到的第一次炮击攻击，攻击护甲高于自身的敌人时，提升自身15%暴击伤害。"""


class Skill_103671_1(CommonSkill):
    """提升自身装甲值10点，"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]


class Skill_103671_2(Skill):
    """航空战时增加15%被暴击率。炮击战时免疫受到的第一次炮击攻击，
    攻击护甲高于自身的敌人时，提升自身15%暴击伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='be_crit',
                phase=AirPhase,
                value=0.15,
                bias_or_weight=0
            ),
            SpecialBuff(
                timer=timer,
                name='shield',
                phase=ShellingPhase,
                exhaust=1
            ),
            AtkBuff(
                timer=timer,
                name='crit_coef',
                phase=ShellingPhase,
                value=0.15,
                bias_or_weight=0,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.target.get_final_status('armor') > \
               self.atk.atk_body.get_final_status('armor')


skill = [Skill_103671_1, Skill_103671_2]
