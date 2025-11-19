# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 深海俾斯麦

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import MagicAtk

"""炮击战阶段受到伤害后对敌人发动反击，伤害为40点且必定命中（大破状态不发动）"""


class Skill_000061_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            HitBack_Bismark(
                timer=timer,
                phase=ShellingPhase,
                exhaust=None
            )
        ]


class HitBack_Bismark(HitBack):
    def activate(self, atk, *args, **kwargs):
        assert atk.atk_body.side != self.master.side

        hit_back = BismarkHitBackAtk(
            timer=self.timer,
            atk_body=self.master,
            def_list=None,
            coef=copy.copy(self.coef),
            target=atk.atk_body
        )
        hit_back.changable = False
        return hit_back


class BismarkHitBackAtk(MagicAtk):
    def formula(self):
        return 40


name = '反击'
skill = [Skill_000061_1]

