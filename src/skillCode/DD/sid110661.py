# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 初雪改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import MagicAtk

"""自身火力值增加 10 点，鱼雷值和回避减少 5 点；
炮击战时 30% 概率对敌方水上单位(优先攻击航母)触发特殊攻击，
造成火力值 100% 的伤害且必定命中。(大破无法发动)
"""


class Skill_110661_1(CommonSkill):
    """自身火力值增加 10 点，鱼雷值和回避减少 5 点；"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=-5,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-5,
                bias_or_weight=0
            )
        ]


class Skill_110661_2(Skill):
    """炮击战时 30% 概率对敌方水上单位(优先攻击航母)触发特殊攻击，
    造成火力值 100% 的伤害且必定命中。(大破无法发动)"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialAtkBuff_110661(
                timer=timer,
                phase=ShellingPhase,
                rate=.3,
                atk_type=MagicAtk_110661,
                undamaged=True
            )
        ]


class SpecialAtkBuff_110661(SpecialAtkBuff):
    """对敌方水上单位(优先攻击航母)触发特殊攻击"""
    def active_start(self, atk: ATK, enemy, *args, **kwargs):
        assert self.master is not None
        self.add_during_buff()  # 攻击时效果

        atk_type = MagicAtk_110661  # 使用特殊攻击类型
        def_list = self.get_def_list(atk_type, enemy)  # 可被攻击目标
        prior = TypeTarget(side=0, shiptype=CV).\
                    get_target(None, def_list)  # 优先攻击航母
        if len(prior):
            def_list = prior

        special_atk = atk_type(
            timer=self.timer,
            atk_body=self.master,
            def_list=def_list,
            coef=copy.copy(self.coef),
        )
        yield special_atk

        self.remove_during_buff()  # 去除攻击时效果
        self.add_end_buff()  # 攻击结束效果


class MagicAtk_110661(MagicAtk):
    """造成火力值 100% 的伤害且必定命中"""
    def formula(self):
        return np.ceil(self.atk_body.get_final_status('fire'))


name = '零距炮击'
skill = [Skill_110661_1, Skill_110661_2]
