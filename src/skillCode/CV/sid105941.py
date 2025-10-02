# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 黄蜂(CV-18)-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身攻击威力不会因耐久损伤而降低，中破时自身回避率和暴击率提高30%。
自身炮击战阶段可对同一个目标进行两次攻击。
全队舰船受到要塞、机场和港口的伤害降低70%，攻击要塞、机场和港口伤害提高40%。
当队伍中除了自身外还存在埃塞克斯级航母时，自身舰载机威力提高30%。"""


class Skill_105941_1(Skill):
    """自身攻击威力不会因耐久损伤而降低，中破时自身回避率和暴击率提高30%。
    自身炮击战阶段可对同一个目标进行两次攻击。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase
            ),
            AtkBuff(
                timer=timer,
                name='miss_rate',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0,
                atk_request=[BuffRequest_1]
            ),
            AtkBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0,
                atk_request=[BuffRequest_1]
            ),
            ExtraAtkBuff(
                timer=timer,
                name='extra_attack',
                phase=ShellingPhase,
                num=2,
                rate=1
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.atk_body.damaged == 2


class Skill_105941_2(Skill):
    """全队舰船受到要塞、机场和港口的伤害降低70%，攻击要塞、机场和港口伤害提高40%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-0.7,
                atk_request=[BuffRequest_2]
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.4,
                atk_request=[BuffRequest_3]
            )
        ]


class BuffRequest_2(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.atk_body, (Fortness, Airfield, Port))


class BuffRequest_3(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (Fortness, Airfield, Port))


class Skill_105941_3(Skill):
    """当队伍中除了自身外还存在埃塞克斯级航母时，自身舰载机威力提高30%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=2,
            )
        ]

    def is_active(self, friend, enemy):
        target_essex = TagTarget(side=1, tag='essex').get_target(friend, enemy)  # 获取埃塞克斯级
        if self.master in target_essex:
            target_essex.remove(self.master)  # 去除自身
        return len(target_essex)


name = '蜇击'
skill = [Skill_105941_1, Skill_105941_2, Skill_105941_3]
