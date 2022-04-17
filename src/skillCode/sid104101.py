# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 萨勒姆-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""精锐装备(3级)：提升自身携带装备所增加的命中值*1.5的火力值。
炮击战阶段有25%概率同时攻击两个目标，第二个目标造成80%的伤害"""


class Skill_104101_1(CommonSkill):
    """提升自身携带装备所增加的命中值*1.5的火力值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=1.5,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        e_accuracy = self.master.get_equip_status('accuracy')
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff.value *= e_accuracy
                tmp_target.add_buff(tmp_buff)


class Skill_104101_2(Skill):
    """炮击战阶段有25%概率同时攻击两个目标，第二个目标造成80%的伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SecondAtkBuff(
                timer=timer,
                name='multi_attack',
                phase=ShellingPhase,
                num=2,
                rate=0.25,
                during_buff=[
                    FinalDamageBuff(
                        timer=timer,
                        name='final_damage_buff',
                        phase=ShellingPhase,
                        value=-0.2
                    )
                ]
            )
        ]


class SecondAtkBuff(MultipleAtkBuff):
    """同时攻击两个目标，第二个目标造成80%的伤害"""
    def active_start(self, atk, enemy, *args, **kwargs):
        assert self.master is not None
        def_list = enemy.get_atk_target(atk_type=atk)

        for i in range(self.num):
            if not len(def_list):
                break

            if i == self.num - 1:
                self.add_during_buff()  # 攻击时效果

            tmp_atk = atk(
                timer=self.timer,
                atk_body=self.master,
                def_list=def_list,
                coef=self.coef,
            )
            tmp_target = tmp_atk.target_init()
            def_list.remove(tmp_target)
            yield tmp_atk

        self.remove_during_buff()  # 去除攻击时效果
        self.add_end_buff()  # 攻击结束效果


skill = [Skill_104101_1, Skill_104101_2]
