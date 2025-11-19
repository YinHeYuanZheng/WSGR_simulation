# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 卡萨诺方案-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import *


"""全队战巡航速增加5节，装甲值和火力值增加25点，受到的鱼雷攻击伤害降低80%。
自身炮击战阶段40%概率同时攻击3个目标，队伍中每有1艘战巡都会增加10%发动概率"""


class Skill_106051_1(PrepSkill):
    """全队战巡航速增加5节"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=BC)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='speed',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]


class Skill_106051_2(Skill):
    """全队战巡装甲值和火力值增加25点，受到的鱼雷攻击伤害降低80%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=BC)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-0.8,
                atk_request=[BuffRequest_1]
            ),
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, TorpedoAtk)


class Skill_106051_3(Skill):
    """自身炮击战阶段40%概率同时攻击3个目标，队伍中每有1艘战巡都会增加10%发动概率"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master=master)
        self.buff = [
            MultipleAtkBuff(
                timer=self.timer,
                name='multi_attack',
                phase=ShellingPhase,
                num=3,
                rate=0.4
            )
        ]

    def activate(self, friend, enemy):
        # 队伍中每有1艘战巡都会增加10%发动概率
        buff_0 = copy.copy(self.buff[0])
        target_bc = TypeTarget(side=1, shiptype=BC).get_target(friend, enemy)  # 获取战巡
        buff_0.rate = min(1., 0.4 + 0.1 * len(target_bc))
        self.master.add_buff(buff_0)


name = '时代幻想'
skill = [Skill_106051_1, Skill_106051_2, Skill_106051_3]