# Chapter 8: Planning & Reasoning 规划与推理

## 8.1 什么是规划（Planning）？

**规划** 是 Agent 将复杂目标分解为可执行步骤序列的过程。

```
目标：组织一次技术分享会

规划：
1. 确定主题和受众
2. 搜集资料（2小时）
3. 制定大纲（30分钟）
4. 制作幻灯片（3小时）
5. 准备示例代码（1小时）
6. 演练（1小时）
7. 正式分享
```

---

## 8.2 规划的类型

### 1. 任务分解（Task Decomposition）

```
复杂任务 → 分解为子任务 → 分解为更小的子任务

示例：写一篇技术博客
├── 确定主题
├── 搜集资料
├── 制定大纲
│   ├── 引言
│   ├── 主体
│   │   ├── 第一部分
│   │   ├── 第二部分
│   │   └── 第三部分
│   └── 结论
├── 撰写初稿
├── 添加代码示例
├── 校对优化
└── 发布
```

### 2. 顺序规划（Sequential Planning）

```
步骤1 → 步骤2 → 步骤3 → ... → 完成

示例：
1. 打开冰箱
2. 取出食材
3. 清洗食材
4. 切菜
5. 开火
6. 炒菜
7. 装盘
8. 上菜
```

### 3. 分支规划（Branching Planning）

```
          开始
            ↓
        ┌───┴───┐
        ↓       ↓
     条件A   条件B
        ↓       ↓
     行动1   行动2
        ↓       ↓
        └───┬───┘
            ↓
          完成
```

---

## 8.3 规划算法

### 1. 层次任务网络（HTN）

```
目标：准备晚餐

HTN 分解：
准备晚餐
├── 准备食材
│   ├── 买菜
│   └── 洗菜
├── 烹饪
│   ├── 切菜
│   ├── 炒菜
│   └── 煮汤
└── 摆盘
    ├── 装盘
    └── 上菜
```

### 2. 图规划（Graphplan）

```
构建规划图：
- 状态层（State Layers）
- 行动层（Action Layers）

S0 → A1 → S1 → A2 → S2 → ... → 目标状态
```

### 3. 前向搜索（Forward Search）

```
从初始状态开始，搜索可达目标状态的路径

初始状态 → 可能的行动 → 新状态 → ...
```

### 4. 后向搜索（Backward Search）

```
从目标状态开始，反向搜索需要的行动

目标状态 → 需要什么前提 → 前提条件如何满足 → ...
```

---

## 8.4 Agent 规划的实现

### LLM 作为规划器

```python
class LLMAgentPlanner:
    def __init__(self, llm):
        self.llm = llm
    
    def plan(self, goal: str, context: str = "") -> List[str]:
        """为给定目标制定计划"""
        prompt = f"""
目标：{goal}
上下文：{context}

请将目标分解为具体的执行步骤，每一步都是可执行的行动。
输出格式：
Step 1: [具体行动]
Step 2: [具体行动]
...
"""
        response = self.llm.generate(prompt)
        return self._parse_plan(response)
    
    def _parse_plan(self, response: str) -> List[str]:
        lines = response.strip().split('\n')
        steps = []
        for line in lines:
            if line.startswith('Step'):
                steps.append(line.split(':', 1)[1].strip())
        return steps
```

### Replan（重新规划）

```python
class AdaptiveAgent:
    def run(self, goal: str):
        # 初始规划
        plan = self.planner.plan(goal)
        
        while not self.is_goal_reached():
            # 执行当前步骤
            result = self.execute_current_step()
            
            # 检查是否需要重新规划
            if self.needs_replan(result):
                new_plan = self.planner.replan(
                    goal, 
                    current_state=result
                )
                plan = new_plan
        
        return self.get_result()
```

---

## 8.5 推理类型

### 1. 演绎推理（Deductive Reasoning）

```
从一般到特殊

前提1：所有人都会死
前提2：苏格拉底是人
结论：苏格拉底会死
```

### 2. 归纳推理（Inductive Reasoning）

```
从特殊到一般

观察1：天鹅1是白色的
观察2：天鹅2是白色的
观察3：天鹅3是白色的
结论：所有天鹅都是白色的（可能）
```

### 3. 类比推理（Analogical Reasoning）

```
基于相似性推理

A 和 B 有相似特征 X、Y、Z
A 有特征 W
结论：B 可能也有特征 W
```

### 4. 因果推理（Causal Reasoning）

```
分析原因和结果

事件 A 发生后，事件 B 发生
多次观察到 A → B 的模式
结论：A 可能导致 B
```

---

## 8.6 Agent 推理的挑战

### 1. 知识不完备

```
问题：Agent 可能缺少必要的背景知识
解决方案：
- 检索外部知识
- 调用搜索工具
- 询问用户
```

### 2. 推理偏差

```
问题：LLM 可能有训练数据偏差
解决方案：
- 多角度思考
- 自我验证
- 交叉检查
```

### 3. 计算限制

```
问题：复杂问题需要大量计算
解决方案：
- 简化问题
- 分步解决
- 使用外部工具
```

---

## 8.7 实战案例：任务规划 Agent

```python
class TaskPlanningAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
        self.memory = []
    
    def execute_task(self, goal: str) -> str:
        # Step 1: 规划
        plan = self.create_plan(goal)
        
        # Step 2: 执行
        for step in plan:
            result = self.execute_step(step)
            self.memory.append({
                "step": step,
                "result": result
            })
            
            # Step 3: 检查是否需要重新规划
            if self.should_replan(result):
                plan = self.replan(goal)
        
        return self.summarize_results()
    
    def create_plan(self, goal: str) -> List[str]:
        """创建计划"""
        prompt = f"""
目标：{goal}

请制定一个详细的执行计划，包含：
1. 每个步骤的具体行动
2. 所需的工具或资源
3. 预期的输出

格式：Step N: [行动] [工具] [输入] → [预期输出]
"""
        response = self.llm.generate(prompt)
        return self.parse_plan(response)
    
    def execute_step(self, step: str) -> Any:
        """执行单个步骤"""
        # 解析步骤，调用相应工具
        pass
    
    def should_replan(self, result: Any) -> bool:
        """判断是否需要重新规划"""
        # 如果结果不符合预期，重新规划
        pass
    
    def replan(self, goal: str) -> List[str]:
        """基于当前状态重新规划"""
        context = self.get_current_context()
        return self.create_plan(f"{goal}\n当前状态：{context}")
```

---

## 8.8 小结

规划与推理是 Agent 智能的核心：

| 能力 | 说明 | 关键技术 |
|------|------|----------|
| **任务分解** | 将复杂目标分解 | HTN、分层规划 |
| **顺序规划** | 确定执行顺序 | 搜索算法 |
| **动态调整** | 根据反馈调整计划 | Replan |
| **推理能力** | 分析和判断 | CoT、逻辑推理 |

**关键点：**
- 好的规划 = 更高的成功率
- 规划需要与执行相结合
- 动态调整是必要的

---

**下一章：** [Chapter 9: Multi-Agent 系统](../03-advanced/chapter09-multi-agent.md)

---

*最后更新：2026-03-11*
