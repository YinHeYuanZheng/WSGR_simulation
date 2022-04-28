# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
from multiprocessing import Process,Queue
import time
import os
import sys
import copy
import numpy as np

curDir = os.path.dirname(__file__)
srcDir = os.path.join(curDir, 'src')
sys.path.append(srcDir)

from multiprocessing import Process,Queue
from src.utils.loadConfig import load_config
from src.utils.loadDataset import Dataset
from src.wsgr.wsgrTimer import timer


def run_victory(battle, epoc, q:Queue):
    #result = [0] * 6
    result_flag_list = ['SS', 'S', 'A', 'B', 'C', 'D']
    info_list = []
    for i in range(epoc):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        result_flag_id = result_flag_list.index(log['result'])
        #result[result_flag_id] += 1
        info_list.append(result_flag_id)
        """print(f"第{i + 1}次 - 战果分布: "
              f"SS {result[0] / (i + 1) * 100:.2f}% "
              f"S {result[1] / (i + 1) * 100:.2f}% "
              f"A {result[2] / (i + 1) * 100:.2f}% "
              f"B {result[3] / (i + 1) * 100:.2f}% "
              f"C {result[4] / (i + 1) * 100:.2f}% "
              f"D {result[5] / (i + 1) * 100:.2f}% ")"""
    q.put(info_list)

def run_hit_rate(battle, epoc, q:Queue):
    hit_rate = 0
    info_list = []
    for i in range(epoc):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        #hit_rate += log['hit_rate']
        info_list.append(log["hit_rate"])
        print(f"第{i + 1}次 - 命中率: {hit_rate / (i + 1) * 100: .4f}%")
    q.put(info_list)

def run_avg_damage(battle, epoc, q:Queue):
    avg_damage = 0
    retreat_num = 0
    info_list = []
    for i in range(epoc):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        #avg_damage += np.sum(log['create_damage'][1])
        #retreat_num += log['enemy_retreat_num']
        info_list.append((np.sum(log['create_damage'][1],log['enemy_retreat_num'])))
        #print(f"第{i + 1}次 - 平均伤害: {avg_damage / (i + 1):.3f}; "
        #      f"平均击沉 {retreat_num / (i + 1):.2f}")

    q.put(info_list)
def run_supply_cost(battle, epoc, q:Queue):
    supply = {'oil': 0, 'ammo': 0, 'steel': 0, 'almn': 0}
    info_list = []
    for i in range(epoc):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()
        
        """"supply['oil'] += log['supply']['oil']
        supply['ammo'] += log['supply']['ammo']
        supply['steel'] += log['supply']['steel']
        supply['almn'] += log['supply']['almn']"""
        info_list.append({"oil":log['supply']['oil'],"ammo":log['supply']['ammo'],\
            "steel":log['supply']['steel'],"almn":log['supply']['almn'],})
        """print(f"第{i + 1}次 - 资源消耗: "
            f"油 {supply['oil'] / (i + 1):.1f} "
            f"弹 {supply['ammo'] / (i + 1):.1f} "
            f"钢 {supply['steel'] / (i + 1):.1f} "
            f"铝 {supply['almn'] / (i + 1):.1f}")"""
    q.put(info_list)
def main_function(times,q,type:str):
    #这里写原本的 main 部分
    configDir = os.path.join(os.path.dirname(srcDir), 'config')
    xml_file = os.path.join(configDir, 'config_1.xml')

    dependDir = os.path.join(os.path.dirname(srcDir), 'depend')
    data_file = os.path.join(dependDir, r'ship\database.xlsx')
    ds = Dataset(data_file)
    timer_init = timer()
    battle = load_config(xml_file, ds, timer_init)
    if(type=="supply"):run_supply_cost(battle, times,q)
    if(type=="hit_rate"):run_hit_rate(battle,times,q)
    if(type=="victory"):run_victory(battle,times,q)
    if(type=="damage"):run_avg_damage(battle,times,q)
def output(type,process_list,queue_list):
    print("simulation complted,start counting")
    info = []
    for i in range(len(queue_list)):
        x = queue_list[i].get()
        process_list[i].join()
        for element in x:
            info.append(element)
    if(type == "damage"):
        avg_damage = 0
        retreat_num = 0
        for (i,x) in enumerate(info):
            avg_damage+=info[0]
            retreat_num+=info[1]
            print(f"第{i + 1}次 - 平均伤害: {avg_damage / (i + 1):.3f}; "
                f"平均击沉 {retreat_num / (i + 1):.2f}")
    if(type == "victory"):
        #info 保存的是 resul_flag_id
        result = [0] * 6
        for (i,x) in enumerate(info):
            result[x] += 1
            print(f"第{i + 1}次 - 战果分布: "
              f"SS {result[0] / (i + 1) * 100:.2f}% "
              f"S {result[1] / (i + 1) * 100:.2f}% "
              f"A {result[2] / (i + 1) * 100:.2f}% "
              f"B {result[3] / (i + 1) * 100:.2f}% "
              f"C {result[4] / (i + 1) * 100:.2f}% "
              f"D {result[5] / (i + 1) * 100:.2f}% ")
    if(type == "supply"):
        supply = {'oil': 0, 'ammo': 0, 'steel': 0, 'almn': 0}
        for (i,x) in enumerate(info):
            supply['oil'] += x['oil']
            supply['ammo'] += x['ammo']
            supply['steel'] += x['steel']
            supply['almn'] += x['almn']
            print(f"第{i + 1}次 - 资源消耗: "
            f"油 {supply['oil'] / (i + 1):.1f} "
            f"弹 {supply['ammo'] / (i + 1):.1f} "
            f"钢 {supply['steel'] / (i + 1):.1f} "
            f"铝 {supply['almn'] / (i + 1):.1f}")
    if(type == 'hit_rate'):
        hit_rate=0
        for (i,x) in enumerate(info):
            hit_rate+=x
            print(f"第{i + 1}次 - 命中率: {hit_rate / (i + 1) * 100: .4f}%")
def run_with_multiprocessing(times:int,type:str,process_count = 4):
    """
    times:实际执行次数   
    type:"supply","damage","hit_rate","victory"
    """
    process_list = []
    queue_list = []
    times_list = []

    for i in range(process_count):
        num = int(times/(process_count-i))
        print(num)
        times_list.append(num)
        q = Queue(maxsize=65536)
        queue_list.append(q)
        process_list.append(Process(target=main_function,args=(num,q,type)))
        times -= num
    for x in process_list:
        x.start()
    output(type,process_list,queue_list)
    
if(__name__ == "__main__"):
    starttime = time.time()
    run_with_multiprocessing(4000,"supply",4)
    print(time.time()-starttime)
