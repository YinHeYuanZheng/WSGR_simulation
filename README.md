# WSGR_simulation

## 战舰少女R战斗系统模拟

航空战基础逻辑
技能基础逻辑

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

可以细看一下 `Skill` 的 `activate` 实现，实际上只是往  `Buff` 队列中扔了 `Buff` 实例，并没有放进属性里。

读一下 `Ship` 类的 `add_buff` 实现，它把 `buff` 分为三类塞到了三个不同的对立里，最后要用属性的时候，会调用 `Ship` 类的 `get_final_status`，这个函数会调用 `Ship` 类的 `get_buff` 函数，读取与当前请求的属性有关的 `buff`，并返回总增益值，然后由 `get_final_status` 算出最终属性并返回，避免了反复修改属性值的问题，移除 `buff` 只需要清空相关的 `buff` 队列。

****

现在回到 `BattleUtil.start()`。

`start_phase` 函数处理了各个 `PrepSkill` 技能，结算了航速索敌航向等数据，这些数据保存在 `timer` 类中，这个类有一个战斗开始就创建好的实例，用于保存环境数据，比如航向和索敌情况，战斗点位等，所有其它类的 `timer` 成员共用这一个 `timer` 实例，**而几乎所有的类中都有一个 `timer` 成员，这个成员都是这个 `timer` 实例。**
然后正式进入战斗，战斗过程和实际游戏一模一样，先是 `buff` 阶段，再是航空战...
不用关心具体怎么进入战斗的，实际上只关心了 `BattleUtil` 类中的 `start` 函数，这个函数通过 `run_phase` 调用了各个 `Phase` 子类（比如说 `ShellingPhase`）中的 `start` 成员函数，具体调用的哪个看 `run_phase` 的参数，通过调用每一阶段的 `start` 成员，完成了整个战斗过程。
各个战斗的逻辑情况基本相同，下面以 `buff` 和首轮炮击两个阶段举例。

### BuffPhase

`BuffPhase` 阶段执行了所有游戏中会在 `buff` 阶段执行的增益效果，按照 `Ship.skill` 的描述，给对应的舰船套上了 `buff`。**`skill` 是 `ship` 类的一个成员，储存已经实例化的技能，但是这些技能仅仅被存在了 `skill` 里，除了 `CommonSkill` 外，其它的技能都还没有被放进 `buff` 队列里，这个时候调用 `get_final_status` 时是不会理会除了 `CommonSkill` 描述的 `Buff` 外的所有技能效果的。**但这个时候 `buff` 只是被扔进了一个增益属性队列里，**没有加到属性上**，需要用 `get_final_status` 去查。注意 `CommonSkill` 描述的 `buff` 在这之前的 `battle_init()` 里已经被扔进了 `buff` 队列了。

**一句话总结：`Skill` 类描述了 `Buff` 类，告诉了程序应该在什么时候添加什么 `Buff`**

主动`buff` 以及必中必不中这些需要等到攻击时才会生效的 `buff` 比如说 `CoeffBuff` 及其子类，这里也已经从 `skill` 队列中跑出来了，放入了 `temper_buff` 中，等待着被 `get_buff`,`get_atk_buff` 查询。

### ShellingPhase

这是一个 `Phase` 的子类
炮击战阶段，执行 `ShellingPhase` 的 `start` 成员函数，`for` 循环中那个 `normal_atk` 调用了 `Ship` 类的 `raise_atk` 函数，在 `raise_atk` 函数中生成了攻击。
接着拿到了 `raise_atk` 的一个 `ATK` 类的返回列表，调用了 `ATK` 类的 `start` 成员。

### raise_atk
这是 `Ship` 类的一个成员函数。
`raise_atk` 中先处理了特殊攻击，具体方式看 `SpecailAtkBuff` 类的 `activate` 实现。
第二步处理了优先攻击技能，具体不赘述。
主要看最后面那个 `normal_atk` 的类的实例化，这玩意实例化了一个 `ATK` 类，并返回了这个实例。

### ATK

这玩意的实现在 `formular.py` 里。
`ATK` 类保存了所有涉及攻击的实例，当然包括攻击者和被攻击者，一些攻击时加成的 `buff`，比如 `AtkBuff` ，会在这里体现。
`start` 成员函数里那几个 `hit_verify`，`crit_verify`,`final_damage` 的实现中，基本都有对 `Ship` 类中 `get_buff` ，`get_atk_buff`相关函数的调用，完成了形如 "攻击xxx时xxx提升xxx" 的效果，而攻击时 `Buff` 的实现会在这些调用中体现，阅读相关内容即可。

### Ship

关注 `add_buff` 函数，这里把所有的 `buff` 都扔了上去，扔到一个待激活队列里（`common_buff`,`temper_buff` 等）。
`get_buff` 一系列函数就从这个待激活队列找需要的 `buff` 并返回到 `ATK` 那里去，然后 `ATK` 得到参数并计算伤害。 

如果谬误，请联系 `huan-yp` 更正。

### 碎碎念
- 一些激活条件随战斗变化的 BUFF,除非是 `ATK_buff`,条件一定要写在 `is_activate` 里面, **不要写在 activate 里**,除了 `ATK_buff` 会在攻击时根据 `activate` 的描述进行操作外,其它 BUFF 的 `activate` 都只会在最开始执行一次,而是否激活由 `is_activate` 在战斗时判断。如果有技能的效果随战斗改变的情况,只能写 `ATKBuff`。

