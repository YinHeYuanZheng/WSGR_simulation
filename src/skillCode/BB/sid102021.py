# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 伊利诺伊-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""战斗中我方每次命中敌人都会增加自身5点火力值和装甲值。
队伍中的衣阿华级舰船增加15火力值和15%暴击率。
自身编队相邻舰船射程提升2档。"""


class Skill_102021_1(Skill):
    """战斗中我方每次命中敌人都会增加自身5点火力值和装甲值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            SpecialAtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=AllPhase,
                buff=[
                    StatusBuff(
                        timer=timer,
                        name='fire',
                        phase=AllPhase,
                        value=5,
                        bias_or_weight=0
                    ),
                    StatusBuff(
                        timer=timer,
                        name='armor',
                        phase=AllPhase,
                        value=5,
                        bias_or_weight=0
                    )
                ],
                target=master
            )
        ]


class SpecialAtkHitBuff(AtkHitBuff):
    def __init__(self, timer, name, phase, buff, target,
                 side=1, atk_request=None, bias_or_weight=3, rate=1):
        super().__init__(timer, name, phase, buff,
                         side, atk_request, bias_or_weight, rate)
        self.target = target

    def activate(self, atk, *args, **kwargs):
        for tmp_buff in self.buff[:]:
            tmp_buff = copy.copy(tmp_buff)
            self.target.add_buff(tmp_buff)


class Skill_102021_2(Skill):
    """队伍中的衣阿华级舰船增加15火力值和15%暴击率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TagTarget(side=1, tag='iowa')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=0
            )
        ]


class Skill_102021_3(Skill):
    """自身编队相邻舰船射程提升2档。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='near'
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='range_buff',
                phase=AllPhase,
                value=2,
                bias_or_weight=0
            )
        ]


name = '巨炮残响'
skill = [Skill_102021_1, Skill_102021_2, Skill_102021_3]
