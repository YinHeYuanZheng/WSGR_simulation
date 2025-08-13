# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 1939战列舰-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""1939战列舰在战斗中视为维内托级舰船。
全队维内托级舰船火力值、装甲值和命中值增加18点。
炮击战阶段攻击时增加自身50%装甲值的额外伤害。
炮击战阶段有40%概率同时攻击2个目标，队伍中每有1艘维内托级舰船都会增加20%发动概率。"""


class Skill_104661_1(Skill):
    """全队维内托级舰船火力值、装甲值和命中值增加18点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TagTarget(side=1, tag='veneto')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=18,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=18,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=18,
                bias_or_weight=0
            )
        ]


class Skill_104661_2(Skill):
    """炮击战阶段攻击时增加自身50%装甲值的额外伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            ArmorExtraDamage(
                timer=timer,
                name='extra_damage',
                phase=ShellingPhase,
                value=0.5,
                bias_or_weight=0
            )
        ]


class ArmorExtraDamage(AtkBuff):
    def change_value(self, *args, **kwargs):
        try:
            atk = kwargs['atk']
        except:
            atk = args[0]
        self.value = np.ceil(atk.atk_body.get_final_status('armor') * 0.5)


class Skill_104661_3(Skill):
    """炮击战阶段有40%概率同时攻击2个目标，队伍中每有1艘维内托级舰船都会增加20%发动概率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MultipleAtkBuff(
                timer=timer,
                name='multi_attack',
                phase=ShellingPhase,
                num=2,
                rate=0.4,
            )
        ]

    def activate(self, friend, enemy):
        buff_0 = copy.copy(self.buff[0])
        target_veneto = TagTarget(side=1, tag='veneto').get_target(friend, enemy)
        buff_0.rate = min(1., buff_0.rate + 0.2 * len(target_veneto))
        self.master.add_buff(buff_0)


name = '第五人'
skill = [Skill_104661_1, Skill_104661_2, Skill_104661_3]
