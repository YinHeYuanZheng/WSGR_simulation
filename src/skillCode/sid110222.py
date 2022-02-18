# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 赤城改-2

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *


class Skill_110222_1(Skill):
    """鱼雷机装备数量较多时，鱼雷机威力增加25%，轰炸机威力降低25%"""
    def __init__(self, master):
        super().__init__(master)

        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                name='air_bomb_atk_buff',
                phase=(AirPhase,),
                value=-0.25,
                bias_or_weight=2
            ),
            CoeffBuff(
                name='air_dive_atk_buff',
                phase=(AirPhase,),
                value=0.25,
                bias_or_weight=2
            )
        ]

    def is_active(self, friend, enemy):
        return bool(self.request[0](self.master, friend, enemy))


class Request_1(Request):
    def __bool__(self):
        # 轰炸机数量（搭载量，不是装备格）
        bomb = EquipTarget(
            side=1,
            target=SelfTarget(self.master),
            equiptype=(Bomber,)
        ).get_target(self.friend, self.enemy)
        num_bomb = sum([plane.load for plane in bomb])

        # 鱼雷机数量（搭载量，不是装备格）
        dive = EquipTarget(
            side=1,
            target=SelfTarget(self.master),
            equiptype=(DiveBomber,)
        ).get_target(self.friend, self.enemy)
        num_dive = sum([plane.load for plane in dive])

        # return len(dive) > len(bomb)
        return num_dive > num_bomb


class Skill_110222_2(Skill):
    """轰炸机装备数量较多时，轰炸机威力增加25%，鱼雷机威力降低25%"""
    def __init__(self, master):
        super().__init__(master)

        self.request = [Request_2]
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                name='air_bomb_atk_buff',
                phase=(AirPhase,),
                value=0.25,
                bias_or_weight=2
            ),
            CoeffBuff(
                name='air_dive_atk_buff',
                phase=(AirPhase,),
                value=-0.25,
                bias_or_weight=2
            )
        ]

    def is_active(self, friend, enemy):
        return bool(self.request[0](self.master, friend, enemy))


class Request_2(Request):
    def __bool__(self):
        # 轰炸机数量（搭载量，不是装备格）
        bomb = EquipTarget(
            side=1,
            target=SelfTarget(self.master),
            equiptype=(Bomber,)
        ).get_target(self.friend, self.enemy)
        num_bomb = sum([plane.load for plane in bomb])

        # 鱼雷机数量（搭载量，不是装备格）
        dive = EquipTarget(
            side=1,
            target=SelfTarget(self.master),
            equiptype=(DiveBomber,)
        ).get_target(self.friend, self.enemy)
        num_dive = sum([plane.load for plane in dive])

        # return len(bomb) > len(dive)
        return num_bomb > num_dive


skill = [Skill_110222_1, Skill_110222_2]
