# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 丹阳改-祥瑞御免
# 玩具技能，没写

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""将所有己方其他舰船的幸运吸收至自身.
每 9 点幸运增加1%回避率。"""


# class Skill_111691(Skill):
#     """将所有己方其他舰船的幸运吸收至自身.每 9 点幸运增加1%回避率"""
#     def __init__(self, timer, master):
#         super().__init__(timer, master)
#         self.target = SelfTarget(master)
#         self.buff = [
#             StatusBuff(
#                 timer=timer,
#                 name='evasion',
#                 phase=AllPhase,
#                 value=0.01,
#                 bias_or_weight=1
#             )
#         ]
#
#     def activate(self, friend, enemy):
#         target = self.target.get_target(friend, enemy)
#         for tmp_target in target:
#             for tmp_buff in self.buff[:]:
#                 tmp_buff = copy.copy(tmp_buff)
#                 tmp_target.add_buff(tmp_buff)
        

name = '祥瑞御免(本技能无实际效果，请检查技能编号)'
skill = []
