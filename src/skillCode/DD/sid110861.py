# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 哥萨克人

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import NormalAtk, AntiSubAtk

"""昼战全阶段锁定攻击敌方对应位置的船只，
炮击战35%概率发动特殊攻击，造成额外20点固定伤害且必定命中。"""


class Skill_110861_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_loc_target',
                phase=DaytimePhase,
                target=LocTarget(side=0, loc=[master.loc]),
                ordered=True
            ),
            SpecialLock(
                timer=timer,
                phase=ShellingPhase,
            ),
            AtkHitBuff(
                timer=timer,
                name='give_atk',
                phase=ShellingPhase,
                buff=[
                    DuringAtkBuff(
                        timer=timer,
                        name='extra_damage',
                        phase=ShellingPhase,
                        value=20,
                        bias_or_weight=0
                    ),
                    DuringAtkBuff(
                        timer=timer,
                        name='must_hit',
                        phase=ShellingPhase,
                        bias_or_weight=3
                    )
                ],
                side=1,
                rate=0.35
            )
        ]


class SpecialLock(ActiveBuff):
    """在炮击战辅助哥萨克人判断攻击类型"""
    def __init__(self, timer, phase, name='special_attack', num=1, rate=1):
        super().__init__(timer, name, phase, num, rate)
        self.normal_atk = NormalAtk
        self.anti_sub_atk = AntiSubAtk

    def get_lock_target(self, enemy):
        return [ship for ship in enemy.ship
                if ship.loc == self.master.loc]

    def is_active(self, atk, enemy, *args, **kwargs):
        if not isinstance(self.timer.phase, self.phase):
            return False

        def_list = self.get_lock_target(enemy)  # 获取锁定的对位
        if not len(def_list):  # 对位不存在
            return False
        elif def_list[0].damaged == 4:  # 对位不存活
            return False
        else:
            return True

    def active_start(self, atk, enemy, *args, **kwargs):
        def_list = self.get_lock_target(enemy)  # 获取锁定的对位
        if not len(def_list) or def_list[0].damaged == 4:  # 对位不存在, 报错
            raise TypeError(f"Wrong call of {self.master.status['name']} skill.")

        lock_target = def_list[0]
        if lock_target.can_be_atk(self.anti_sub_atk):
            atk_type = self.anti_sub_atk
        else:
            atk_type = self.normal_atk

        special_atk = atk_type(
            timer=self.timer,
            atk_body=self.master,
            def_list=def_list
        )
        yield special_atk


name = '跳帮作战'
skill = [Skill_110861_1]
