# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 彼得·施特拉塞尔-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.equipment import *

"""超重型航弹(3级)：增加自身20%暴击率。
彼得·施特拉塞尔命中过的目标会降低10点闪避值与10点装甲值，
如果是航母装母轻母单位还会再额外降低10点命中值(限炮击战阶段)"""


class Skill_104261_1(Skill):
    """增加自身20%暴击率。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=(AllPhase,),
                value=0.2,
                bias_or_weight=0
            )
        ]


class Skill_104261_2(Skill):
    """彼得·施特拉塞尔命中过的目标会降低10点闪避值与10点装甲值（限炮击战阶段）"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=(AllPhase,),
                buff=[
                    StatusBuff(
                        timer=timer,
                        name='evasion',
                        phase=(ShellingPhase,),
                        value=-10,
                        bias_or_weight=0
                    ),
                    StatusBuff(
                        timer=timer,
                        name='armor',
                        phase=(ShellingPhase,),
                        value=-10,
                        bias_or_weight=0
                    )
                ],
                side=0)
        ]


class Skill_104261_3(Skill):
    """如果是航母装母轻母单位还会再额外降低10点命中值（限炮击战阶段）。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=(AllPhase,),
                buff=[
                    StatusBuff(
                        timer=timer,
                        name='accurace',
                        phase=(ShellingPhase,),
                        value=-10,
                        bias_or_weight=0)
                ],
                side=0,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (CV, AV, CVL))


name = '超重型航弹'
skill = [Skill_104261_1, Skill_104261_2, Skill_104261_3]
