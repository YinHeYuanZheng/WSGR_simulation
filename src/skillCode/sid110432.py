# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 渐减雷击(北上改-2、大井改-2)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""开幕雷击一起发射三枚鱼雷，威力为鱼雷值均值的80%，
该鱼雷具有40%的穿甲属性，且中破时开幕雷击无视战损，并使被击中的目标回避减少10
（必须北上、大井在队伍中且同时使用本技能）"""


class Skill_110432(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.multi_flag = False
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='multi_attack',
                phase=FirstTorpedoPhase,
            ),
            ActPhaseBuff(
                timer=timer,
                name='act_phase',
                phase=FirstTorpedoPhase
            ),
            CoeffBuff(
                timer=timer,
                name='power_buff',
                phase=FirstTorpedoPhase,
                value=-0.2,
                bias_or_weight=2
            ),
            CoeffBuff(
                timer=timer,
                name='pierce_coef',
                phase=FirstTorpedoPhase,
                value=0.4,
                bias_or_weight=0
            ),
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=FirstTorpedoPhase,
                atk_request=[BuffRequest_1]
            ),
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=FirstTorpedoPhase,
                buff=[
                    StatusBuff(
                        timer=timer,
                        name='evasion',
                        phase=AllPhase,
                        value=-10,
                        bias_or_weight=0
                    )
                ],
                side=0
            )
        ]

    def is_active(self, friend, enemy):
        sis_list = CidTarget(side=1, cid_list=['11043', '11044']
                             ).get_target(friend, enemy)
        if self.master not in sis_list:  # master不是北上大井（让巴尔复制）
            return False

        sis_list.remove(self.master)
        if len(sis_list) == 0:  # 队伍内不同时存在北上大井
            return False

        sister = sis_list[0]
        if type(sister.skill[0]).__name__ != type(self).__name__:  # 没有同时使用本技能
            return False

        # 站位靠前的获得双发能力
        if sister.loc > self.master.loc:
            self.multi_flag = True
        else:
            self.multi_flag = False
        return True

    def activate(self, friend, enemy):
        if self.multi_flag:  # 站位靠前的获得双发能力
            mul_buff = copy.copy(self.buff[0])
            self.master.add_buff(mul_buff)

        for tmp_buff in self.buff[1:]:
            tmp_buff = copy.copy(tmp_buff)
            self.master.add_buff(tmp_buff)


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.atk_body.damaged == 2


skill = [Skill_110432]
