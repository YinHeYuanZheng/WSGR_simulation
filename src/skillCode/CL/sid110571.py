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
                coef={'final_damage_buff': -0.1},
            )
        ]


class NeighborAtkBuff(ActiveBuff):
    def is_active(self, atk_type, enemy, *args, **kwargs):
        from src.wsgr.formulas import AntiSubAtk
        if issubclass(atk_type, AntiSubAtk):
            return False
        return super().is_active(atk_type, enemy, *args, **kwargs)

    def active_start(self, atk, enemy, *args, **kwargs):
        assert self.master is not None
        from src.wsgr.formulas import AntiSubAtk
        assert not isinstance(atk, AntiSubAtk)
        def_list = atk.def_list

        self.add_during_buff()  # 攻击时效果
        atk.set_coef(self.coef)  # 添加参数
        yield atk
        tmp_target = atk.target

        neighbor_target = NearestLocTarget(
            side=0, master=tmp_target, radius=1, direction='near'
        ).get_target(None, def_list)
        if len(neighbor_target):
            another_atk = type(atk)(
                timer=self.timer,
                atk_body=self.master,
                def_list=neighbor_target,
                coef=copy.copy(self.coef),
            )
            yield another_atk

        self.remove_during_buff()  # 去除攻击时效果
        self.add_end_buff()  # 攻击结束效果


name = '高速弹幕'
skill = [Skill_110571]
