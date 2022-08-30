# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 凤凰城-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""涅槃(3级)：战斗中受到大于当前血量50%的伤害时，减少99%所受到的伤害。（每场战斗触发一次）"""


class Skill_104221(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            RecoverShield(timer=timer)
        ]


class RecoverShield(CoeffBuff):
    def __init__(self, timer, phase=AllPhase, name='reduce_damage',
                 value=0, bias_or_weight=0, rate=1):
        super().__init__(timer, name, phase, value, bias_or_weight, rate)
        self.exhaust = 1

    def is_active(self, damage, *args, **kwargs):
        if self.exhaust == 0:
            return False

        master_health = self.master.status['health']
        if damage <= master_health * 0.5:
            return False

        self.value = np.floor(damage * 0.99)
        self.exhaust -= 1
        return True


name = '涅槃'
skill = [Skill_104221]
