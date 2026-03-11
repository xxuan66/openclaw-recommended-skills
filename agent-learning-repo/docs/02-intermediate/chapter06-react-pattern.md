# Chapter 6: ReAct 模式详解

## 6.1 什么是 ReAct？

**ReAct = Reasoning + Acting（推理 + 行动）**

ReAct 是一种将推理（Reasoning）和行动（Acting）交替进行的 Agent 设计模式，让 LLM 能够在思考和行动之间灵活切换。

---

## 6.2 ReAct 的核心思想

### 传统方法的问题

```
方法1：纯推理（Chain-of-Thought）
问题 → 推理 → 推理 → 推理 → 答案
          ↑
    只能基于已有知识，无法获取新信息

方法2：纯行动（纯工具调用）
问题 → 行动 → 行动 → 行动 → 答案
          ↑
    没有思考过程，容易出错
```

### ReAct 的解决方案

```
ReAct 模式：
问题 → 思考 → 行动 → 观察 → 思考 → 行动 → 观察 → ... → 答案

Think: 我需要了解什么？
Act: 调用工具获取信息
Obs: 观察结果
Think: 基于新信息，下一步做什么？
Act: 调用工具
Obs: 观察结果
...
Answer: 最终答案
```

---

## 6.3 ReAct 的工作流程

### 经典示例：问答任务

```
问题：爱因斯坦在哪一年获得诺贝尔物理学奖？

Thought: 我需要搜索爱因斯坦的诺贝尔奖信息
Action: search("爱因斯坦 诺贝尔物理学奖 年份")
Observation: 爱因斯坦在1921年获得诺贝尔物理学奖，获奖原因是光电效应

Thought: 我已经获得了所需信息
Final Answer: 爱因斯坦在1921年获得诺贝尔物理学奖
```

---

## 6.4 ReAct 的实现

### 提示词模板

```python
REACT_PROMPT = """
你是一个智能助手，可以使用以下工具：
{tools}

请按照以下格式回答：

Question: 需要回答的问题
Thought: 思考应该做什么
Action: 工具名称
Action Input: 工具参数
Observation: 工具返回的结果
... (可以重复 Thought/Action/Observation)
Thought: 我已经获得足够信息
Final Answer: 最终答案

Question: {input}
"""
```

### 代码实现

```python
class ReActAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
    
    def run(self, question):
        history = []
        
        while True:
            # 生成思考
            thought = self.llm.generate(
                self._build_prompt(question, history)
            )
            
            # 解析行动
            action = self._parse_action(thought)
            
            if action == "final_answer":
                return self._parse_answer(thought)
            
            # 执行工具
            observation = self.tools[action["name"]].run(
                action["input"]
            )
            
            # 记录历史
            history.append({
                "thought": thought,
                "action": action,
                "observation": observation
            })
    
    def _build_prompt(self, question, history):
        prompt = REACT_PROMPT.format(
            input=question,
            tools=self._format_tools()
        )
        for h in history:
            prompt += f"\nThought: {h['thought']}"
            prompt += f"\nAction: {h['action']['name']}"
            prompt += f"\nObservation: {h['observation']}"
        return prompt
```

---

## 6.5 ReAct 的优势

### 1. 可解释性

```
每个思考步骤都可以被追踪：
- Agent 在想什么
- 为什么选择这个行动
- 观察到什么结果
```

### 2. 错误恢复

```
Thought: 我需要搜索天气
Action: search("明天天气")
Observation: 搜索失败，网络连接错误

Thought: 搜索失败，我应该使用备用方案
Action: search("天气预报 今天")
Observation: 成功返回结果
```

### 3. 灵活性

```
可以根据观察结果动态调整策略：
- 发现信息不足 → 继续搜索
- 发现矛盾 → 重新验证
- 获得足够信息 → 停止搜索
```

---

## 6.6 ReAct 的局限性

| 局限性 | 说明 | 解决方案 |
|--------|------|----------|
| **Token 消耗大** | 每一步都需要生成思考 | 优化提示词，减少步骤 |
| **可能循环** | 无限循环 | 设置最大步数限制 |
| **工具依赖** | 需要可靠的工具 | 工具健壮性设计 |
| **推理质量** | 依赖 LLM 能力 | 使用更强的模型 |

---

## 6.7 ReAct vs 其他模式

| 模式 | 特点 | 适用场景 |
|------|------|----------|
| **ReAct** | 推理+行动交替 | 需要外部信息的任务 |
| **CoT** | 纯推理链 | 无需外部工具的问题 |
| **Plan-and-Execute** | 先规划后执行 | 复杂多步骤任务 |
| **Tool Use** | 纯工具调用 | 简单的工具操作 |

---

## 6.8 实战示例：智能问答 Agent

```python
# 完整的 ReAct Agent 实现
from typing import List, Dict, Any

class SmartQAAgent:
    def __init__(self, llm, search_tool, calculator_tool):
        self.llm = llm
        self.tools = {
            "search": search_tool,
            "calculator": calculator_tool
        }
        self.max_steps = 10
    
    def answer(self, question: str) -> str:
        history = []
        
        for step in range(self.max_steps):
            # 生成思考和行动
            prompt = self._build_prompt(question, history)
            response = self.llm.generate(prompt)
            
            # 解析响应
            parsed = self._parse_response(response)
            
            if parsed["type"] == "final_answer":
                return parsed["answer"]
            
            # 执行行动
            tool_name = parsed["action"]
            tool_input = parsed["action_input"]
            observation = self.tools[tool_name].run(tool_input)
            
            # 记录历史
            history.append({
                "thought": parsed["thought"],
                "action": tool_name,
                "input": tool_input,
                "observation": observation
            })
        
        return "抱歉，无法找到答案"
```

---

## 6.9 小结

ReAct 模式让 Agent 能够：
- ✅ 在思考和行动之间灵活切换
- ✅ 动态获取外部信息
- ✅ 根据观察结果调整策略
- ✅ 提供可解释的推理过程

**核心循环：**
```
Think → Act → Observe → Think → Act → Observe → ... → Answer
```

---

**下一章：** [Chapter 7: Chain-of-Thought 思维链](chapter07-chain-of-thought.md)

---

*最后更新：2026-03-11*
