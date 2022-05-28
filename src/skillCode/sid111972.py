# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# U-47 狼群战术

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""队伍中每有一艘潜艇，都会增加所有潜艇的命中值 2 点及暴击率 2%，这个技能只在旗舰是 U 型潜艇时生效。"""


class Skill_111972_1(Skill):
    """队伍中每有一艘潜艇，都会增加所有潜艇的命中值 2 点及暴击率 2%，这个技能只在旗舰是 U 型潜艇时生效。"""
    
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(master, shiptype=SS)
        #value 将在 activate 具体计算
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=2,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=.02,
                bias_or_weight=0
            )
        ]
    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        flagship = LocTarget(side=1, loc=[1]).get_target(friend, enemy)[0]
        count = len(target)
        if(not (flagship.get_final_status('country') == 'G' and isinstance(flagship, SS))):return
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= count
                tmp_target.add_buff(tmp_buff)
skill = [Skill_111972_1,]
