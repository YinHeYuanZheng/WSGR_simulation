# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 猎户座-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.equipment import *

"""自身携带主炮类装备的增加3点火力值；
单纵阵和梯形阵时降低自身5点闪避值，增加自身15点火力值与20点装甲值
同时，队伍内其他战列舰增加10点火力值与10点装甲值（对低速舰船提升数值翻倍）。"""


class Skill_104681_1(CommonSkill):
    """自身携带主炮类装备的增加3点火力值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(side=1,
                                  target=SelfTarget(master),
                                  equiptype=(MainGun,))
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            )
        ]


class Skill_104681_2(Skill):
    """单纵阵和梯形阵时降低自身5点闪避值，增加自身15点火力值与20点装甲值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master=master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_form() == 1 or \
               self.master.get_form() == 4


class Skill_104681_3(Skill):
    """单纵阵和梯形阵时, 队伍内其他战列舰增加10点火力值与10点装甲值（对低速舰船提升数值翻倍）"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=BB)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_form() == 1 or \
               self.master.get_form() == 4

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)

                # 对低速舰船提升数值翻倍
                if tmp_target.get_final_status('speed') <= 27:
                    tmp_buff.value *= 2
                tmp_target.add_buff(tmp_buff)


skill = [Skill_104681_1, Skill_104681_2, Skill_104681_3]
