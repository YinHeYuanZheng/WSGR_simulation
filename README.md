# 战舰少女R 战斗模拟器

战舰少女R（Warship Girls R）战斗系统模拟器，完整还原游戏内全部战斗流程、技能逻辑与伤害公式，支持胜率分析、命中率分析、平均伤害统计等多种模拟功能。

## 环境依赖

- Python 3.11+
- numpy、pandas、openpyxl、pyyaml

```bash
pip install -r requirements.txt
```

## 快速上手

编辑 `main.py` 底部的参数，然后运行：

```bash
python main.py
```

| 参数 | 说明 |
|------|------|
| `configFile` | 战斗配置文件路径（XML 或 YAML），位于 `config/` 目录 |
| `epoch` | 模拟次数，默认 10000 |
| `battle_num` | 每次模拟的战斗轮次，默认 1 |
| `fun` | 分析函数，见下表 |

**可用分析函数：**

| 函数名 | 功能 |
|--------|------|
| `run_victory` | 胜利等级概率分布（SS/S/A/B/C/D） |
| `run_hit_rate` | 各舰命中率统计 |
| `run_avg_damage` | 各阶段平均伤害 |
| `run_supply_cost` | 补给消耗计算 |
| `run_map_victory` | 关卡通关成功率 |

## 战斗配置

支持 XML 和 YAML 两种格式，模板分别见 `config/config.xml` 和 `config/save/config_sample.yaml`。

**XML 示例：**
```xml
<Battle type="DaytimeBattle">
  <Fleet side="1" form="2">
    <!-- side: 1=我方, 0=敌方 | form: 队形(1-4) -->
    <Ship loc="1" cid="10513" level="110" affection="200" skill="1">
      <Equipment loc="1" eid="10653"/>
      <Strategy stid="233" level="3"/>
    </Ship>
  </Fleet>
  <Fleet side="0" form="1">
    <Ship loc="1" cid="20101" level="1"/>
  </Fleet>
</Battle>
```

**YAML 示例：**
```yaml
battle_type: DaytimeBattle
friend_fleet:
  form: 2
  side: 1
  ships:
    - loc: 1
      cid: '10513'
      level: 110
      affection: 200
      skill: 1
      equipment:
        - loc: 1
          eid: '10653'
      strategy:
        - stid: '233'
          level: 3
enemy_fleet:
  form: 1
  side: 0
  ships:
    - loc: 1
      cid: '20101'
      level: 1
```

舰船 ID（`cid`）、装备 ID（`eid`）、战术 ID（`stid`）均来自 `depend/ship/database.xlsx`。

**队形对照：**

| form | 队形  |
|------|-----|
| 1    | 单纵阵 |
| 2    | 复纵阵 |
| 3    | 轮形阵 |
| 4    | 梯形阵 |
| 5    | 单横阵 |

**Ship 属性说明：**

| 属性 | 说明 |
|------|------|
| `loc` | 队列位置，1 为旗舰，依次往后 |
| `cid` | 舰船 ID，对应数据库中的编号 |
| `level` | 等级 |
| `affection` | 好感度（影响部分技能触发） |
| `skill` | 是否开启技能，1 为开启，0 为关闭 |

**战斗类型（BattleType）：**

| 值 | 说明          |
|----|-------------|
| `DaytimeBattle` | 标准昼战        |
| `NightBattle` | 夜战          |
| `AirBattle` | 航空战（含炮击、夜战） |
| `OnlyAirBattle` | 纯航空战        |
| `SpecialBattle` | 特殊战斗        |

## 装备特效配置

装备技能通过 `depend/ship/database.xlsx` 装备表中的 `特效配置` 列读取。旧的
`特效` 和 `特效数值` 列仅作为历史数据保留，运行时不再使用。

### 普通词条

普通词条的完整格式为：

```text
词条名:数值[,stack][,阶段]
```

| 写法 | 说明 |
|------|------|
| `hit_rate:0.05` | 使用词条默认阶段 |
| `hit_rate:0.05,ShellingPhase` | 覆盖默认阶段 |
| `pierce_coef:0.05,stack` | 允许原本不可叠加的词条正常叠加 |
| `pierce_coef:0.05,stack,ShellingPhase` | 同时指定 `stack` 和阶段 |

`stack` 必须写在阶段之前。它对普通可叠加词条没有额外作用，
目前主要用于使`pierce_coef`(穿甲) 和 `uplimit_buff`(超重弹) 正常叠加。
不填写 `stack` 时，这两类词条只保留最高值。

当前支持的普通词条：

| 词条名 | 默认阶段 | 说明 |
|--------|----------|------|
| `pierce_coef` | `AllPhase` | 穿甲系数，默认不可叠加 |
| `uplimit_buff` | `ShellingPhase` | 攻击上限加成，默认不可叠加 |
| `hit_rate` | `AllPhase` | 命中率 |
| `miss_rate` | `AllPhase` | 回避率 |
| `crit` | `AllPhase` | 暴击率 |
| `power_buff` | `AllPhase` | 攻击威力倍率 |
| `final_damage_buff` | `AllPhase` | 最终伤害倍率 |
| `air_ctrl_buff` | `AirPhase` | 制空值加成 |
| `air_atk_buff` | `AirPhase` | 舰载机威力倍率 |
| `air_bomb_atk_buff` | `AirPhase` | 轰炸机威力倍率 |
| `air_dive_atk_buff` | `AirPhase` | 鱼雷机威力倍率 |

阶段参数直接使用 `src/wsgr/phase.py` 中已有的阶段类名，例如
`AirPhase`、`ShellingPhase` 和 `AllPhase`。

### 并列与合并

使用分号并列多个配置项：

```text
air_atk_buff:0.05;hit_rate:0.05,ShellingPhase
```

上述配置生成两个独立的 `EquipSkill`，每个技能包含一个 `EquipEffect`。

主动使用大括号包裹两个或更多最终普通词条时，它们会合并为一个
`EquipSkill`，内部包含多个 `EquipEffect`(推荐这样写)：

```text
{air_atk_buff:0.05;hit_rate:0.05,ShellingPhase}
```

每个 `EquipEffect` 仍拥有独立的可读特效编号，例如 `10619.001` 和
`10619.002`。顶层大括号不能只包裹一个普通词条，也不能在同一组内混合普通
词条与包装器。

### 包装器

包装器用于限制装备技能的生效条件或目标。包装普通词条时必须使用大括号；
包装另一个包装器时直接嵌套，不额外添加大括号。

| 包装器 | 参数 | 说明           |
|--------|------|--------------|
| `Cid` | 舰船编号或编号数组 | 仅指定舰船装备时生效   |
| `Country` | 国籍或国籍数组 | 仅指定国籍装备时生效      |
| `Tag` | 标签或标签数组 | 仅指定标签装备时生效      |
| `ShipType` | 舰种或舰种数组 | 仅指定舰种装备时生效      |
| `Side` | `0` 或 `1` | 将目标改为敌方或我方全队 |

示例：

```text
Cid(533,{crit:0.1})
Country(C,{crit:0.1;miss_rate:0.05})
Country(C,ShipType(CLT,{crit:0.1;miss_rate:0.05}))
Side(0,{hit_rate:-0.1,AirPhase})
ShipType(BM,{pierce_coef:0.1,stack;miss_rate:0.1})
```

包装器内的大括号同样具有合并语义，因此
`Country(C,{crit:0.1;miss_rate:0.05})` 会生成一个包含两个效果的技能。

`Cid` 支持以下编号规则：

- 三位编号表示友方舰船，并自动展开为未改造 `10xxx` 和改造 `11xxx`。
- 五位且以 `0` 开头的编号表示敌方舰船，直接使用。
- 五位且以 `1` 开头的编号表示友方舰船，直接使用。
- 同一个 `Cid` 参数中不能混用三位和五位编号。

```text
Cid(533,{crit:0.1})
Cid(["030","552"],{crit:0.1})
Cid("00048",{crit:0.1})
```

### Python 定向

无法用普通词条和包装器表达的复杂效果，可以通过 `@特效编号` 定向调用
`src/skillCode/Equipment/esid{编号}.py`：

```text
@013:0.1
@013:0.1;hit_rate:0.05,ShellingPhase
Cid(552,{@013:0.1})
```

冒号后的值会作为参数传给原 Python 装备技能。Python 定向可以与其他配置项
并列，也可以被包装器限制，但不能参与普通词条的大括号合并组。

配置通过数据库加载时，语法错误会同时显示装备 ID 和原始配置内容，例如：

```text
装备 10999 的特效配置错误: 未知装备特效词条: unknown_effect
配置内容: unknown_effect:0.1
```

### 完整语法示例

以下 `#` 行仅为 README 注释，填写 Excel 单元格时只填写对应配置文本。

```text
# 两个独立技能
air_atk_buff:0.05;hit_rate:0.05,ShellingPhase

# 一个包含两个效果的技能
{air_atk_buff:0.05;hit_rate:0.05,ShellingPhase}

# 指定舰种生效，并将两个效果合并为一个技能
ShipType(BM,{pierce_coef:0.1,stack;miss_rate:0.1})

# 普通穿甲不可叠加，指定舰船获得的额外穿甲可以叠加
pierce_coef:0.1;Cid(533,{pierce_coef:0.05,stack})

# 复用现有 Python 技能并追加普通词条
@013:0.1;hit_rate:0.05,ShellingPhase
```

## 项目结构

```
WSGR/
├── main.py                  # 入口：参数配置与运行
├── config/                  # 战斗配置文件（XML/YAML）
├── depend/
│   ├── ship/database.xlsx   # 舰船、装备数据库
│   └── map/                 # 海图数据
└── src/
    ├── wsgr/                # 核心模型
    │   ├── ship.py          # Ship / Fleet 类
    │   ├── equipment.py     # 装备类层级
    │   ├── formulas.py      # 攻击与伤害公式
    │   ├── skill.py         # 技能/Buff 引擎
    │   └── wsgrTimer.py     # 战斗状态单例
    ├── utils/
    │   ├── battleUtil.py    # 战斗流程编排
    │   ├── phase.py         # 战斗阶段（侦察→航空→雷击→炮击→夜战）
    │   ├── loadConfig.py    # 配置文件解析
    │   ├── loadDataset.py   # 数据库读取
    │   ├── parseEquipSkill.py # 装备特效配置语法解析
    │   ├── runUtil.py       # 统计分析函数
    │   ├── mapUtil.py       # 关卡地图逻辑
    │   ├── envBuffUtil.py   # 环境Buff定义
    │   └── gui.py           # 图形界面
    └── skillCode/           # 技能实现
        ├── BB/ BC/ CV/ CVL/ CA/ CL/ DD/ SS/ ASDG/
        ├── Other/ Enemy/
        ├── Equipment/       # 装备特效 (esid*.py)
        └── Strategy/        # 战术效果 (stid*.py)
```

### Skill 与 Buff：核心设计

**Skill 描述"何时给谁加什么 Buff"，Buff 是实际存放在舰船队列中的效果实例。**

- `battle_init()` 阶段：结算 `CommonSkill`（面板技能），其 Buff 进入 `common_buff` 队列
- `BuffPhase` 阶段：激活其余技能，Buff 进入 `temper_buff`（临时）或 `active_buff`（主动）队列
- Buff **从不直接修改属性值**。需要查询属性时，调用 `Ship.get_final_status()`，它内部通过 `get_buff()` 动态聚合相关队列中的所有 Buff，计算最终值后返回
- 移除 Buff 只需清空对应队列，无需回滚属性

**Buff 类型（仅举例部分）：**

| 类型 | 说明 |
|------|------|
| `StatusBuff` | 属性值增减（火力、装甲等面板数值） |
| `CommonBuff` | 常驻属性加成，存入 `common_buff`，配合 `CommonSkill` 使用 |
| `CoeffBuff` | 无条件百分比修正（暴击率、命中率、回避率等） |
| `AtkBuff` | 有攻击条件（`atk_request`）的百分比修正 |
| `FinalDamageBuff` | 最终伤害倍率修正（继承自 `AtkBuff`，支持 `rate` 触发概率） |
| `AtkHitBuff` | 攻击/被攻击事件触发，将内层 buff 施加给指定目标（支持叠加） |
| `RoundaboutBuff` | 迂回成功率直接加成，继承自 `CommonBuff`，配合 `CommonSkill + SelfTarget` 防止重复计算 |

### ATK：攻击执行流程

`formulas.py` 中定义了 20+ 种 ATK 子类（炮击、雷击、航空、导弹、夜战等），每次攻击的执行步骤：

1. `target_init()` — 选择目标（随机 / 优先 / 嘲讽）
2. `start_atk()` — 检查格挡效果，触发攻击时 Buff
3. `hit_verify()` — 命中判定（受阵型、航向系数影响）
4. `crit_verify()` — 暴击判定
5. `formula()` — 基础伤害
6. `real_damage()` — 应用所有系数与 Buff'
7. `final_damage()` — 应用所有倍率与 FinalDamageBuff

---

## 扩展开发

- **新增舰船技能：** 在 `src/skillCode/{舰种}/sid{N}.py` 中按现有格式添加
- **新增装备特效：** 优先在数据库 `特效配置` 列组合已有词条；无法声明式表达时，在 `src/skillCode/Equipment/esid{N}.py` 中添加并使用 `@N` 定向
- **新增战术效果：** 在 `src/skillCode/Strategy/stid{N}.py` 中添加
- **新增分析函数：** 在 `src/utils/runUtil.py` 中按 `run_*` 命名规范添加
- **新增战斗类型：** 继承 `BattleUtil` 并在 `src/utils/battleUtil.py` 中组合所需阶段

技能文件结构：
```python
# -*- coding:utf-8 -*-
# Author:作者署名
# env:py38
# 船名-技能序号

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""技能描述"""

class SkillClass_section1(CommonSkill):
    """技能语段1(根据实际目标、效果、条件等进行拆分)
    CommonSkill仅包含战斗外面板加成
    PrepSkill仅包含影响迂回、索敌的战斗内加成"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target
        self.buff = []
        self.request = None

class SkillClass_section2(Skill):
    """技能语段2(根据实际目标、效果、条件等进行拆分)
    CommonSkill、PrepSkill外的所有加成都需要通过Skill实现"""
    pass

name = "技能名称"
skill = [SkillClass_section1, SkillClass_section2]  # 列表索引对应技能拆分语段
```

## 联系

如有错误或问题，请联系 `银河远征`。
