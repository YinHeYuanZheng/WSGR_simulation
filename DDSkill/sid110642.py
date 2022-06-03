# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 吹雪孤注一掷

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""提升自身2点耐久值；射程变为长。
队伍中的特型驱逐舰小于等于2时，提升自身9点火力值、15点鱼雷值，(全阶段)自身攻击无法暴击，附带自身鱼雷值35%的固定伤害。"""


class Skill_110642_1(CommonSkill):
    """提升自身2点耐久值；"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='health',
                phase=AllPhase,
                value=2,
                bias_or_weight=0,
            ),
        ]
class Skill_110642_2(Skill):
    """射程变为长。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='range',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
        ]
class Skill_110642_3(Skill):
    def __init__(self, timer, master):
        "队伍中的特型驱逐舰小于等于2时，提升自身9点火力值、15点鱼雷值，(全阶段)自身攻击无法暴击，附带自身鱼雷值35%的固定伤害。"
        super().__init__(timer, master)
        """全阶段命中不暴击未完成"""
        self.target = TagTarget(side=1, tag="fubuki")
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=7,
                bias_or_weight=0,
            ),
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=15,
                bias_or_weight=0,
            ),




            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=AllPhase,
                buff=[
                    this_extra_damage_buff(
                        timer=timer,
                        name="extra_damage",
                        phase=AllPhase,
                        value=.35,
                        bias_or_weight=0    
                    )
                ],
                side=1,
            )
            
            
            
        ]
    def is_active(self, friend, enemy):
        count = len(TagTarget(side=1, tag="fubuki").get_target(friend, enemy))
        return count <= 2
skill = [Skill_110642_1, Skill_110642_2, Skill_110642_3]
class this_extra_damage_buff(CoeffBuff):
    def is_active(self, *args, **kwargs):
        self.value = np.ceil(self.master.get_final_status('torpedo') * 0.35)
        return True