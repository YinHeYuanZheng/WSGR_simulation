# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 初夏改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""缘之祝福(3级)：全队北风型驱逐舰对空值、鱼雷值和回避值增加15点。
先制鱼雷、鱼雷战阶段全队驱逐、潜艇、雷巡提高10%暴击率；
队伍中每有一艘驱逐、潜艇、雷巡都会额外再提高3%暴击率。
当队伍中J国驱逐≥2时，随机2艘敌方舰船降低30点回避值和装甲值。
"""


class Skill_112661_1(Skill):
    """全队北风型驱逐舰对空值、鱼雷值和回避值增加15点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TagTarget(side=1, tag='kitakaze')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_112661_2(Skill):
    """先制鱼雷、鱼雷战阶段全队驱逐、潜艇、雷巡提高10%暴击率；
    队伍中每有一艘驱逐、潜艇、雷巡都会额外再提高3%暴击率"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(DD, SS, CLT))
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=TorpedoPhase,
                value=0.10,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        count = len(TypeTarget(side=1, shiptype=(DD, SS, CLT)).get_target(friend, enemy))
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value += 0.03 * count
                tmp_target.add_buff(tmp_buff)


class Skill_112661_3(Skill):
    """当队伍中J国驱逐≥2时，随机2艘敌方舰船降低30点回避值和装甲值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = RandomTarget(side=0, num=2)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-30,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-30,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        j_dd = [ship for ship in
                CountryTarget(side=1, country='J').get_target(friend, enemy)
                if isinstance(ship, DD)]
        return len(j_dd) >= 2


name = '缘之祝福'
skill = [Skill_112661_1, Skill_112661_2, Skill_112661_3]
