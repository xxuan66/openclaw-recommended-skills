# Chapter 14: 常见 Agent 框架对比

## 14.1 框架概览

### 主流 Agent 框架

| 框架 | 开发者 | 特点 | 适用场景 |
|------|--------|------|----------|
| **LangChain** | LangChain Inc. | 生态丰富、功能全面 | 通用 Agent 开发 |
| **AutoGen** | Microsoft | Multi-Agent 原生 | 多 Agent 协作 |
| **CrewAI** | CrewAI | 角色分工明确 | 团队协作 Agent |
| **Semantic Kernel** | Microsoft | 企业级、.NET 友好 | 企业应用 |
| **LlamaIndex** | LlamaIndex | 数据/检索优化 | RAG 应用 |
| **OpenAI Assistants** | OpenAI | 官方支持、简单 | 快速原型 |

---

## 14.2 LangChain

### 特点

```
✅ 优点：
- 生态系统最丰富
- 大量预构建组件
- 社区活跃
- 文档完善

❌ 缺点：
- 学习曲线较陡
- 抽象层级多，有时难以调试
- 版本更新快，API 变化多
```

### 快速入门

```python
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# 创建 Agent
llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有用的助手"),
    ("user", "{input}")
])

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# 使用
result = agent_executor.invoke({"input": "帮我查询天气"})
print(result["output"])
```

### 适用场景

- 需要快速搭建 Agent 原型
- 需要丰富的工具集成
- RAG + Agent 的应用

---

## 14.3 AutoGen (Microsoft)

### 特点

```
✅ 优点：
- Multi-Agent 原生支持
- 角色定义清晰
- 对话式协作
- 企业级支持

❌ 缺点：
- 相对较新，生态较小
- 学习曲线中等
- 文档还在完善中
```

### 快速入门

```python
from autogen import AssistantAgent, UserProxyAgent, GroupChat

# 创建 Agent
assistant = AssistantAgent(
    "assistant",
    llm_config={"model": "gpt-4"},
    system_message="你是一个编程专家"
)

user_proxy = UserProxyAgent(
    "user_proxy",
    code_execution_config={"work_dir": "coding"}
)

# 多 Agent 协作
groupchat = GroupChat(
    agents=[assistant, user_proxy],
    messages=[],
    max_round=10
)

manager = GroupChatManager(groupchat=groupchat)
user_proxy.initiate_chat(
    manager,
    message="帮我写一个快速排序算法"
)
```

### 适用场景

- Multi-Agent 协作系统
- 复杂任务分解
- 代码生成和审查

---

## 14.4 CrewAI

### 特点

```
✅ 优点：
- 角色和任务定义清晰
- 适合团队协作场景
- 易于理解的 API

❌ 缺点：
- 相对较新
- 社区较小
- 功能相对有限
```

### 快速入门

```python
from crewai import Agent, Task, Crew

# 定义 Agent
researcher = Agent(
    role="研究员",
    goal="搜集相关信息",
    backstory="你是一个专业的研究员",
    verbose=True
)

writer = Agent(
    role="写手",
    goal="撰写高质量文章",
    backstory="你是一个经验丰富的写手",
    verbose=True
)

# 定义任务
research_task = Task(
    description="搜集 Agent 发展趋势的最新信息",
    agent=researcher
)

write_task = Task(
    description="根据研究结果撰写一篇技术文章",
    agent=writer
)

# 创建 Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    verbose=True
)

# 执行
result = crew.kickoff()
```

### 适用场景

- 内容创作团队
- 研究和分析
- 多角色协作任务

---

## 14.5 Semantic Kernel

### 特点

```
✅ 优点：
- 企业级设计
- .NET 生态友好
- 插件系统完善
- 微软官方支持

❌ 缺点：
- Python 支持相对较弱
- 学习曲线中等
- 主要面向企业用户
```

### 快速入门

```python
# Python 版本
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

kernel = sk.Kernel()
kernel.add_chat_service(
    "chat",
    OpenAIChatCompletion("gpt-4", "your-api-key")
)

# 添加插件
plugin = kernel.import_semantic_skill_from_directory("plugins", "MyPlugin")

# 执行
result = await kernel.run_async(
    plugin["MyFunction"],
    input_str="你的输入"
)
```

### 适用场景

- 企业级应用
- .NET 技术栈
- 需要插件系统

---

## 14.6 OpenAI Assistants API

### 特点

```
✅ 优点：
- 官方支持，稳定可靠
- 配置简单
- 内置工具（代码解释器、文件搜索等）
- 无需额外框架

❌ 缺点：
- 依赖 OpenAI 服务
- 自定义能力有限
- 成本较高
```

### 快速入门

```python
from openai import OpenAI

client = OpenAI()

# 创建 Assistant
assistant = client.beta.assistants.create(
    name="My Assistant",
    instructions="你是一个有用的助手",
    model="gpt-4",
    tools=[{"type": "code_interpreter"}]
)

# 创建线程
thread = client.beta.threads.create()

# 添加消息
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="帮我分析这个数据"
)

# 运行
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)

# 获取结果
messages = client.beta.threads.messages.list(thread_id=thread.id)
```

### 适用场景

- 快速原型
- 简单 Agent 应用
- 不想维护复杂框架

---

## 14.7 框架选择指南

### 选择流程图

```
你需要什么？
    │
    ├── 快速原型 → OpenAI Assistants API
    │
    ├── 复杂 Agent 系统 → LangChain
    │
    ├── Multi-Agent 协作 → AutoGen 或 CrewAI
    │
    ├── RAG 应用 → LlamaIndex
    │
    ├── 企业应用 → Semantic Kernel
    │
    └── 不确定 → 先用 LangChain，后期迁移
```

### 决策矩阵

| 需求 | 推荐框架 | 理由 |
|------|----------|------|
| **快速原型** | OpenAI Assistants | 最简单 |
| **功能丰富** | LangChain | 最全面 |
| **多 Agent** | AutoGen | 原生支持 |
| **团队协作** | CrewAI | 角色清晰 |
| **企业级** | Semantic Kernel | 微软支持 |
| **RAG 优化** | LlamaIndex | 检索强大 |

---

## 14.8 框架对比总结

| 维度 | LangChain | AutoGen | CrewAI | Semantic Kernel | OpenAI Assistants |
|------|-----------|---------|--------|-----------------|-------------------|
| **学习曲线** | 中等 | 中等 | 低 | 中等 | 低 |
| **功能丰富度** | 高 | 中 | 中 | 高 | 中 |
| **Multi-Agent** | 支持 | 原生 | 原生 | 支持 | 不支持 |
| **社区** | 大 | 中 | 小 | 中 | 官方 |
| **文档** | 好 | 好 | 中 | 好 | 好 |
| **企业支持** | 中 | 好 | 差 | 好 | 好 |

---

## 14.9 小结

选择 Agent 框架需要考虑：

1. **项目需求** - 复杂度、规模、功能要求
2. **团队技能** - 现有技术栈、学习能力
3. **长期维护** - 社区活跃度、文档质量
4. **成本** - API 费用、开发成本

**建议：**
- 新手从 **LangChain** 或 **OpenAI Assistants** 开始
- Multi-Agent 需求选 **AutoGen**
- 企业应用选 **Semantic Kernel**

---

**下一章：** [Chapter 15: Agent 应用案例](chapter15-use-cases.md)

---

*最后更新：2026-03-11*
