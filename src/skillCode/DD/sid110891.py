# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 弗莱彻

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""图鉴中每开启1艘弗莱彻级舰船，增加自己火力，装甲，对空，命中，回避，鱼雷，幸运，对潜面板属性各1点。(现版本总计27)"""


class Skill_110891(CommonSkill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        buff_value = 27
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=buff_value,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=buff_value,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=buff_value,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=buff_value,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=buff_value,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=buff_value,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='luck',
                phase=AllPhase,
                value=buff_value,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='antisub',
                phase=AllPhase,
                value=buff_value,
                bias_or_weight=0
            ),
        ]


name = '最优驱逐舰'
skill = [Skill_110891]
