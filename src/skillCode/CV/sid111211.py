# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 企业改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_111211_1(CommonSkill):
    """增加自身回避20点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]


class Skill_111211_2(Skill):
    """队伍中没有其余航母（航母，轻母，装母）存在时，自身射程变更为长,火力加成55点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.request = [Request_1]
        self.buff = [
            StatusBuff(
                timer=timer,
                name='range',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=55,
                bias_or_weight=0
            )
        ]


class Request_1(Request):
    def __bool__(self):
        target = TypeTarget(
            side=1,
            shiptype=(CV, CVL, AV)
        ).get_target(self.friend, self.enemy)
        target.remove(self.master)
        num = len(target)
        return num == 0


name = '独木成林'
skill = [Skill_111211_1, Skill_111211_2]
