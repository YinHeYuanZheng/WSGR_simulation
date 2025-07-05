# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# AIII

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队G国舰船索敌值增加5点，火力值、命中值、装甲值增加9点。
自身装备的飞机类装备对空值提高50%。攻击时增加自身100%对空值的火力值，增加自身50%耐久值的额外伤害。
索敌成功时，自身因战斗造成的舰载机损失减少100%，炮击战阶段同时对2个目标发动必定命中且暴击的攻击。"""


class Skill_105861_1(PrepSkill):
    """全队G国舰船索敌值增加5点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='G')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]


class Skill_105861_2(Skill):
    """全队G国舰船火力值、命中值、装甲值增加9点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='G')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            )
        ]


class Skill_105861_3(CommonSkill):
    """自身装备的飞机类装备对空值提高50%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(
            side=1,
            target=SelfTarget(master),
            equiptype=Plane
        )
        self.buff = [
            CommonBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=0.5,
                bias_or_weight=1
            )
        ]


class Skill_105861_4(Skill):
    """攻击时增加自身100%对空值的火力值，增加自身50%耐久值的额外伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                timer=timer,
                name='give_atk',
                phase=AllPhase,
                buff=[
                    AntiairBaseFire(
                        timer=timer,
                        name='fire',
                        phase=AllPhase,
                        value=1,
                        bias_or_weight=0
                    )
                ],
                side=1
            ),
            HealthExtraDamage(
                timer=timer,
                name='extra_damage',
                phase=AllPhase,
                value=0.5,
                bias_or_weight=0
            )
        ]


class AntiairBaseFire(DuringAtkBuff):
    """增加自身100%对空值的火力值"""
    def change_value(self, *args, **kwargs):
        self.value = self.master.get_final_status('antiair')


class HealthExtraDamage(StatusBuff):
    """增加自身50%耐久值的额外伤害"""
    def change_value(self, *args, **kwargs):
        health = self.master.status['standard_health']
        self.value = np.ceil(health * 0.5)


class Skill_105861_5(Skill):
    """索敌成功时，自身因战斗造成的舰载机损失减少100%，
    炮击战阶段同时对2个目标发动必定命中且暴击的攻击。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='fall_rest',
                phase=AirPhase,
                value=-1,
                bias_or_weight=1,
            ),
            SkillMultiAtkBuff(
                timer=timer,
                name='multi_attack',
                phase=ShellingPhase,
                num=2,
                rate=1,
                coef={'must_hit': True,
                      'must_crit': True}
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_recon_flag()


class SkillMultiAtkBuff(MultipleAtkBuff):
    """对2个目标发动必定命中且暴击的攻击"""
    def active_start(self, atk: ATK, enemy: Fleet, *args, **kwargs):
        assert self.master is not None
        self.add_during_buff()  # 攻击时效果

        first_target = None
        for i in range(self.num):
            atk = self.raise_atk(enemy, first_target)
            if atk is None:
                break
            yield atk
            first_target = atk.target

        self.remove_during_buff()  # 去除攻击时效果
        self.add_end_buff()  # 攻击结束效果

    def raise_atk(self, target_fleet: Fleet, first_target) -> ATK:
        """通过技能代码重构AIII炮击战逻辑
        目前次轮炮击可以同时进行反潜和炮击，优先反潜"""
        atk = None

        # 优先反潜
        if self.master.check_anti_sub():
            def_list = target_fleet.get_atk_target(atk_type=self.master.anti_sub_atk)
            if first_target is not None and first_target in def_list:
                def_list.remove(first_target)  # 移除第一次攻击目标
            if len(def_list):
                atk = self.master.anti_sub_atk(
                    timer=self.timer,
                    atk_body=self.master,
                    def_list=def_list,
                    coef=self.coef
                )

        # 普通炮击
        if atk is None:  # 无反潜
            def_list = target_fleet.get_atk_target(atk_type=self.master.normal_atk)
            if first_target is not None and first_target in def_list:
                def_list.remove(first_target)  # 移除第一次攻击目标
            if len(def_list):
                atk = self.master.normal_atk(
                    timer=self.timer,
                    atk_body=self.master,
                    def_list=def_list,
                    coef=self.coef
                )

        return atk  # 当技能发动时只剩一个目标存活，第二次攻击判定可能生成None


name = '破交'
skill = [Skill_105861_1, Skill_105861_2, Skill_105861_3,
         Skill_105861_4, Skill_105861_5]
