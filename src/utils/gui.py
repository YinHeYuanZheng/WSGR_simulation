# -*- coding:utf-8 -*-
# Author:银河远征、爱摸鱼的萌新
# env:py38
# 类名使用大驼峰
# 变量名、方法名使用小驼峰

import os
import sys
import copy
import numpy as np
import yaml
import threading

curDir = os.path.dirname(__file__)
srcDir = os.path.dirname(curDir)
sys.path.append(srcDir)

from src.utils.loadConfig import load_xml, load_yaml, load_config
from src.utils.loadDataset import Dataset
from src.utils.runUtil import *
from src.utils.battleUtil import *
from src.wsgr.wsgrTimer import timer
from src.wsgr.formulas import *
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, filedialog


class App:
    configDir = os.path.join(os.path.dirname(srcDir), 'config')
    dependDir = os.path.join(os.path.dirname(srcDir), 'depend')
    mapDir = os.path.join(dependDir, r'map')
    dataFile = os.path.join(dependDir, r'ship/database.xlsx')
    data = Dataset(dataFile)  # 全部舰船、装备数据

    def __init__(self):
        self.root = Tk()
        self.root.title('战舰少女R战斗模拟器')  # 标题
        # self.root.geometry('1125x485')  # 界面尺寸
        self.mainloop = self.root.mainloop

        self.mainDlg = MainDlg(self.root, self)
        self.getBattleConfig = self.mainDlg.getBattleConfig
        self.getSimulationSettings = self.mainDlg.getSimulationSettings

        self.simulation_thread = None
        self.stop_event = threading.Event()

    def simulation(self):
        if self.simulation_thread is not None and self.simulation_thread.is_alive():
            return

        self.stop_event.clear()
        self.simulation_thread = threading.Thread(target=self._run_simulation)
        self.simulation_thread.daemon = True
        self.simulation_thread.start()

    def _run_simulation(self):
        self.mainDlg.frameResult.clear()

        # 获取战斗设置
        battleConfig = self.getBattleConfig()
        if battleConfig is None:
            return
        epoch, battleNum, fun = self.getSimulationSettings()

        # 运行并输出结果
        sys.stdout = self.mainDlg.frameResult.resultTextBox
        timer_init = timer()  # 创建时钟
        battle = load_config(battleConfig, self.mapDir, self.data, timer_init)
        print('')
        set_supply(battle, battleNum)
        prebattle_info(battle)
        print('')
        fun(battle, epoch, stop_event=self.stop_event)
        sys.stdout = sys.__stdout__

    def stop_simulation(self):
        if self.simulation_thread is not None and self.simulation_thread.is_alive():
            self.stop_event.set()

    def saveFile(self, outfile=None):
        if outfile is None:
            outfile = os.path.join(self.configDir, 'save/gui_config.yaml')
        elif outfile.endswith('.xml'):
            messagebox.showerror('错误', '保存文件后缀必须为 .yaml')
            return
        battleConfig = self.getBattleConfig()
        if battleConfig is not None:
            with open(outfile, 'w') as f:
                yaml.safe_dump(battleConfig, f, sort_keys=False)

    def openFile(self, infile):
        try:
            if infile.endswith('.xml'):
                battleConfig = load_xml(infile, self.mapDir)
            elif infile.endswith('.yaml'):
                battleConfig = load_yaml(infile, self.mapDir)
            else:
                messagebox.showerror('错误', f"未许可的文件后缀'{os.path.splitext(infile)[1]}'")
                return
        except FileNotFoundError as e:
            messagebox.showerror('错误', f"文件不存在: {e}")
            return
        except:
            messagebox.showerror('错误', '格式不符合要求，文件读取失败!')
            return

        self.mainDlg.setBattleConfig(battleConfig)


class MainDlg(Frame):
    """用户界面"""
    def __init__(self, master: Tk, app: App):
        super().__init__(master)
        self.master = master
        self.app = app
        self.pack()

        # 界面分区
        self.menubar = None
        self.frameFriend = None
        self.frameEnemy = None
        self.frameSettings = None
        self.frameResult = None

        # 复制指令
        self.saveFile = self.app.saveFile
        self.openFile = self.app.openFile
        self.simulation = self.app.simulation
        self.stop = self.app.stop_simulation

        # 建立友方船名-cid互查字典
        self.friendNameDict = {name: cid for name, cid in
                               zip(self.app.data.ship_data_0['名称'],
                                   self.app.data.ship_data_0.index)}
        self.friendNameDict.update(
            {name + '-改': cid for name, cid in
             zip(self.app.data.ship_data_1['名称'],
                 self.app.data.ship_data_1.index)}
        )

        # 建立装备名-eid互查字典
        self.equipNameDict = {name: eid for name, eid in
                              zip(self.app.data.equip_data_friend['名称'],
                                  self.app.data.equip_data_friend.index)}

        # 建立敌方船名-cid互查字典
        self.enemyNameDict = {f'{name}-{cid}': cid for name, cid in
                              zip(self.app.data.ship_data_enemy['名称'],
                                  self.app.data.ship_data_enemy.index)}

        self.createWidgets()
        self.createBindings()

    def createWidgets(self):
        self.createMenubar()  # 菜单栏
        self.createFriendSelect()  # 我方舰队设置模块
        self.createSettings()  # 模拟设置模块
        self.createEnemySelect()  # 敌方舰队设置模块
        self.createResult()  # 结果显示模块

    def createBindings(self):
        """绑定全局事件"""
        # 打开
        self.master.bind('<Control-o>', lambda event: self.openFileDialog())
        self.master.bind('<Control-O>', lambda event: self.openFileDialog())
        # 保存
        self.master.bind('<Control-s>', lambda event: self.saveFile())
        self.master.bind('<Control-S>', lambda event: self.saveFile())
        # 另存为
        self.master.bind('<Control-Shift-s>', lambda event: self.saveAsDialog())
        self.master.bind('<Control-Shift-S>', lambda event: self.saveAsDialog())
        # 清除
        self.master.bind('<Control-d>', lambda event: self.clearAll())
        self.master.bind('<Control-D>', lambda event: self.clearAll())
        # 退出
        self.master.bind('<Alt-x>', lambda event: self.quit())
        self.master.bind('<Alt-X>', lambda event: self.quit())

    def createMenubar(self):
        """创建菜单栏"""
        self.menubar = Menubar(self)
        self.master.config(menu=self.menubar)

    def createFriendSelect(self):
        """我方舰队设置模块"""
        self.frameFriend = FrameFriend(self, self.friendNameDict, self.equipNameDict)
        self.frameFriend.grid(row=0, column=0, rowspan=2,
                              padx=10, pady=10,
                              ipadx=3, ipady=2,
                              sticky='NS')

    def createSettings(self):
        """模拟设置模块"""
        self.frameSettings = FrameSettings(self)
        self.frameSettings.grid(row=0, column=1,
                                padx=10, pady=10, ipady=4,
                                sticky='NSWE')

    def createEnemySelect(self):
        """敌方舰队设置模块"""
        self.frameEnemy = FrameEnemy(self, self.enemyNameDict)
        self.frameEnemy.grid(row=1, column=1,
                             padx=10, pady=10,
                             ipadx=3, ipady=4,
                             sticky='NSWE')

    def createResult(self):
        """结果显示模块"""
        self.frameResult = FrameResult(self)
        self.frameResult.grid(row=0, column=2, rowspan=2,
                              padx=10, pady=10,
                              sticky='NS')

    def getBattleConfig(self) -> dict or None:
        battleConfig = {
            'battle_type': self.frameSettings.battleType.__name__,
            'friend_fleet': self.frameFriend.getFleetDict(),
            'enemy_fleet': self.frameEnemy.getFleetDict()
        }
        if battleConfig['friend_fleet'] is None or \
                battleConfig['enemy_fleet'] is None:
            return None
        return battleConfig

    def setBattleConfig(self, battleConfig: dict) -> None:
        try:
            friendDict = battleConfig['friend_fleet']
            enemyDict = battleConfig['enemy_fleet']
            battleType = battleConfig['battle_type']
        except KeyError:
            messagebox.showerror('错误', '配置文件格式错误！')
            return
        self.frameFriend.setConfig(friendDict)
        self.frameEnemy.setConfig(enemyDict)
        self.frameSettings.setBattleType(battleType)

    def getSimulationSettings(self):
        return (self.frameSettings.epoch,
                self.frameSettings.battleNum,
                self.frameSettings.fun)

    def clearAll(self):
        if messagebox.askyesno('战舰少女R战斗模拟器', '是否清除全部内容？'):
            self.frameFriend.clear()  # 清除舰船设定
            self.frameSettings.clear()  # 清除模拟设定
            self.frameEnemy.clear()  # 清除敌舰选择
            self.frameResult.clear()  # 清除结果显示

    def openFileDialog(self):
        """打开文件选择对话框并处理选择的文件"""
        # 打开文件对话框
        file_path = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[
                ("配置文件", "*.xml;*.yaml"),
                ("所有文件", "*.*"),
            ],
            initialdir=App.configDir  # 从用户目录开始
        )
        # 如果用户选择了文件（没有取消）
        if file_path:
            self.openFile(file_path)

    def saveAsDialog(self):
        """另存为文件对话框"""
        file_path = filedialog.asksaveasfilename(
            title="另存为",
            defaultextension=".yaml",
            filetypes=[
                ("yaml文件", "*.yaml"),
                ("所有文件", "*.*")
            ],
            initialdir=App.configDir,  # 从用户目录开始
            initialfile="new_config.yaml"  # 默认文件名
        )

        # 如果用户选择了保存路径（没有取消）
        if file_path:
            self.saveFile(file_path)


class Menubar(Menu):
    """菜单栏"""

    def __init__(self, master: MainDlg):
        super().__init__(master)
        self.master = master

        # 复制指令
        self.saveFile = master.saveFile
        self.openFile = master.openFile
        self.openFileDialog = master.openFileDialog
        self.saveAsDialog = master.saveAsDialog
        self.clear = master.clearAll

        # 菜单变量
        self.fileMenu = None
        self.openMenu = None

        # 生成菜单
        self.createFileMenu()

    def createFileMenu(self):
        """文件菜单"""
        self.fileMenu = Menu(self, tearoff=False)
        self.add_cascade(label="文件", menu=self.fileMenu)

        # 文件菜单内容
        self.openMenu = Menu(self.fileMenu, tearoff=False)
        self.fileMenu.add_cascade(label="快捷打开...", menu=self.openMenu)
        self.createOpenMenu()  # 打开菜单内容
        self.fileMenu.add_command(label="打开", command=self.openFileDialog, accelerator="Ctrl+O")
        self.fileMenu.add_command(label="保存", command=self.saveFile, accelerator="Ctrl+S")
        self.fileMenu.add_command(label="另存为...", command=self.saveAsDialog, accelerator="Ctrl+Shift+S")
        self.fileMenu.add_command(label="清除", command=self.clear, accelerator="Ctrl+D")
        self.fileMenu.add_separator()  # 分割线
        self.fileMenu.add_command(label="退出", command=self.quit, accelerator="Alt+X")

    def createOpenMenu(self):
        """创建打开菜单，显示所有记录文件"""
        saveDir = os.path.join(App.configDir, 'save')
        if not os.path.exists(saveDir):
            os.mkdir(saveDir)

        fileList = os.listdir(path=saveDir)
        yamlList = [fname for fname in fileList if fname.endswith('.yaml')]
        if len(yamlList):
            for fname in yamlList:
                self.openMenu.add_command(label=os.path.splitext(fname)[0],
                                          command=lambda x=os.path.join(saveDir, fname): self.openFile(x))
        else:
            self.openMenu.add_command(label="（无存档）")


class FrameFriend(LabelFrame):
    """我方舰队设置模块"""
    formDict = {
        '单纵阵': 1,
        '复纵阵': 2,
        '轮形阵': 3,
        '梯形阵': 4,
        '单横阵': 5,
    }
    strategyDict = {
        1: {
            '雷击熟练': '111',
            '炮击训练': '112',
            '拦阻射击': '113',
            '效力射': '211',
            '数据交互': '212',
            '弹跳攻击': '213',
            '穿甲航弹': '311',
            '全甲板突击': '312',
            '穿甲榴弹': '313'
        },
        2: {
            '对海警戒哨': '121',
            '前哨援护': '122',
            '过穿': '123',
            '硬化装甲': '221',
            '编队援护': '222',
            '防空弹幕': '223',
            '探照灯警戒': '321',
            '护航援护': '322',
            '装甲甲板': '323'
        },
        3: {
            '大角度规避': '131',
            '雁行雷击': '132',
            '交互射击': '231',
            '硬被帽': '232',
            '炮塔后备弹': '233',
            '改良被帽弹': '331',
            '照明弹校正': '332',
            '对空预警': '333'
        }
    }

    def __init__(self, master, shipNameDict, equipNameDict):
        super().__init__(master, text='我方舰队设置')
        self.master = master
        self.shipNameDict = shipNameDict
        self.shipNameList = list(shipNameDict)
        self.shipCidList = list(shipNameDict.values())
        self.equipNameDict = equipNameDict
        self.equipNameList = list(equipNameDict)
        self.equipEidList = list(equipNameDict.values())

        self.shipComb = np.empty(6, dtype=object)  # 友方舰船组合框
        self.affectionEntry = np.empty(6, dtype=object)  # 友方舰船好感度输入框
        self.skillComb = np.empty(6, dtype=object)  # 友方舰船技能组合框
        self.strategyComb = np.empty((6, 3), dtype=object)  # 友方舰船战术组合框
        self.equipComb = np.empty((6, 4), dtype=object)  # 友方舰船装备组合框
        self.createFrame()

    def createFrame(self):
        formCombLabel = Label(self, text=f'阵型：')
        formCombLabel.grid(row=0, column=0, padx=5, pady=2, sticky='E')
        self.formComb = Combobox(self, width=28, height=8,
                                 state='pressed',
                                 values=list(self.formDict),
                                 textvariable=StringVar())
        self.formComb.set('梯形阵')
        self.formComb.grid(row=0, column=1, columnspan=2, sticky='WE')

        for i in range(6):
            if i == 0:
                staticLabel = Label(self, text=f'旗舰：')
            else:
                staticLabel = Label(self, text=f'{i + 1}号位：')
            staticLabel.grid(row=3*i+1, column=0, padx=5, sticky='E')

            # 舰船设置
            self.shipComb[i] = Combobox(self,
                                        width=28, height=8,
                                        state='pressed',
                                        values=self.shipNameList,
                                        textvariable=StringVar())
            self.shipComb[i].bind('<<ComboboxSelected>>',
                                  lambda event, x=i: self.setShip(x))  # 选择响应
            self.shipComb[i].bind("<KeyRelease>",
                                  lambda event, x=i: self.inputName(x))  # 输入响应
            self.shipComb[i].bind("<FocusOut>",
                                  lambda event, x=i: self.deleteName(x))  # 在输入为空时失去焦点，清空当前行
            self.shipComb[i].grid(row=3*i+1, column=1, columnspan=2, sticky='WE')

            # 好感设置
            affectionLabel = Label(self, text=f'好感度：')
            affectionLabel.grid(row=3*i+1, column=3, padx=5, sticky='E')
            self.affectionEntry[i] = Entry(self, width=15,
                                           textvariable=StringVar())
            self.affectionEntry[i].grid(row=3*i+1, column=4, sticky='WE')
            self.affectionEntry[i].insert(0, '200')
            self.affectionEntry[i].config(state="disabled")

            # 舰船技能
            self.skillComb[i] = Combobox(self,
                                         width=13, height=8,
                                         state='disabled',
                                         values=['无技能', '1', '2'],
                                         textvariable=StringVar())
            self.skillComb[i].set('技能')
            self.skillComb[i].grid(row=3*i+2, column=1)

            # 舰船战术
            for j in range(3):
                self.strategyComb[i, j] = Combobox(self,
                                                   width=13, height=8,
                                                   state='disabled',
                                                   textvariable=StringVar())
                self.strategyComb[i, j].set(f'{10 * j + 90}级战术')
                self.strategyComb[i, j].grid(row=3*i+2, column=j+2)
            self.strategyComb[i, 0]['values'] = list(self.strategyDict[1])
            self.strategyComb[i, 1]['values'] = list(self.strategyDict[2])
            self.strategyComb[i, 2]['values'] = list(self.strategyDict[3])

            # 装备设置
            for j in range(4):
                self.equipComb[i, j] = Combobox(self,
                                                width=13, height=8,
                                                state='disabled',
                                                values=self.equipNameList,
                                                textvariable=StringVar())
                self.equipComb[i, j].bind("<KeyRelease>",
                                          lambda event, x=(i, j): self.inputEquip(x))  # 输入响应
                self.equipComb[i, j].bind("<FocusOut>",
                                          lambda event, x=(i, j): self.deleteEquip(x))  # 在输入为空时失去焦点，清空当前格

                self.equipComb[i, j].set(f'装备{j + 1}')
                self.equipComb[i, j].grid(row=3*i+3, column=j+1)

    def setShip(self, row):
        """选择舰船后解锁装备可选项"""
        shipName = self.shipComb[row].get()
        if shipName != '':
            cid = self.shipNameDict[shipName]
            status = App.data.get_friend_ship_status(cid)

            # 技能选项设置
            skillList = status['skill']
            skillVarList = ['无技能']
            from src import skillCode
            for j in range(2):
                sid = skillList[j]
                if sid != '':
                    sid = 'sid' + sid
                    skillName = getattr(skillCode, sid).name
                    skillVarList.append(skillName)
            self.skillComb[row].config(state='normal')
            self.skillComb[row]['values'] = skillVarList
            self.skillComb[row].set('无技能')

            # 好感度设置
            self.affectionEntry[row].config(state="normal")

            # 战术选项设置
            for j in range(3):
                self.strategyComb[row, j].config(state='normal')

            # 装备选项设置
            equipnum = status['equipnum']
            for j in range(4):
                if j < equipnum:
                    self.equipComb[row, j].config(state='normal')
                else:
                    self.equipComb[row, j].set(f'装备{j + 1}')
                    self.equipComb[row, j].config(state="disabled")
                    self.equipComb[row, j]['values'] = self.equipNameList

    def inputName(self, row):
        """
        输入框内容变化后重新设置选择框内可选项，使其只包含包含输入内容
        :param row: 控件所在行
        """
        input_str = self.shipComb[row].get()
        new_select_list = [name for name in self.shipNameList if input_str in name]
        combobox_tmp = self.shipComb[row]
        if len(new_select_list):
            combobox_tmp['values'] = new_select_list
        else:
            combobox_tmp['values'] = self.shipNameList

    def inputEquip(self, loc):
        input_str = self.equipComb[loc].get()
        new_select_list = [name for name in self.equipNameList if input_str in name]
        combobox_tmp = self.equipComb[loc]
        if len(new_select_list):
            combobox_tmp['values'] = new_select_list
        else:
            combobox_tmp['values'] = self.equipNameList

    def deleteName(self, row):
        """
        输入框失去焦点时调用，如果内容为空，重置当前行
        :param row: 控件所在行
        """
        shipName = self.shipComb[row].get()
        if shipName == '':
            self.clearRow(row)  # 重置所有组件

    def deleteEquip(self, loc):
        equipName = self.equipComb[loc].get()
        if equipName == '':
            self.equipComb[loc].set(f'装备{loc[1] + 1}')

    def clearRow(self, row):
        """
        重置一行舰船设定
        :param row: 控件所在行
        """
        self.shipComb[row]['values'] = self.shipNameList
        self.shipComb[row].set('')
        self.skillComb[row]['values'] = ['无技能']
        self.skillComb[row].set('技能')
        self.skillComb[row].config(state="disabled")
        self.affectionEntry[row].delete(0, 'end')
        self.affectionEntry[row].insert(0, '200')
        self.affectionEntry[row].config(state="disabled")

        for j in range(3):
            self.strategyComb[row, j].set(f'{10 * j + 90}级战术')
            self.strategyComb[row, j].config(state="disabled")
            self.strategyComb[row, j]['values'] = list(self.strategyDict[j+1])
        for j in range(4):
            self.equipComb[row, j].set(f'装备{j + 1}')
            self.equipComb[row, j].config(state="disabled")
            self.equipComb[row, j]['values'] = self.equipNameList

    def clear(self):
        self.formComb.set('梯形阵')
        for i in range(6):
            self.clearRow(i)

    def getFleetDict(self) -> dict or None:
        if not self.checkShipOrder():
            return None

        fleetDict = {'side': 1,
                     'form': self.formDict[self.formComb.get()]}
        shipList = []
        for i in range(6):
            if self.shipComb[i].get() == '':
                break
            shipDict = {
                'loc': i + 1,
                'cid': self.shipNameDict[self.shipComb[i].get()],
                'level': 110,
                'affection':
                    max(min(int(self.affectionEntry[i].get()), 200), 0)  # 好感度范围0-200
                    if self.affectionEntry[i].get() != ''
                    else 200,  # 好感度为空时默认200
                'skill': self.skillComb[i].current(),
                'equipment': [
                    {'loc': j + 1,
                     'eid': self.equipNameDict[self.equipComb[i, j].get()]}
                    for j in range(4)
                    if self.equipComb[i, j].get() != f'装备{j + 1}'
                ],
                'strategy': [
                    {'stid': self.strategyDict[j + 1][self.strategyComb[i, j].get()],
                     'level': 3}  # todo 可从设置更改战术等级
                    for j in range(3)
                    if self.strategyComb[i, j].get() != f'{10 * j + 90}级战术'
                ]
            }
            shipList.append(shipDict)

        fleetDict['ships'] = shipList
        return fleetDict

    def setConfig(self, fleetDict):
        self.clear()
        form = int(fleetDict['form'])
        self.formComb.current(form - 1)
        for i, shipDict in enumerate(fleetDict['ships']):
            cid = shipDict['cid']
            self.shipComb[i].current(self.shipCidList.index(cid))
            self.setShip(i)
            self.skillComb[i].current(int(shipDict['skill']))

            affection = shipDict['affection']
            self.affectionEntry[i].delete(0, 'end')
            self.affectionEntry[i].insert(0, affection)

            for eDict in shipDict['equipment']:
                eid = eDict['eid']
                loc = int(eDict['loc'])  # 装备栏位
                idx = self.equipEidList.index(eid)
                self.equipComb[i, loc - 1].current(idx)

            for stDict in shipDict['strategy']:
                stid = stDict['stid']
                stLevel = int(stid[1])  # 战术等级
                idx = list(self.strategyDict[stLevel].values()).index(stid)
                self.strategyComb[i, stLevel - 1].current(idx)

    def checkShipOrder(self) -> bool:
        """检查舰队是否符合要求"""
        fleetCheck = np.array([self.shipComb[i].get() != '' for i in range(6)])
        shipLen = np.sum(fleetCheck)
        if np.sum(fleetCheck) == 0:
            messagebox.showinfo("提示", "友方舰队不能为空！")
            return False
        if not fleetCheck[0]:
            messagebox.showinfo("提示", "友方旗舰不能为空！")
            return False

        for i in range(5, -1, -1):
            if self.shipComb[i].get() != '' and i >= shipLen:
                messagebox.showinfo("提示", "请按顺序编辑友方舰队！")
                return False
        return True


class FrameEnemy(LabelFrame):
    """敌方舰队设置模块"""
    formDict = {
        '单纵阵': 1,
        '复纵阵': 2,
        '轮形阵': 3,
        '梯形阵': 4,
        '单横阵': 5,
    }

    def __init__(self, master, shipNameDict):
        super().__init__(master, text='敌方舰队设置')
        self.master = master
        self.shipNameDict = shipNameDict
        self.shipNameList = list(shipNameDict)
        self.shipCidList = list(shipNameDict.values())
        self.shipComb = np.empty(6, dtype=object)  # 敌方舰船组合框
        self.createFrame()

    def createFrame(self):
        formCombLabel = Label(self, text=f'阵型：')
        formCombLabel.grid(row=0, column=0, padx=5, pady=3, sticky='E')
        self.formComb = Combobox(self, width=18, height=8,
                                 state='pressed',
                                 values=list(self.formDict),
                                 textvariable=StringVar())
        self.formComb.set('梯形阵')
        self.formComb.grid(row=0, column=1, columnspan=2)

        for i in range(6):
            if i == 0:
                staticLabel = Label(self, text=f'旗舰：')
            else:
                staticLabel = Label(self, text=f'{i + 1}号位：')
            staticLabel.grid(row=i+1, column=0, padx=5, pady=3, sticky='E')

            # 舰船设置
            self.shipComb[i] = Combobox(self,
                                        width=18, height=8,
                                        state='pressed',
                                        values=self.shipNameList,
                                        textvariable=StringVar())
            self.shipComb[i].bind("<KeyRelease>",
                                  lambda event, x=i: self.inputName(x))  # 输入响应
            self.shipComb[i].grid(row=i+1, column=1)

    def inputName(self, row):
        """
        输入框内容变化后重新设置选择框内可选项，使其只包含包含输入内容
        :param row: 控件所在行
        """
        input_str = self.shipComb[row].get()
        new_select_list = [name for name in self.shipNameList if input_str in name]
        combobox_tmp = self.shipComb[row]
        if len(new_select_list):
            combobox_tmp['values'] = new_select_list
        else:
            combobox_tmp['values'] = self.shipNameList

    def clear(self):
        self.formComb.set('梯形阵')
        for i in range(6):
            self.shipComb[i].set('')

    def getFleetDict(self) -> dict or None:
        if not self.checkShipOrder():
            return None

        fleetDict = {'side': 0,
                     'form': self.formDict[self.formComb.get()]}
        shipList = []
        for i in range(6):
            if self.shipComb[i].get() == '':
                break
            shipDict = {'loc': i + 1,
                        'cid': self.shipNameDict[self.shipComb[i].get()],
                        'level': 110,
                        'affection': 50,
                        'skill': 1}
            shipList.append(shipDict)

        fleetDict['ships'] = shipList
        return fleetDict

    def setConfig(self, fleetDict):
        self.clear()
        form = int(fleetDict['form'])
        self.formComb.current(form - 1)
        for i, shipDict in enumerate(fleetDict['ships']):
            cid = shipDict['cid']
            self.shipComb[i].current(self.shipCidList.index(cid))

    def checkShipOrder(self):
        """检查舰队是否符合要求"""
        fleetCheck = np.array([self.shipComb[i].get() != '' for i in range(6)])
        shipLen = np.sum(fleetCheck)
        if np.sum(fleetCheck) == 0:
            messagebox.showinfo("提示", "敌方舰队不能为空！")
            return False
        if not fleetCheck[0]:
            messagebox.showinfo("提示", "敌方旗舰不能为空！")
            return False

        for i in range(5, -1, -1):
            if self.shipComb[i].get() != '' and i >= shipLen:
                messagebox.showinfo("提示", "请按顺序编辑敌方舰队！")
                return False
        return True


class FrameSettings(LabelFrame):
    """模拟设置模块"""
    phaseMap = {
        '全阶段': NormalBattle,
        '航空战': AirBattle,
        '夜战': NightBattle,
        '无夜战': DaytimeBattle,
        '仅航空战': OnlyAirBattle,
        '自定义': BattleUtil
    }
    funDict = {
        '胜率': run_victory,
        '总伤害': run_avg_damage,
        '消耗': run_supply_cost,
        '破损率': run_damaged
    }

    def __init__(self, master: MainDlg):
        super().__init__(master, text='模拟选项')
        self.master = master
        self.simulation = self.master.simulation
        self.stop = self.master.stop
        self.createFrame()

    def createFrame(self):
        epochLabel = Label(self, text='模拟次数：')
        epochLabel.grid(row=0, column=0, padx=5, pady=3, sticky='E')
        self.epochEntry = Entry(self, width=18,
                                textvariable=StringVar())
        self.epochEntry.insert(0, '1000')
        self.epochEntry.grid(row=0, column=1, padx=5, pady=3, sticky='WE')

        phaseLabel = Label(self, text='战斗阶段：')
        phaseLabel.grid(row=1, column=0, padx=5, pady=3, sticky='E')
        self.phaseComb = Combobox(self,
                                  width=16, height=8,
                                  state='pressed',
                                  values=list(self.phaseMap),
                                  textvariable=StringVar())
        self.phaseComb.set('全阶段')
        self.phaseComb.grid(row=1, column=1, padx=5, pady=3)

        battleNumLabel = Label(self, text='战斗轮次：')
        battleNumLabel.grid(row=2, column=0, padx=5, pady=3, sticky='E')
        self.battleNumComb = Combobox(self,
                                      width=16, height=8,
                                      state='pressed',
                                      values=['1', '2', '3', '4', '5'],
                                      textvariable=StringVar())
        self.battleNumComb.set('1')
        self.battleNumComb.grid(row=2, column=1, padx=3, pady=2)

        funLabel = Label(self, text='功能：')
        funLabel.grid(row=3, column=0, padx=5, pady=3, sticky='E')
        self.funComb = Combobox(self, width=16, height=8,
                                state='pressed',
                                values=list(self.funDict),
                                textvariable=StringVar())
        self.funComb.set('胜率')
        self.funComb.grid(row=3, column=1, padx=3, pady=2)

        self.startButton = Button(self, text='开始模拟', command=self.simulation)
        self.startButton.grid(row=4, columnspan=2, padx=5, pady=5)
        self.stopButton = Button(self, text='停止', command=self.stop)
        self.stopButton.grid(row=5, columnspan=2, padx=5, pady=2)

    @property
    def epoch(self):
        """模拟次数"""
        return int(self.epochEntry.get())

    @property
    def battleType(self):
        """战斗类型"""
        return self.phaseMap[self.phaseComb.get()]

    @property
    def battleNum(self):
        """战斗轮次"""
        return int(self.battleNumComb.get())

    @property
    def fun(self):
        """输出类型"""
        return self.funDict[self.funComb.get()]

    def setBattleType(self, battleType: str):
        from src.utils import battleUtil
        battleClass = getattr(battleUtil, battleType)
        try:
            idx = list(self.phaseMap.values()).index(battleClass)
            self.phaseComb.current(idx)
        except:
            self.phaseComb.current(0)
            raise ResourceWarning('Battle type not accepted, setting as default')

    def clear(self):
        # self.epochEntry.insert(0, '1000')
        # self.phaseComb.set('全阶段')
        # self.funComb.set('胜率')
        pass


class FrameResult(LabelFrame):
    """结果显示模块"""
    def __init__(self, master):
        super().__init__(master, text='模拟结果')
        self.master = master
        self.resultTextBox = TextRedirector(master=self, height=35, width=50)
        self.resultTextBox.grid(row=0, column=0, padx=5, pady=5)

    def clear(self):
        self.resultTextBox.delete("1.0", END)
        self.resultTextBox.update()


class TextRedirector(Text):
    """重定向系统输出到文本框"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def write(self, string: str):
        if string.startswith('\r'):
            self.delete('end-1c linestart', 'end-1c')
            self.insert(END, string[1:])
        else:
            self.insert(END, string)
        self.update()

    def flush(self):
        """ 保持与sys.stdout兼容 """
        pass


if __name__ == '__main__':
    app = App()
    # app.openFile(os.path.join(App.configDir, 'config_test.yaml'))

    app.mainloop()
