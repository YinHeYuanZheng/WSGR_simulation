# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 护航援护

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身位于队伍中时，提高舰队中战列舰的装甲值3/5/7/10点。"""


class Strategy_322(FleetStrategy):
    def __init__(self, timer, master, level=3):
        super().__init__(timer, master, level)
        value = [3, 5, 7, 10]
        self.stid = '322'
        self.target = TypeTarget(side=1, shiptype=BB)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=value[self.level],
                bias_or_weight=0
            )
        ]


skill = [Strategy_322]
