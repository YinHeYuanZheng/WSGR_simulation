# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 10581工程

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""战斗中免疫受到的第一次攻击。全队U国和S国舰船火力值和命中值增加20点。
全队航战暴击率提高20%。占据制空权、制空优势时自身因战斗造成的舰载机损失减少100%。
首轮炮击阶段对队伍航战数量（最多3艘）的敌方进行一次必中攻击，并提升敌方50%回避值的额外伤害。"""


class Skill_106351_1(Skill):
    """战斗中免疫受到的第一次攻击
    占据制空权、制空优势时自身因战斗造成的舰载机损失减少100%。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='shield',
                phase=AllPhase,
                exhaust=1
            ),
            AirControlFallRest(
                timer=timer,
                name='fall_rest',
                phase=AirPhase,
                value=-1,
                bias_or_weight=1
            )
        ]


class AirControlFallRest(CoeffBuff):
    """仅在占据制空权(空确)、制空优势时减少舰载机损失。
    击坠减免在战斗机与轰炸机(ATK 作为 atk 传入)两条路径下均会被查询，
    因此依据 buff 持有者自身的制空结果判定，避免依赖传入的 atk 对象类型。"""

    def is_active(self, *args, **kwargs):
        if not super().is_active(*args, **kwargs):
            return False
        return self.master.get_air_con_flag() in [1, 2]


class Skill_106351_2(Skill):
    """全队U国和S国舰船火力值和命中值增加20点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='US')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=20,
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


class Skill_106351_3(Skill):
    """全队航战暴击率提高20%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=BBV)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            )
        ]


class Skill_106351_4(Skill):
    """首轮炮击阶段对队伍航战数量（最多3艘）的敌方进行一次必中攻击，
    并提升敌方50%回避值的额外伤害"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MultipleAtkBuff(
                timer=timer,
                name='multi_attack',
                phase=FirstShellingPhase,
                num=3,
                rate=1,
                coef={'must_hit': True},
                during_buff=[
                    EvasionExtraDamage(
                        timer=timer,
                        name='extra_damage',
                        phase=AllPhase,
                        value=0.5,
                        bias_or_weight=0
                    )
                ]
            )
        ]

    def activate(self, friend, enemy):
        bbv = TypeTarget(side=1, shiptype=BBV).get_target(friend, enemy)
        num = min(3, len(bbv))
        if num == 0:
            return
        buff0 = copy.copy(self.buff[0])
        buff0.num = num
        self.master.add_buff(buff0)


class EvasionExtraDamage(AtkBuff):
    """提升敌方(被攻击目标)50%回避值的额外伤害"""

    def change_value(self, *args, **kwargs):
        try:
            atk = kwargs['atk']
        except KeyError:
            atk = args[0]
        self.value = np.ceil(atk.target.get_final_status('evasion') * 0.5)


name = 'Атака!'
skill = [Skill_106351_1, Skill_106351_2, Skill_106351_3, Skill_106351_4]
