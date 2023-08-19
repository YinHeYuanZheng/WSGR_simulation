# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# A150-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身被攻击概率提升30%，中破和大破时暴击伤害提升30%。
队伍里除了自身没有其它J国舰船时，自身攻击无视战损。
首轮炮击阶段，A150可以同时攻击多个目标（目标数量为队伍中J国战列、战巡、航战数量，最多3艘），并增加自身50%装甲值的额外伤害。"""


class Skill_101911_1(Skill):
    """自身被攻击概率提升30%，中破和大破时暴击伤害提升30%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MagnetBuff(
                timer=timer,
                phase=AllPhase,
                rate=0.3
            ),
            AtkBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.atk_body.damaged in [2, 3]


class Skill_101911_2(Skill):
    """队伍里除了自身没有其它J国舰船时，自身攻击无视战损。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase,
            )
        ]

    def is_active(self, friend, enemy):
        shipJ = CountryTarget(side=1, country='J'
                              ).get_target(friend, enemy)
        shipJ.remove(self.master)
        return len(shipJ) == 0


class Skill_101911_3(Skill):
    """首轮炮击阶段，A150可以同时攻击多个目标
    （目标数量为队伍中J国战列、战巡、航战数量，最多3艘），
    并增加自身50%装甲值的额外伤害。"""
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
                during_buff=[
                    ArmorExtraDamage(
                        timer=timer,
                        name='extra_damage',
                        phase=AllPhase,
                        value=0.5,
                        bias_or_weight=0
                    )
                ]
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.cid in ['10191', '11191']

    def activate(self, friend, enemy):
        bbJ = CombinedTarget(
            side=1,
            target_list=[CountryTarget(side=1, country='J'),
                         TypeTarget(side=1, shiptype=(BB, BC, BBV))]
        ).get_target(friend, enemy)
        buff0 = copy.copy(self.buff[0])
        buff0.num = min(3, len(bbJ))
        self.master.add_buff(buff0)


class ArmorExtraDamage(AtkBuff):
    def change_value(self, *args, **kwargs):
        try:
            atk = kwargs['atk']
        except:
            atk = args[0]
        self.value = np.ceil(atk.atk_body.get_final_status('armor') * 0.5)


name = '泡沫幻影'
skill = [Skill_101911_1, Skill_101911_2, Skill_101911_3]
