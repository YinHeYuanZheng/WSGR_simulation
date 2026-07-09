# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 不挠-1

from src.wsgr.equipment import *
from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""持久作战(3级)：提升自身所携带的鱼雷机的鱼雷值7点。
攻击威力不会因耐久损伤而降低，
且同时减少30%自身因战斗造成的舰载机损失（大破时除外）。"""


class Skill_103191_1(CommonSkill):
    """提升自身所携带的鱼雷机的鱼雷值7点"""

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
                value=7,
                bias_or_weight=0
            )
        ]


class Skill_103191_2(Skill):
    """攻击威力不会因耐久损伤而降低，
    且同时减少30%自身因战斗造成的舰载机损失（大破时除外）。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase,
            ),
            UnDamagedFallRest(
                timer=timer,
                name='fall_rest',
                phase=AirPhase,
                value=-0.3,
                bias_or_weight=1,
            )
        ]


class UnDamagedFallRest(CoeffBuff):
    """仅在非大破时减少舰载机损失。
    击坠减免在战斗机与轰炸机(ATK 作为 atk 传入)两条路径下均会被查询，
    因此依据 buff 持有者自身的制空结果判定，避免依赖传入的 atk 对象类型。"""

    def is_active(self, *args, **kwargs):
        if not super().is_active(*args, **kwargs):
            return False
        return self.master.damaged < 3


name = '持久作战'
skill = [Skill_103191_1, Skill_103191_2]
