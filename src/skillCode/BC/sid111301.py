# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 斯佩伯爵海军上将-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""破交袭击：攻击航速低于或等于自己的敌方单位时提升 12% 暴击率，
被航速高于或等于自己的单位攻击时回避率提升 12%。"""


class Skill_111301(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.12,
                bias_or_weight=0,
                atk_request=[Request_1]
            ),
            AtkBuff(
                timer=timer,
                name='miss_rate',
                phase=AllPhase,
                value=0.12,
                bias_or_weight=0,
                atk_request=[Request_1]
            )
        ]


class Request_1(ATKRequest):
    def __bool__(self):
        return self.atk.atk_body.get_final_status('speed') >= \
               self.atk.target.get_final_status('speed')


name = '破交袭击'
skill = [Skill_111301]
