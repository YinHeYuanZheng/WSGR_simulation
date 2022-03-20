# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

import pandas as pd


class Dataset:
    def __init__(self, infile):
        self._infile = infile
        self.ship_data_0 = pd.read_excel(
            self._infile, sheet_name='舰船数据-未改', keep_default_na=False, dtype=str)
        self.ship_data_0.set_index('cid', inplace=True)

        self.ship_data_1 = pd.read_excel(
            self._infile, sheet_name='舰船数据-改造', keep_default_na=False, dtype=str)
        self.ship_data_1.set_index('cid', inplace=True)

        self.ship_data_enemy = pd.read_excel(
            self._infile, sheet_name='舰船数据-深海', keep_default_na=False, dtype=str)
        self.ship_data_enemy.set_index('cid', inplace=True)

        self.equip_data_friend = pd.read_excel(
            self._infile, sheet_name='装备数据-常规', keep_default_na=False, dtype=str)
        self.equip_data_friend.set_index('eid', inplace=True)

        self.equip_data_enemy = pd.read_excel(
            self._infile, sheet_name='装备数据-深海', keep_default_na=False, dtype=str)
        self.equip_data_enemy.set_index('eid', inplace=True)

    def get_friend_ship_status(self, cid):
        if cid[1] == '0':
            ship_list = self.ship_data_0
        else:
            ship_list = self.ship_data_1

        try:
            ship = ship_list.loc[cid]
        except:
            raise ValueError(f"cid error with '{cid}'")

        status = {
            'type': ship.loc['舰种'],  # 舰种
            'name': ship.loc['名称'],  # 船名
            'country': ship.loc['国籍'],  # 国籍
            'total_health': int(ship.loc['耐久']),  # 总耐久
            'health': int(ship.loc['耐久']),  # 当前耐久
            'fire': int(ship.loc['火力']),  # 火力
            'torpedo': int(ship.loc['鱼雷']),  # 鱼雷
            'armor': int(ship.loc['装甲']),  # 装甲
            'antiair': int(ship.loc['对空']),  # 对空
            'antisub': int(ship.loc['对潜']),  # 对潜
            'accuracy': int(ship.loc['命中']),  # 命中
            'evasion': int(ship.loc['回避']),  # 回避
            'recon': int(ship.loc['索敌']),  # 索敌
            'speed': float(ship.loc['航速']),  # 航速
            'range': int(ship.loc['射程']),  # 射程, 1: 短; 2: 中; 3: 长; 4: 超长
            'luck': int(ship.loc['幸运']),  # 幸运
            'equipnum': int(ship.loc['装备栏']),  # 装备栏
            'capacity': int(ship.loc['总搭载']),  # 总搭载
            'tag': ship.loc['标签'],  # 标签
        }

        if status['capacity'] != 0:
            status['load'] = []
            for i in range(1, status['equipnum'] + 1):
                status['load'].append(int(ship.loc['搭载' + str(i)]))

        status['skill'] = [
            ship.loc['技能1'],
            ship.loc['技能2']
        ]

        return status

    def get_enemy_ship_status(self, cid):
        ship_list = self.ship_data_enemy
        try:
            ship = ship_list.loc[cid]
        except:
            raise ValueError(f"cid error with '{cid}'")

        status = {
            'type': ship.loc['舰种'],  # 舰种
            'name': ship.loc['名称'],  # 船名
            'country': ship.loc['国籍'],  # 国籍
            'total_health': int(ship.loc['耐久']),  # 总耐久
            'health': int(ship.loc['耐久']),  # 当前耐久
            'fire': int(ship.loc['火力']),  # 火力
            'torpedo': int(ship.loc['鱼雷']),  # 鱼雷
            'armor': int(ship.loc['装甲']),  # 装甲
            'antiair': int(ship.loc['对空']),  # 对空
            'antisub': int(ship.loc['对潜']),  # 对潜
            'accuracy': int(ship.loc['命中']),  # 命中
            'evasion': int(ship.loc['回避']),  # 回避
            'recon': int(ship.loc['索敌']),  # 索敌
            'speed': float(ship.loc['航速']),  # 航速
            'range': int(ship.loc['射程']),  # 射程, 1: 短; 2: 中; 3: 长; 4: 超长
            'luck': int(ship.loc['幸运']),  # 幸运
            'capacity': int(ship.loc['总搭载']),  # 总搭载
        }

        if status['capacity'] != 0:
            status['load'] = []
            for i in range(1, 5):
                status['load'].append(int(ship.loc['搭载' + str(i)]))

        status['equip'] = []
        equip_list_0 = self.equip_data_enemy
        equip_list_1 = self.equip_data_friend
        for i in range(1, 5):
            equip = ship.loc['装备' + str(i)]
            if equip != '':
                try:
                    eid = equip_list_0[equip_list_0['名称'] == equip].index[0]
                except:
                    try:
                        eid = equip_list_1[equip_list_1['名称'] == equip].index[0]
                    except:
                        raise ValueError('装备不存在！')

                status['equip'].append(eid)
            else:
                status['equip'].append(equip)

        status['skill'] = [
            ship.loc['技能1'],
            ship.loc['技能2']
        ]
        return status

    def get_equip_status(self, eid):
        if eid[0] == '1':
            equip_list = self.equip_data_friend
        else:
            equip_list = self.equip_data_enemy

        try:
            equip = equip_list.loc[eid]
        except:
            raise ValueError(f"eid error with '{eid}'")
        name_list = ['耐久', '火力', '鱼雷', '装甲', '对潜', '索敌',
                     '命中', '射程', '闪避', '幸运', '轰炸', '对空',
                     '对空倍率', '对空补正', '铝耗',
                     # '导弹突防', '导弹拦截', '导弹防护',
                     ]
        eng_name_list = ['health', 'fire', 'torpedo', 'armor', 'antisub', 'recon',
                         'accuracy', 'range', 'evasion', 'luck', 'bomb', 'antiair',
                         'aa_scale', 'aa_coef', 'al_cost',
                         # 'missile_atk', 'missile_def', 'missile_protect',
                         ]

        status = {
            'type': equip.loc['种类'],  # 种类
            'name': equip.loc['名称'],  # 装备名
            'skill': equip.loc['特效'],  # 特殊效果
        }

        if equip.loc['特效数值'] != '':
            status['skill_value'] = [
                float(x) for x in equip.loc['特效数值'].split(',')  # 特效数值
            ]
        else:
            status['skill_value'] = ''

        for i, name in enumerate(name_list):
            value = equip.loc[name]
            if value != '':
                if name in ['对空倍率', '对空补正']:
                    status[eng_name_list[i]] = float(value)
                else:
                    status[eng_name_list[i]] = int(value)
            elif name == '对空倍率':
                status['aa_scale'] = 1.

        return status
