# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 沃克兰

from src.wsgr.formulas import TorpedoAtk
from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自己和相邻两艘驱逐舰的火力值 7 点，鱼雷值 6 点
遭受鱼雷攻击时增加自己回避35点。"""


class Skill_110981_1(Skill):
    """增加自己和相邻两艘驱逐舰的火力值 7 点，鱼雷值 6 点
    """
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='near',
            master_include=True,
            shiptype=DD
        )

        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=7,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            )
        ]


class Skill_110981_2(Skill):
    """遭受鱼雷攻击时增加自己回避35点。
    """
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                timer=timer,
                name='get_atk',
                phase=AllPhase,
                buff=[
                    DuringAtkBuff(
                        timer=timer,
                        name='evasion',
                        phase=AllPhase,
                        value=35,
                        bias_or_weight=0
                    )
                ],
                side=1,
                atk_request=[ATK_Request1]
            )
        ]
    

class ATK_Request1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, TorpedoAtk)
        

name = '超级驱逐舰'
skill = [Skill_110981_1, Skill_110981_2]
