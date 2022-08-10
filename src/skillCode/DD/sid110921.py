# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 布雷恩改

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加 8 点索敌值，60% 的索敌视为火力和对空。"""


class Skill_110921(CommonSkill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=.6,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=.6,
                bias_or_weight=0
            ),
        ]
    def activate(self, friend, enemy):
        """Question:
            如果 self.target = SelfTarget(master)
            self.master 和 self.target.get_target(friend, enemy) 是否为同一个实例
           Answer:

        """
        
        target = self.target.get_target(friend, enemy)
        recon = self.master.get_final_status('recon')
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= recon
                tmp_target.add_buff(tmp_buff)



name = '冷战先锋'
skill = [Skill_110921]
