# Chapter 2: Agent 的基本组成

## 2.1 Agent 的核心组件

一个完整的 AI Agent 通常由以下核心组件构成：

```
┌─────────────────────────────────────────────────────────┐
│                      Agent 架构                          │
├─────────────────────────────────────────────────────────┤
│  ┌─────────┐    ┌─────────┐    ┌─────────────────────┐  │
│  │ 感知层  │ ─→ │ 决策层  │ ─→ │     行动层          │  │
│  │Perceive│    │ Decide  │    │     Act             │  │
│  └─────────┘    └─────────┘    └─────────────────────┘  │
│       ↑              ↑                    ↓             │
│       │              │                    │             │
│       └──────────────┴────────────────────┘             │
│                      记忆层 (Memory)                    │
└─────────────────────────────────────────────────────────┘
```

---

## 2.2 感知层（Perception）

### 功能
理解输入信息，包括用户请求、环境状态、工具返回结果等。

### 主要能力

| 能力 | 说明 |
|------|------|
| **意图理解** | 理解用户真正想要什么 |
| **上下文理解** | 理解对话历史和背景 |
| **多模态理解** | 处理文本、图像、音频等 |
| **信息提取** | 从复杂信息中提取关键点 |

### 实现方式

```python
# 感知层示例
class PerceptionLayer:
    def __init__(self, llm):
        self.llm = llm
    
    def understand_intent(self, user_input):
        """理解用户意图"""
        prompt = f"""
        分析以下用户输入的意图：
        用户：{user_input}
        
        请输出：
        1. 核心意图
        2. 所需工具
        3. 优先级
        """
        return self.llm.generate(prompt)
    
    def extract_context(self, conversation_history):
        """提取对话上下文"""
        # 实现上下文提取逻辑
        pass
```

---

## 2.3 决策层（Decision）

### 功能
基于感知结果，决定下一步应该执行什么动作。

### 核心能力

| 能力 | 说明 |
|------|------|
| **推理** | 基于已有信息进行逻辑推理 |
| **规划** | 制定多步骤行动计划 |
| **选择** | 在多个选项中选择最佳方案 |
| **评估** | 评估行动的风险和收益 |

### 决策流程

```
输入 → 分析 → 规划 → 选择 → 输出行动
         ↓
      评估反馈
         ↓
      调整策略
```

### 实现方式

```python
# 决策层示例
class DecisionLayer:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
    
    def plan(self, goal, context):
        """制定计划"""
        prompt = f"""
        目标：{goal}
        上下文：{context}
        
        请制定一个分步计划：
        1. 第一步做什么
        2. 第二步做什么
        3. 如何验证结果
        """
        return self.llm.generate(prompt)
    
    def select_tool(self, task):
        """选择合适的工具"""
        # 评估可用工具，选择最佳方案
        pass
```

---

## 2.4 行动层（Action）

### 功能
执行决策层制定的计划，调用工具，产生实际输出。

### 行动类型

| 类型 | 说明 | 示例 |
|------|------|------|
| **工具调用** | 调用外部工具/函数 | 搜索、计算、API调用 |
| **代码执行** | 运行代码 | Python脚本、Shell命令 |
| **内容生成** | 生成文本/图像 | 回复、文档、图片 |
| **环境交互** | 修改环境状态 | 文件操作、数据库更新 |

### 实现方式

```python
# 行动层示例
class ActionLayer:
    def __init__(self, tools):
        self.tools = tools
    
    def execute_tool(self, tool_name, params):
        """执行工具调用"""
        if tool_name in self.tools:
            tool = self.tools[tool_name]
            return tool.run(params)
        raise ValueError(f"工具 {tool_name} 不存在")
    
    def generate_response(self, content):
        """生成响应"""
        return content
```

---

## 2.5 记忆层（Memory）

### 功能
存储和检索信息，帮助 Agent 保持状态和积累知识。

### 记忆类型

| 类型 | 说明 | 持久性 | 示例 |
|------|------|--------|------|
| **短期记忆** | 当前会话信息 | 会话级 | 对话历史 |
| **长期记忆** | 持久化知识 | 永久 | 用户偏好、历史记录 |
| **工作记忆** | 临时计算结果 | 任务级 | 中间推理结果 |
| **语义记忆** | 概念和事实 | 永久 | 世界知识 |

### 实现方式

```python
# 记忆层示例
class MemoryLayer:
    def __init__(self):
        self.short_term = []      # 短期记忆
        self.long_term = {}       # 长期记忆
        self.working_memory = {}  # 工作记忆
    
    def add_short_term(self, item):
        """添加短期记忆"""
        self.short_term.append(item)
    
    def add_long_term(self, key, value):
        """添加长期记忆"""
        self.long_term[key] = value
    
    def retrieve(self, query):
        """检索记忆"""
        # 从所有记忆层检索相关信息
        results = []
        # 检索逻辑...
        return results
```

---

## 2.6 组件协作流程

### 完整的 Agent 工作流程

```
1. 感知层：接收用户输入
   ↓
2. 记忆层：检索相关历史信息
   ↓
3. 决策层：分析 + 规划
   ↓
4. 行动层：执行计划（工具调用/生成回复）
   ↓
5. 记忆层：存储新的信息
   ↓
6. 返回结果给用户
```

### 代码示例

```python
class Agent:
    def __init__(self):
        self.perception = PerceptionLayer(llm)
        self.decision = DecisionLayer(llm, tools)
        self.action = ActionLayer(tools)
        self.memory = MemoryLayer()
    
    def run(self, user_input):
        # 1. 感知
        intent = self.perception.understand_intent(user_input)
        
        # 2. 检索记忆
        context = self.memory.retrieve(intent)
        
        # 3. 决策
        plan = self.decision.plan(intent, context)
        
        # 4. 行动
        result = self.action.execute(plan)
        
        # 5. 存储记忆
        self.memory.add_short_term({
            'input': user_input,
            'output': result
        })
        
        return result
```

---

## 2.7 小结

Agent 的核心组件包括：

| 组件 | 核心功能 | 关键技术 |
|------|----------|----------|
| 感知层 | 理解输入 | NLP、意图识别 |
| 决策层 | 推理规划 | CoT、ReAct、Planning |
| 行动层 | 执行任务 | Tool Use、代码执行 |
| 记忆层 | 存储检索 | 向量数据库、Embedding |

---

**下一章：** [Chapter 3: 从 Chatbot 到 Agent](chapter03-chatbot-to-agent.md)

---

*最后更新：2026-03-11*
