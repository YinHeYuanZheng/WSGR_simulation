# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 休·W·哈德利改

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队舰船对空值增加40点，命中值增加20点。
航空战阶段自身被攻击概率和回避率提高30%。自身对空值的40%视为火力值。
自身优先攻击航母、装母和轻母，攻击航母、装母和轻母时无视目标装甲且攻击威力不会因耐久损伤而降低并造成2倍伤害。"""


class Skill_115891_1(Skill):
    """全队舰船对空值增加40点，命中值增加20点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=40,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]


class Skill_115891_2(Skill):
    """航空战阶段自身被攻击概率和回避率提高30%。
    自身对空值的40%视为火力值。
    自身优先攻击航母、装母和轻母，攻击航母、装母和轻母时
    无视目标装甲且攻击威力不会因耐久损伤而降低并造成2倍伤害。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MagnetBuff(
                timer=timer,
                phase=AirPhase,
                rate=0.3
            ),
            CoeffBuff(
                timer=timer,
                name='miss_rate',
                phase=AirPhase,
                value=0.3,
                bias_or_weight=0
            ),
            AntiairBasedFire(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=0.4,
                bias_or_weight=0
            ),
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=AllPhase,
                target=TypeTarget(side=0, shiptype=(CV, AV, CVL)),
                ordered=True
            ),
            AtkBuff(
                timer=timer,
                name='ignore_armor',
                phase=AllPhase,
                value=-1,
                bias_or_weight=1,
                atk_request=[AtkCVTypeRequest]
            ),
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase,
                atk_request=[AtkCVTypeRequest]
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=1,
                atk_request=[AtkCVTypeRequest]
            )
        ]


class AntiairBasedFire(StatusBuff):
    """自身对空值的指定比例视为火力值"""

    def change_value(self, *args, **kwargs):
        self.value = np.ceil(self.master.get_final_status('antiair') * 0.4)


class AtkCVTypeRequest(ATKRequest):
    """攻击目标为航母(CV)、装母(AV)、轻母(CVL)"""

    def __bool__(self):
        return isinstance(self.atk.target, (CV, AV, CVL))


name = '枪弹帷幕'
skill = [Skill_115891_1, Skill_115891_2]
