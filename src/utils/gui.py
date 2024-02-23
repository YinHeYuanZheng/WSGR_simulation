# -*- coding:utf-8 -*-
# Author:爱摸鱼的萌新
# env:py39
# 类名使用大驼峰
# 变量名、方法名使用小驼峰

import os
import sys
import copy
import numpy as np
import time

curDir = os.path.dirname(__file__)
srcDir = os.path.join(curDir, '..')
sys.path.append(srcDir)

from src.utils.loadConfig import load_config
from src.utils.loadDataset import Dataset
from src.utils.runUtil import *
from src.wsgr.wsgrTimer import timer
from src.wsgr.formulas import *
from tkinter import *
from tkinter.ttk import *


class MainDlg():
    dependDir = os.path.join(os.path.dirname(srcDir), '../../depend')
    dataFile = os.path.join(dependDir, r'ship\database.xlsx')
    dataBase = Dataset(dataFile)  # 全部舰船、装备数据

    def __init__(self):
        self.loadData()

    # 显示对话框
    def showDlg(self):
        self.root = Tk()
        self.root.title('战舰少女R战斗模拟器')  # 标题
        self.root.geometry('1125x485')  # 界面尺寸

        # 友方选项
        self.showFriendChioce()

        # 敌方选项
        self.showEnemyChioce()

        # 选择：阶段
        staticText = Label(self.root, text='阶段:', anchor="e")
        staticText.place(x=720, y=5, height=25, width=30)
        self.phaseComboText = StringVar()
        phaseCombo = Combobox(self.root, textvariable=self.phaseComboText, values=self.phaseList)
        phaseCombo.place(x=750, y=5, height=25, width=110)

        # 输入：模拟次数
        staticText = Label(self.root, text='模拟次数:', anchor="e")
        staticText.place(x=865, y=5, height=25, width=60)
        self.simulationTimesEntry = Entry(self.root)
        self.simulationTimesEntry.place(x=925, y=5, height=25, width=100)
        self.simulationTimesEntry.insert(END, 1000)

        # 按钮：开始模拟
        self.simulationButton = Button(self.root, text='开始模拟', command=self.simulate)
        self.simulationButton.place(x=1030, y=5, height=25, width=90)

        # 输出：模拟结果
        self.resultText = Text(self.root)  # 用于显示结果
        self.resultText.place(x=720, y=30, height=450, width=400)

        # 打开对话框
        self.root.mainloop()

    # 加载数据
    def loadData(self):
        # configDir = os.path.join(os.path.dirname(srcDir), 'config')
        # mapDir = os.path.join(self.dependDir, r'map')
        self.shipIDFromName = {}  # 友方船名->CID
        self.equipIDFromName = {}  # 友方装备名->EID
        self.enemyIDFromName = {}  # 敌方船名->CID
        self.enemyEquipIDFromName = {}  # 敌方装备名->EID
        self.shipNameList = []  # 友方船名列表
        self.equipNameList = []  # 友方装备名列表
        self.enemyNameList = []  # 敌方船名列表
        self.enemyEquipNameList = []  # 敌方装备名列表
        # 获取全部友方舰船名
        counts = 0
        for index, row in self.dataBase.ship_data_0.iterrows():
            shipName = self.dataBase.ship_data_0.values[counts][1]
            self.shipNameList.append(shipName)
            self.shipIDFromName[shipName] = self.dataBase.ship_data_0.index[counts]
            counts = counts + 1
        counts = 0
        for index, row in self.dataBase.ship_data_1.iterrows():
            shipName = self.dataBase.ship_data_1.values[counts][1] + '-改'
            self.shipNameList.append(shipName)
            self.shipIDFromName[shipName] = self.dataBase.ship_data_1.index[counts]
            counts = counts + 1
            # 获取全部友方装备名
        counts = 0
        for row in self.dataBase.equip_data_friend.iterrows():
            equipName = self.dataBase.equip_data_friend.values[counts][1]
            self.equipNameList.append(equipName)
            self.equipIDFromName[equipName] = self.dataBase.equip_data_friend.index[counts]
            counts = counts + 1
        # 获取全部敌方舰船名
        counts = 0
        for index, row in self.dataBase.ship_data_enemy.iterrows():
            enemyName = self.dataBase.ship_data_enemy.values[counts][1]
            self.enemyNameList.append(self.dataBase.ship_data_enemy.values[counts][1])
            self.enemyIDFromName[enemyName] = self.dataBase.ship_data_enemy.index[counts]
            counts = counts + 1
            # 获取全部敌方装备名
        counts = 0
        for row in self.dataBase.equip_data_enemy.iterrows():
            equipName = self.dataBase.equip_data_enemy.values[counts][1]
            self.enemyEquipNameList.append(equipName)
            self.enemyEquipIDFromName[equipName] = self.dataBase.equip_data_enemy.index[counts]
            counts = counts + 1
        # 可选战斗阶段 键值对
        self.phaseMap = {
            '全阶段': 'AllPhase',
            '准备阶段': 'PreparePhase',
            'buff阶段': 'BuffPhase',
            '支援攻击': 'SupportPhase',
            '昼战阶段': 'DaytimePhase',
            '航空战阶段': 'AirPhase',
            '梯形锁定': 'TLockPhase',
            '导弹战': 'MissilePhase',
            '远程导弹支援': 'LongMissilePhase',
            '开幕导弹': 'FirstMissilePhase',
            '闭幕导弹': 'SecondMissilePhase',
            '先制反潜': 'AntiSubPhase',
            '鱼雷战': 'TorpedoPhase',
            '先制鱼雷': 'FirstTorpedoPhase',
            '闭幕鱼雷': 'SecondTorpedoPhase',
            '炮击战': 'ShellingPhase',
            '首轮炮击': 'FirstShellingPhase',
            '次轮炮击': 'SecondShellingPhase',
            '夜战': 'DaytimePhase',
        }
        self.phaseList = []
        for name in self.phaseMap:
            self.phaseList.append(name)

    # 显示友方选项组合框
    def showFriendChioce(self):
        self.shipCombText = []  # 友方舰船名
        self.shipComb = []  # 友方舰船组合框
        self.equipCombText = []  # 友方舰船装备名
        self.equipComb = []  # 友方舰船装备组合框
        for pos in range(6):
            self.shipCombText.append(StringVar())
            self.shipComb.append(Combobox(self.root, textvariable=self.shipCombText[pos], values=self.shipNameList))
            equipCombTextTemp = []
            equipCombTemp = []
            for count in range(4):
                equipCombTextTemp.append(StringVar())
                equipCombTemp.append(
                    Combobox(self.root, textvariable=equipCombTextTemp[count], values=self.equipNameList))
            self.equipCombText.append(equipCombTextTemp)
            self.equipComb.append(equipCombTemp)
            staticText = Label(self.root, text=str(pos) + '号位:')
            staticText.place(x=5, y=5 + 80 * pos, height=25, width=40)
            self.shipComb[pos].place(x=50, y=5 + 80 * pos, height=25, width=200)
            self.equipComb[pos][0].place(x=50, y=30 + 80 * pos, height=25, width=150)
            self.equipComb[pos][1].place(x=205, y=30 + 80 * pos, height=25, width=150)
            self.equipComb[pos][2].place(x=50, y=55 + 80 * pos, height=25, width=150)
            self.equipComb[pos][3].place(x=205, y=55 + 80 * pos, height=25, width=150)

    # 显示敌方组合框
    def showEnemyChioce(self):
        self.enemyCombText = []  # 敌方舰船名
        self.enemyComb = []  # 敌方舰船组合框
        self.enemyEquipCombText = []  # 敌方舰船装备名
        self.enemyEquipComb = []  # 敌方舰船装备组合框
        for pos in range(6):
            self.enemyCombText.append(StringVar())
            self.enemyComb.append(Combobox(self.root, textvariable=self.enemyCombText[pos], values=self.enemyNameList))
            enemyEquipCombTextTemp = []
            enemyEquipCombTemp = []
            for count in range(4):
                enemyEquipCombTextTemp.append(StringVar())
                enemyEquipCombTemp.append(
                    Combobox(self.root, textvariable=enemyEquipCombTextTemp[count], values=self.enemyEquipNameList))
            self.enemyEquipCombText.append(enemyEquipCombTextTemp)
            self.enemyEquipComb.append(enemyEquipCombTemp)
            staticText = Label(self.root, text=str(pos) + '号位:')
            staticText.place(x=365, y=5 + 80 * pos, height=25, width=40)
            self.enemyComb[pos].place(x=410, y=5 + 80 * pos, height=25, width=200)
            self.enemyEquipComb[pos][0].place(x=410, y=30 + 80 * pos, height=25, width=150)
            self.enemyEquipComb[pos][1].place(x=565, y=30 + 80 * pos, height=25, width=150)
            self.enemyEquipComb[pos][2].place(x=410, y=55 + 80 * pos, height=25, width=150)
            self.enemyEquipComb[pos][3].place(x=565, y=55 + 80 * pos, height=25, width=150)

    # 显示结果       
    def showResult(self, strResult):
        self.resultText.delete("1.0", END)  # 清空原来的结果
        self.resultText.insert(END, strResult)  # 显示新结果
        self.resultText.update()  # 立刻刷新显示

    # 模拟战斗按钮
    def simulate(self):
        # 读取界面当前信息
        shipID = []  # 我方舰队ID
        equipID = []  # 我方舰队装备ID
        enemyID = []  # 敌方舰队ID
        enemyEquipID = []  # 敌方舰队装备ID
        for shipPos in range(6):
            shipID.append(self.getShipName(shipPos))
            enemyID.append(self.getEnemyName(shipPos))
            equipIDTemp = []
            enemyEquipIDTemp = []
            for count in range(4):
                equipIDTemp.append(self.getEquipName(shipPos, count))
                enemyEquipIDTemp.append(self.getEnemyEquipName(shipPos, count))
            equipID.append(equipIDTemp)
            enemyEquipID.append(enemyEquipIDTemp)

        # 开始模拟
        simulationTotalTimes = self.getSimulationTimes()  # 模拟次数
        currentPhase = self.getPhase()  # 模拟阶段
        for simulationTimes in range(simulationTotalTimes):
            # 模拟一次，在这里加入计算过程，获取计算结果
            time.sleep(0.001)  # 等待1ms，不需要这句话，只是假装在计算

            # 显示模拟结果
            self.showResult('第' + str(simulationTimes) + '次：' + '先随便写一点凑合\n')

    # 按cid设置我方舰船名
    def setShipName(self, shipID, shipPos):
        if shipPos < 0 or shipPos > 5:
            return False
        self.shipCombText[shipPos].set(self.dataBase.get_friend_ship_status(shipID).name)
        return True

    # 读取我方舰船名，返回cid
    def getShipName(self, shipPos):
        if shipPos < 0 or shipPos > 5:
            return None
        return self.shipIDFromName.get(self.shipCombText[shipPos].get())

    # 按eid设置我方装备名
    def setEquipName(self, equipID, shipPos, equipPos):
        if shipPos < 0 or shipPos > 5:
            return False
        if equipPos < 0 or equipPos > 3:
            return False
        self.equipCombText[shipPos][equipPos].set(self.dataBase.get_equip_status(equipID).name)
        return True

    # 读取我方装备名，返回eid
    def getEquipName(self, shipPos, equipPos):
        if shipPos < 0 or shipPos > 5:
            return None
        if equipPos < 0 or equipPos > 3:
            return None
        return self.equipIDFromName.get(self.equipCombText[shipPos][equipPos].get())

    # 按cid设置敌方舰船名
    def setEnemyName(self, enemyID, enemyPos):
        if enemyPos < 0 or enemyPos > 5:
            return False
        self.enemyCombText[enemyPos].set(self.dataBase.get_enemy_ship_status(enemyID).name)
        return True

    # 读取敌方舰船名，返回cid
    def getEnemyName(self, enemyPos):
        if enemyPos < 0 or enemyPos > 5:
            return None
        return self.enemyIDFromName.get(self.enemyCombText[enemyPos].get())

    # 按eid设置敌方装备名
    def setEnemyEquipName(self, enemyEquipID, enemyPos, equipPos):
        if enemyPos < 0 or enemyPos > 5:
            return False
        if equipPos < 0 or equipPos > 3:
            return False
        self.enemyEquipCombText[enemyPos][equipPos].set(self.dataBase.get_equip_status(enemyEquipID).name)
        return True

    # 读取敌方装备名，返回eid
    def getEnemyEquipName(self, enemyPos, equipPos):
        if enemyPos < 0 or enemyPos > 5:
            return None
        if equipPos < 0 or equipPos > 3:
            return None
        return self.enemyEquipIDFromName.get(self.enemyEquipCombText[enemyPos][equipPos].get())

    # 读取当前阶段
    def getPhase(self):
        return self.phaseMap.get(self.phaseComboText.get())

    # 读取模拟次数
    def getSimulationTimes(self):
        return int(self.simulationTimesEntry.get())


if __name__ == '__main__':
    mainDlg = MainDlg()
    mainDlg.showDlg()
