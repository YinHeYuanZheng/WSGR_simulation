# WSGR_simulation

## 战舰少女R战斗系统模拟
包含全部战斗流程
以及技能基础逻辑

## 配置步骤



## 代码执行步骤简介:

高度建议打开你的 `IDE` 对着代码看这个简介。

先看 `main.py`，其它函数的不用管，看 `load_config`。

### load_config:

主函数入口调用 `load_config` 加载战斗模块，这个函数里主要是一些配置上的东西，其它不用管，**真正要运行的模块在 `load_cofig` 的实现里**，叫 `BattleUtil`。

`load_config` 最后把一个 `battle` 返回了，然后在 `main.py` 的 `run_supply_cost` 这些函数中调用了这个 `battle`，**本质上调用的是 `BattleUtil` 的 `start` 成员函数**

### BattleUtil

在 `main` 函数中调用了 `Battleutil` 的 `start` 成员函数，正式进行战斗。 
然后它执行了一堆东西：
`battle_init` 函数初始化了各个舰船的血量，处理了环境增益（战况，猪飞这些），结算了面板技能，并将其它技能从技能代码库中导了进来，塞进了待激活技能队列 `self.skill` 里。

**下面注意区分好 `Skill` 和 `Buff`，这是两个东西**

可以细看一下 `Skill` 的 `activate` 实现，实际上只是往舰船的  `Buff` 队列中添加了 `Buff` 实例，并没有放进属性里。

`Ship` 类的 `add_buff` 方法中，将 `buff` 分为三类不同的队列里。调用属性值时，会调用`get_final_status`方法，这个函数会继续调用 `Ship` 类的 `get_buff` 函数，读取与当前请求的属性有关的 `buff`，并返回总增益值，然后由 `get_final_status` 算出最终属性并返回，避免了反复修改属性值的问题，移除 `buff` 只需要清空相关的 `buff` 队列。

****

现在回到 `BattleUtil.start()`。

`start_phase` 函数处理了各个 `PrepSkill` 技能，结算了航速索敌航向等数据，这些数据保存在 `timer` 类中，这个类有一个战斗开始就创建好的实例，用于保存环境数据，比如航向和索敌情况，战斗点位等，所有其它类的 `timer` 成员共用这一个 `timer` 实例，**而几乎所有的类中都有一个 `timer` 成员，这个成员都是这个 `timer` 实例。**
然后正式进入战斗，战斗过程和实际游戏一模一样，先是 `buff` 阶段，再是航空战...
不用关心具体怎么进入战斗的，实际上只关心了 `BattleUtil` 类中的 `start` 函数，这个函数通过 `run_phase` 调用了各个 `Phase` 子类（比如说 `ShellingPhase`）中的 `start` 成员函数，具体调用的哪个看 `run_phase` 的参数，通过调用每一阶段的 `start` 成员，完成了整个战斗过程。
各个战斗的逻辑情况基本相同，下面以 `buff` 和首轮炮击两个阶段举例。

### BuffPhase

`BuffPhase` 阶段执行了所有游戏中会在 `buff` 阶段执行的增益效果，按照 `Ship.skill` 的描述，给满足条件的舰船添加 `buff`。**`skill` 是 `ship` 类的一个成员，储存已经实例化的技能，但是这些技能仅仅被存在了 `skill` 里，除了 `CommonSkill` 外，其它的技能都还没有结算，这个时候调用 `get_final_status` 时只会受到 `CommonSkill` 的影响。**但这个时候 `buff` 只是被扔进了一个增益属性队列里，**没有加到属性上**，需要用 `get_final_status` 去查。注意 `CommonSkill` 描述的 `buff` 在这之前的 `battle_init()` 里已经被扔进了 `buff` 队列了。

**一句话总结：`Skill` 类描述了 `Buff` 类，告诉了程序应该在什么时候添加什么 `Buff`**

主动`buff` 以及必中必不中这些需要等到攻击时才会生效的 `buff` 比如说 `CoeffBuff` 及其子类，这里也已经被 `skill` 施加给对应舰船，放入了 `temper_buff` 中，等待着被 `get_buff`,`get_atk_buff` 查询。

### ShellingPhase

这是一个 `Phase` 的子类
炮击战阶段，执行 `ShellingPhase` 的 `start` 成员函数，`for` 循环中那个 `normal_atk` 调用了 `Ship` 类的 `raise_atk` 函数，在 `raise_atk` 函数中生成了攻击。
接着拿到了 `raise_atk` 的一个 `ATK` 类的返回列表，调用了 `ATK` 类的 `start` 成员。

### raise_atk
这是 `Ship` 类的一个成员函数。
`raise_atk` 中先处理了特殊攻击，具体方式看 `SpecailAtkBuff` 类的 `activate` 实现。
第二步处理了优先攻击技能，具体不赘述。
如果没有特殊攻击技能，则会根据船型设定，创建一个 `ATK` 类的实例并返回。

### ATK

这玩意的实现在 `formulas.py` 里。
`ATK` 类保存了所有涉及攻击的实例，当然包括攻击者和被攻击者，一些攻击时加成的 `buff`，比如 `AtkBuff` ，会在这里体现。
`start` 成员函数里那几个 `hit_verify`，`crit_verify`,`final_damage` 的实现中，基本都有对 `Ship` 类中 `get_buff` ，`get_atk_buff`相关函数的调用，完成了形如 "攻击xxx时xxx提升xxx" 的效果，而攻击时 `Buff` 的实现会在这些调用中体现，阅读相关内容即可。

### Ship

关注 `add_buff` 函数，这里把所有的 `buff` 都保存到一个待激活队列里（`common_buff`,`temper_buff` 等）。
`get_buff` 一系列函数就从这个待激活队列找需要的 `buff` 并返回到 `ATK` 那里去，然后 `ATK` 得到参数并计算伤害。 

## config.xml文件结构:
括号内为当前节点所有属性
```
Battle -+- (type) 战斗类型(可以填战斗点属性或 Map)
        |
        | type 填写战斗点属性时，需要同时填写两个 Fleet 节点，Map 时只有一个 Fleet 节点
        | 一个是友方舰队，一个是深海舰队，深海舰队不需要写装备
        +- Fleet -+- (side)
        |         +- (form)
        |         +- Ship -+- (loc)
        |                  +- (cid)
        |                  +- (level)
        |                  +- (affection)
        |                  +- (skill)
        |                  +- Equipment -+- (loc)
        |                                +- (eid)
        |
        | 只有当 type 填入 Map 时才会写 Map 节点，否则只有两个 Fleet 节点
        +- Map -+- (mapid) 与对应的 mapid.xml 中的数字相同
                +- (entrance) 入口编号，与 mapid.xml 中 entrance 节点的属性 num 对应
```

## mapidxxxxx.xml文件结构:
括号内为当前节点所有属性
```
Map -+- (id)
     +- entrance -+- (num) 有几个入口就写几个 entrance 节点，分别有不用的地图带路条件
                  +- point -+- (pid) pid对应数据保存在 ./ship/database.xlsx/海图 中
                            +- (name) entrance 节点下第一个 point 节点的名称必须为 entrance
                            +- (level) 0-5分别代表入口、出门、道中、门神、非boss终点、boss
                            |
                            | 带路点，当 point 的 level 不是4或5时必须填写至少一个
                            +- suc -+- (name) 带路点名称
                                    +- (weight) 随机沟权重，用星级表示
                                    +- (relation) 如果有带路条件且超过一个，在这里填写各条件关系，同时满足填写'and'，只要一个满足填写'or'
                                    +- request -+- (type) 带路条件种类 -+- 'num': 舰队内指定舰种的个数(如 CV>=2)
                                                |                     +- 'leader': 旗舰是或不是指定舰种(如 旗舰为BB)
                                                |                     +- 'status': 舰队某一属性满足要求，注意旗舰属性也在这里
                                                +- (name) 带路条件具体要求 -+- 指定舰种时用大写字母填写，中间用英文逗号隔开(如 'BB,BC' 或 'DD')
                                                |                        | 指定属性包括以下几类，没有多余种类，有需求联系我
                                                |                        +- 'level''avg_speed''leader_speed''low_speed''high_speed''recon''luck'
                                                +- (fun) 判断式符号 -+- 'lt': <
                                                |                  +- 'le': <=
                                                |                  +- 'eq': ==
                                                |                  +- 'ge': >=
                                                |                  +- 'gt': >
                                                |                  +- 'is': 仅限旗舰种类(如 旗舰为BB)
                                                |                  +- 'not': 仅限旗舰种类(如 旗舰不为BB)
                                                +- (value) 判断式数值，如果type填写'leader'，没有value属性
```
如果谬误，请联系 `huan-yp` 更正。

### 碎碎念
- 一些激活条件随战斗变化的 BUFF,除非是 `ATK_buff`,条件一定要写在 `is_activate` 里面, **不要写在 activate 里**,除了 `ATK_buff` 会在攻击时根据 `activate` 的描述进行操作外,其它 BUFF 的 `activate` 都只会在最开始执行一次,而是否激活由 `is_activate` 在战斗时判断。如果有技能的效果随战斗改变的情况,只能写 `ATKBuff`。

