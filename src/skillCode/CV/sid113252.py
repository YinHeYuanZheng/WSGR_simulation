# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 列克星敦(cv-16)-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身提升15%舰载机威力。
自身编队左边2艘舰船提升8%舰载机威力，如果编队左边2艘舰船为U国舰船，则再额外提升其8%舰载机威力。
当列克星敦(CV-2)位于队伍中时，自身和列克星敦(CV-2)提升15%舰载机威力。"""


class Skill_113252_1(Skill):
    """自身提升15%舰载机威力"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=2
            )
        ]


class Skill_113252_2(Skill):
    """自身编队左边2艘舰船提升8%舰载机威力，
    如果编队左边2艘舰船为U国舰船，则再额外提升其8%舰载机威力"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=2,
            direction='up',
        )
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.08,
                bias_or_weight=2
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                buff_1 = copy.copy(tmp_buff)
                tmp_target.add_buff(buff_1)
                if tmp_target.status['country'] in 'U':
                    buff_2 = copy.copy(tmp_buff)
                    tmp_target.add_buff(buff_2)


class Skill_113252_3(Skill):
    """当列克星敦(CV-2)位于队伍中时，自身和列克星敦(CV-2)提升15%舰载机威力"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.target_2 = None
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=2
            )
        ]

    def is_active(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        for tmp_ship in friend:
            # 列克星敦cv2 cid = 10029/11029
            if tmp_ship.cid == '10029' or tmp_ship.cid == '11029':
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


name = '传承者'
skill = [Skill_113252_1, Skill_113252_2, Skill_113252_3]
