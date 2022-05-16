# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 朱诺改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""高速弹幕(3级)：炮击战阶段有40%概率对两个相邻的单位造成90%的伤害,对水下单位无效。"""


class Skill_110571(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            NeighborAtkBuff(
                timer=timer,
                name='multi_attack',
                phase=ShellingPhase,
                num=2,
                rate=0.4,
                during_buff=[
                    FinalDamageBuff(
                        timer=timer,
                        name='final_damage_buff',
                        phase=ShellingPhase,
                        value=-0.1
                    )
                ]
            )
        ]


class NeighborAtkBuff(ActiveBuff):
    def active_start(self, atk, enemy, *args, **kwargs):
        assert self.master is not None
        def_list = enemy.get_atk_target(atk_type=atk)
        assert len(def_list)
        self.add_during_buff()  # 攻击时效果

        atk_sample = atk(
            timer=self.timer,
            atk_body=self.master,
            def_list=def_list,
            coef=copy.copy(self.coef),
        )
        tmp_target = atk_sample.target_init()
        # def_list.remove(tmp_target)
        yield atk_sample

        neighbor_target = NearestLocTarget(
            side=0, master=tmp_target, radius=1, direction='near'
        ).get_target(None, def_list)
        if not len(neighbor_target):
            return
        another_atk = atk(
            timer=self.timer,
            atk_body=self.master,
            def_list=neighbor_target,
            coef=copy.copy(self.coef),
        )
        yield another_atk


skill = [Skill_110571]
