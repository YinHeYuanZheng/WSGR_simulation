# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

import pandas as pd


class Dataset:
    def __init__(self, infile):
        self._infile = infile
        # self.ship_data_0 = pd.read_excel(self._infile, sheet_name='舰船数据-普通', index_col=0)
        self.ship_data_1 = pd.read_excel(self._infile, sheet_name='舰船数据-改造', index_col=0)
        # self.ship_data_enemy = pd.read_excel(self._infile, sheet_name='舰船数据-深海', index_col=0)

    def get_ship_status(self, cid):
        # if cid[0] == '1':
        #     if cid[1] == '0':
        #         ship_list = self.ship_data_0
        #     if cid[1] == '1':
        #         ship_list = self.ship_data_1

        ship_list = self.ship_data_1
        ship = ship_list.loc[int(cid)]
        status = {
            'name': ship.loc['名称'],  # 船名
            'country': ship.loc['国籍'],  # 国籍
            'total_health': int(ship.loc['耐久']),  # 总耐久
            'health': int(ship.loc['耐久']),  # 当前耐久
            'fire': int(ship.loc['火力']),  # 火力
            'armor': int(ship.loc['装甲']),  # 装甲
            'torpedo': int(ship.loc['鱼雷']),  # 鱼雷
            'antiair': int(ship.loc['对空']),  # 对空
            'antisub': int(ship.loc['对潜']),  # 对潜
            'accuracy': int(ship.loc['命中']),  # 命中
            'evasion': int(ship.loc['回避']),  # 回避
            'recon': int(ship.loc['索敌']),  # 索敌
            'speed': int(ship.loc['航速']),  # 航速
            'range': int(ship.loc['射程']),  # 射程, 1: 短; 2: 中; 3: 长; 4: 超长
            'luck': int(ship.loc['幸运']),  # 幸运
            'equipnum': int(ship.loc['装备栏']),  # 装备栏
            'capacity': int(ship.loc['总搭载']),  # 总搭载
            'tag': str(ship.loc['标签']).split(','),  # 标签
        }

        if status['capacity'] != 0:
            status['load'] = []
            for i in range(1, status['equipnum']+1):
                status['load'].append(int(ship.loc['搭载'+str(i)]))

        if cid[1] == '1':
            status['skill'] = [
                str(ship.loc['技能1']),
                str(ship.loc['技能2'])
            ]

        return status
