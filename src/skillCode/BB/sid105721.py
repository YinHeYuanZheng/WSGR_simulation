# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 骏河-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身与编队相邻右边一艘舰船增加8%暴击率和8点装甲值，如果编队相邻右边一艘为J国舰船，则该船获得两倍效果。
炮击战阶段50%概率对敌方进行一次必定命中且必定暴击的特殊攻击。
若近江位于队伍中，特殊攻击发动概率变为100%，全队J国舰船攻击威力提高10%。"""


class Skill_105721_1(Skill):
    """自身与编队相邻右边一艘舰船增加8%暴击率和8点装甲值，如果编队相邻右边一艘为J国舰船，则该船获得两倍效果。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='down'
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.08,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                if tmp_target.status['country'] == 'J':
                    tmp_buff.value *= 2
                tmp_target.add_buff(tmp_buff)

        for tmp_buff in self.buff[:]:
            tmp_buff = copy.copy(tmp_buff)
            self.master.add_buff(tmp_buff)


class Skill_105721_2(Skill):
    """炮击战阶段50%概率对敌方进行一次必定命中且必定暴击的特殊攻击。
    若近江位于队伍中，特殊攻击发动概率变为100%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialAtkBuff(
                timer=timer,
                phase=ShellingPhase,
                rate=0.5,
                coef={'must_hit': True,
                      'must_crit': True}
            )
        ]

    def activate(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        cid_list = [tmp_ship.cid for tmp_ship in friend]
        tmp_buff = copy.copy(self.buff[0])

        # 若近江位于队伍中，特殊攻击发动概率变为100%
        # 近江cid = 10514/11514
        if ('10514' in cid_list) or ('11514' in cid_list):
            tmp_buff.change_rate(1)
        self.master.add_buff(tmp_buff)


class Skill_105721_3(Skill):
    """若近江位于队伍中，全队J国舰船攻击威力提高10%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='J')
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='power_buff',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=2
            )
        ]

    def is_active(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        cid_list = [tmp_ship.cid for tmp_ship in friend]
        # 近江cid = 10514/11514
        return ('10514' in cid_list) or ('11514' in cid_list)


name = '战列线中坚'
skill = [Skill_105721_1, Skill_105721_2, Skill_105721_3]
