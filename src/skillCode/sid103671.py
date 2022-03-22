# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 乌尔里希·冯·胡滕-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
from src.wsgr.formulas import *
"""德式设计(3级)：提升自身装甲值10点，
航空战时增加15%被暴击率，
炮击战时免疫受到的第一次炮击攻击，
攻击护甲高于自身的敌人时，提升自身15%暴击伤害。
"""


class Skill_103671_1(CommonSkill):
    """提升自身装甲值10点，"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer,
                name="armor",
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]


class Skill_103671_2(Skill):
    """航空战时增加15%被暴击率，"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer,
                name='be_crit',
                phase=AirPhase,
                value=0.15,
                bias_or_weight=0
            )
        ]


class Skill_103671_3(Skill):
    """炮击战时免疫受到的第一次炮击攻击，"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='shield',
                phase=(AllPhase,),
                atk_request=[BuffRequest_1])
        ]


class Skill_103671_4(Skill):
    """攻击护甲高于自身的敌人时，提升自身15%暴击伤害。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=0,
                atk_request=[Request_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, NormalAtk)


class Request_1(ATKRequest):
    def __bool__(self):
        return self.atk.atk_body.status['armor'] < self.atk.target.status['armor']


skill = [Skill_103671_1, Skill_103671_2, Skill_103671_3, Skill_103671_4]
