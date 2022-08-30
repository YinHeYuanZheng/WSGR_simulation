# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 可畏改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自身携带的轰炸机5点轰炸值和鱼雷机5点鱼雷值。
航空战阶段自身对战列舰、重巡洋舰造成的伤害提高24%。
当我方队伍中战列舰≥3时，航空战阶段和炮击战阶段自身优先攻击战列舰，攻击战列舰时降低敌方100%对空值(不包含装备)。"""


class Skill_112242_1(CommonSkill):
    """增加自身携带的轰炸机5点轰炸值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(
            side=1,
            target=SelfTarget(master),
            equiptype=Bomber
        )
        self.buff = [
            CommonBuff(
                timer=timer,
                name='bomb',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]


class Skill_112242_2(CommonSkill):
    """增加自身携带的鱼雷机5点鱼雷值。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(
            side=1,
            target=SelfTarget(master),
            equiptype=DiveBomber
        )
        self.buff = [
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]


class Skill_112242_3(Skill):
    """航空战阶段自身对战列舰、重巡洋舰造成的伤害提高24%。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AirPhase,
                value=0.24,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (BB, CA))


class Skill_112242_4(Skill):
    """当我方队伍中战列舰≥3时，航空战阶段和炮击战阶段自身优先攻击战列舰，
    攻击战列舰时降低敌方100%对空值(不包含装备)。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=(AirPhase, ShellingPhase),
                target=RandomTypeTarget(side=0, shiptype=BB),
                ordered=False
            ),
            AtkBuff(
                timer=timer,
                name='ignore_antiair',
                phase=AllPhase,
                value=-1,
                bias_or_weight=1,
                atk_request=[BuffRequest_2]
            )
        ]

    def is_active(self, friend, enemy):
        target_bb = TypeTarget(side=1, shiptype=BB)\
            .get_target(friend, enemy)
        return len(target_bb) >= 3


class BuffRequest_2(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, BB)


skill = [Skill_112242_1, Skill_112242_2, Skill_112242_3, Skill_112242_4]
