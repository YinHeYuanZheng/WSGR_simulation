# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 武藏-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身非中破和大破时，增加全队舰船15点火力值、回避值、对空值和装甲值。
中破和大破时自身攻击无视目标装甲值且攻击威力不会受到耐久损伤的影响。
中破时炮击战阶段自身受到伤害后会对攻击的敌人发动必中的反击。
当A150位于队伍中时，自身将变为[俱尽]状态，自身和A150额外提高30%暴击率。"""


class Skill_106131_1(Skill):
    """自身非中破和大破时，增加全队舰船15点火力值、回避值、对空值和装甲值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            ShiftBuff_1(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            ShiftBuff_1(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            ShiftBuff_1(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            ShiftBuff_1(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class ShiftBuff_1(StatusBuff):
    def is_active(self, *args, **kwargs):
        if self.master.damaged == 1:
            return super().is_active(*args, **kwargs)
        else:
            return False


class Skill_106131_2(Skill):
    """中破和大破时自身攻击无视目标装甲值且攻击威力不会受到耐久损伤的影响。
    中破时炮击战阶段自身受到伤害后会对攻击的敌人发动必中的反击。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='ignore_armor',
                phase=AllPhase,
                value=-1,
                bias_or_weight=1,
                atk_request=[BuffRequest_1]
            ),
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=BuffPhase,
            ),
            HitBack_106131(
                timer=timer,
                phase=ShellingPhase,
                exhaust=None,
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.atk_body.damaged in [2, 3]


class HitBack_106131(HitBack):
    def __init__(self, timer, phase, *args, **kwargs):
        super().__init__(timer, phase, *args, **kwargs)
        self.master_damaged = None

    def set_master(self, master):
        self.master_damaged = master.damaged  # 战损状态缓存(受伤前状态)
        super().set_master(master)

    def is_active(self, atk, *args, **kwargs):
        # 如果战损状态缓存是中破，技能发动
        if self.master_damaged == 2:
            return super().is_active(atk, *args, **kwargs)
        # 否则更新战损状态缓存，技能不发动
        self.master_damaged = self.master.damaged
        return False


class Skill_106131_3(Skill):
    """当A150位于队伍中时，自身和A150额外提高30%暴击率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.target_2 = None
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        for tmp_ship in friend:
            # A150 cid = 10191/11191
            if tmp_ship.cid == '10191' or tmp_ship.cid == '11191':
                self.target_2 = tmp_ship
                return True
        return False

    def activate(self, friend, enemy):
        if self.target_2 is None:
            return
        tmp_target = self.target.get_target(friend, enemy)[0]
        for tmp_buff in self.buff[:]:
            buff_1 = copy.copy(tmp_buff)
            tmp_target.add_buff(buff_1)
            buff_2 = copy.copy(tmp_buff)
            self.target_2.add_buff(buff_2)


name = '神前讨魔'
skill = [Skill_106131_1, Skill_106131_2, Skill_106131_3]
