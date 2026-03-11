# Chapter 9: Multi-Agent 多智能体系统

## 9.1 什么是 Multi-Agent 系统？

**Multi-Agent 系统（多智能体系统）** 是由多个 Agent 协作完成复杂任务的系统架构。

```
┌─────────────────────────────────────────────────────────┐
│                   Multi-Agent 系统                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│    ┌─────────┐         ┌─────────┐         ┌─────────┐ │
│    │ Agent 1 │  ←───→  │ Agent 2 │  ←───→  │ Agent 3 │ │
│    │ (搜索)  │         │ (分析)  │         │ (撰写)  │ │
│    └─────────┘         └─────────┘         └─────────┘ │
│         ↑                   ↑                   ↑      │
│         │                   │                   │      │
│         └───────────────────┴───────────────────┘      │
│                          ↑                              │
│                     协调器/用户                          │
└─────────────────────────────────────────────────────────┘
```

---

## 9.2 为什么需要 Multi-Agent？

### 单 Agent 的局限性

| 问题 | 说明 |
|------|------|
| **能力有限** | 一个 Agent 难以擅长所有领域 |
| **效率瓶颈** | 串行执行，无法并行处理 |
| **视角单一** | 缺乏多角度思考 |
| **复杂度限制** | 难以处理超复杂任务 |

### Multi-Agent 的优势

| 优势 | 说明 |
|------|------|
| **专业化分工** | 每个 Agent 专注特定任务 |
| **并行处理** | 多个 Agent 同时工作 |
| **多视角分析** | 不同 Agent 提供不同观点 |
| **协作增强** | 1+1>2 的效果 |

---

## 9.3 Multi-Agent 架构模式

### 1. 协作模式（Collaborative）

```
Agent A ←─→ Agent B ←─→ Agent C
   ↓           ↓           ↓
 任务A       任务B       任务C
   ↓           ↓           ↓
   └───────────┴───────────┘
               ↓
            最终结果
```

**示例：**
- Agent A：搜索信息
- Agent B：分析数据
- Agent C：生成报告

### 2. 监督模式（Supervisor）

```
         ┌──────────────┐
         │   监督者      │
         │  (Supervisor) │
         └──────┬───────┘
                ↓
    ┌───────────┴───────────┐
    ↓           ↓           ↓
┌───────┐   ┌───────┐   ┌───────┐
│Agent 1│   │Agent 2│   │Agent 3│
└───────┘   └───────┘   └───────┘
```

**示例：**
- 监督者：项目经理，分配任务
- Agent 1-3：执行具体任务

### 3. 辩论模式（Debate）

```
      ┌───────┐
      │ Agent │
      │   A   │
      └───┬───┘
          ↓
    ┌─────────┐
    │  辩论   │
    │         │
    └─────────┘
          ↑
      ┌───┴───┐
      │ Agent │
      │   B   │
      └───────┘
```

**示例：**
- Agent A：支持方案 X
- Agent B：支持方案 Y
- 通过辩论得出最佳方案

### 4. 流水线模式（Pipeline）

```
Agent 1 → Agent 2 → Agent 3 → Agent 4
  ↓         ↓         ↓         ↓
处理1     处理2     处理3     处理4
  ↓         ↓         ↓         ↓
中间结果  中间结果  中间结果  最终结果
```

---

## 9.4 Multi-Agent 通信

### 通信协议

```python
# Agent 间消息格式
message = {
    "from": "agent_1",
    "to": "agent_2",
    "type": "request|response|notification",
    "content": {...},
    "timestamp": "2026-03-11T12:00:00Z"
}
```

### 通信方式

| 方式 | 说明 | 适用场景 |
|------|------|----------|
| **直接通信** | Agent 间直接发送消息 | 简单协作 |
| **广播** | 一对多消息 | 通知所有 Agent |
| **发布订阅** | 基于主题的消息传递 | 复杂协作 |
| **共享内存** | 通过共享空间交换信息 | 状态同步 |

---

## 9.5 实战：AutoGen 框架

### Microsoft AutoGen

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat

# 创建 Agent
coder = AssistantAgent(
    "coder",
    llm_config=llm_config,
    system_message="你是一个 Python 编程专家"
)

reviewer = AssistantAgent(
    "reviewer",
    llm_config=llm_config,
    system_message="你是一个代码审查专家"
)

tester = AssistantAgent(
    "tester",
    llm_config=llm_config,
    system_message="你是一个测试专家"
)

# 创建 Group Chat
groupchat = GroupChat(
    agents=[coder, reviewer, tester],
    messages=[],
    max_round=10
)

# 启动对话
manager = GroupChatManager(groupchat=groupchat)
user_proxy.initiate_chat(
    manager,
    message="帮我写一个快速排序算法，并进行代码审查和测试"
)
```

---

## 9.6 实战：LangGraph

### 图结构的 Multi-Agent

```python
from langgraph import Graph, END

# 定义 Agent 节点
def researcher(state):
    # 搜索信息
    return {"research": "搜索结果..."}

def analyst(state):
    # 分析数据
    return {"analysis": "分析报告..."}

def writer(state):
    # 生成报告
    return {"report": "最终报告..."}

# 构建图
workflow = Graph()
workflow.add_node("researcher", researcher)
workflow.add_node("analyst", analyst)
workflow.add_node("writer", writer)

# 添加边
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "writer")
workflow.add_edge("writer", END)

# 设置入口
workflow.set_entry_point("researcher")

# 编译并运行
app = workflow.compile()
result = app.invoke({"input": "研究 Agent 发展趋势"})
```

---

## 9.7 Multi-Agent 的挑战

### 1. 协调复杂性

```
问题：Agent 间如何高效协作？
解决方案：
- 明确的角色定义
- 清晰的通信协议
- 协调者角色
```

### 2. 一致性问题

```
问题：不同 Agent 可能产生冲突的结果
解决方案：
- 冲突检测机制
- 仲裁机制
- 多数投票
```

### 3. 资源消耗

```
问题：多个 Agent 同时运行，消耗大量资源
解决方案：
- 按需启动 Agent
- 复用 Agent 实例
- 优化通信开销
```

### 4. 调试困难

```
问题：多个 Agent 交互，难以追踪问题
解决方案：
- 详细日志
- 可视化工具
- 单元测试
```

---

## 9.8 Multi-Agent 应用场景

| 场景 | Agent 角色 | 协作方式 |
|------|-----------|----------|
| **软件开发** | 架构师、开发者、审查者、测试者 | 流水线 |
| **内容创作** | 研究员、写手、编辑、校对 | 流水线 |
| **数据分析** | 数据采集、清洗、分析、可视化 | 流水线 |
| **客服系统** | 接待员、专家、质检员 | 监督模式 |
| **决策支持** | 分析员、建议者、评估者 | 辩论模式 |

---

## 9.9 小结

Multi-Agent 系统让 AI 能够：

| 能力 | 说明 |
|------|------|
| **专业化** | 每个 Agent 专注特定领域 |
| **协作** | Agent 间高效沟通协作 |
| **并行** | 同时处理多个任务 |
| **复杂任务** | 处理超复杂问题 |

**关键原则：**
- 明确角色分工
- 设计清晰的通信协议
- 引入协调机制
- 处理冲突和一致性

---

**下一章：** [Chapter 10: Agent 工具使用](chapter10-tool-use.md)

---

*最后更新：2026-03-11*
