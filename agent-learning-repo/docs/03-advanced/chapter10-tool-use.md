# Chapter 10: Agent 工具使用

## 10.1 什么是 Tool Use？

**Tool Use（工具使用）** 是 Agent 调用外部工具来扩展自身能力的核心技术。

```
┌─────────────────────────────────────────────────────────┐
│                      Agent                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│    "我需要搜索天气信息"                                   │
│            ↓                                            │
│    ┌─────────────────────────────────┐                  │
│    │         工具选择器               │                  │
│    └─────────────────────────────────┘                  │
│            ↓                                            │
│    ┌─────────┐ ┌─────────┐ ┌─────────┐                 │
│    │  搜索   │ │  计算   │ │  代码   │  ...            │
│    │  工具   │ │  工具   │ │  工具   │                 │
│    └─────────┘ └─────────┘ └─────────┘                 │
│            ↓                                            │
│    "上海明天天气：阴转小雨，12-18°C"                     │
└─────────────────────────────────────────────────────────┘
```

---

## 10.2 为什么 Agent 需要工具？

### LLM 的局限性

| 局限性 | 说明 | 工具解决方案 |
|--------|------|-------------|
| **知识截止** | 训练数据有时间限制 | 搜索工具获取实时信息 |
| **无法执行代码** | 只能生成，不能运行 | 代码执行工具 |
| **无法访问外部系统** | 不能调用 API | API 调用工具 |
| **计算能力有限** | 复杂计算能力弱 | 计算器工具 |
| **无法操作文件** | 不能读写本地文件 | 文件工具 |

---

## 10.3 工具类型

### 1. 搜索工具（Search Tools）

```python
search_tool = {
    "name": "web_search",
    "description": "搜索互联网获取实时信息",
    "parameters": {
        "query": {"type": "string", "description": "搜索关键词"},
        "max_results": {"type": "integer", "description": "最大结果数"}
    }
}

# 使用
result = web_search("上海明天天气")
```

### 2. 代码执行工具（Code Execution）

```python
code_tool = {
    "name": "python_executor",
    "description": "执行 Python 代码",
    "parameters": {
        "code": {"type": "string", "description": "Python 代码"}
    }
}

# 使用
result = python_executor("print(2 + 2)")
# 输出: 4
```

### 3. 计算器工具（Calculator）

```python
calculator_tool = {
    "name": "calculator",
    "description": "执行数学计算",
    "parameters": {
        "expression": {"type": "string", "description": "数学表达式"}
    }
}

# 使用
result = calculator("(3 + 5) * 2")
# 输出: 16
```

### 4. 文件操作工具（File Operations）

```python
file_tools = {
    "read_file": {
        "description": "读取文件内容",
        "parameters": {"path": {"type": "string"}}
    },
    "write_file": {
        "description": "写入文件",
        "parameters": {
            "path": {"type": "string"},
            "content": {"type": "string"}
        }
    }
}
```

### 5. API 调用工具（API Caller）

```python
api_tool = {
    "name": "http_request",
    "description": "发送 HTTP 请求",
    "parameters": {
        "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE"]},
        "url": {"type": "string"},
        "body": {"type": "object"}
    }
}
```

---

## 10.4 工具选择机制

### 1. 基于描述的选择

```python
def select_tool(query: str, tools: List[Tool]) -> Tool:
    """根据查询选择最合适的工具"""
    prompt = f"""
    问题：{query}
    
    可用工具：
    {format_tools(tools)}
    
    请选择最合适的工具，并说明原因。
    """
    
    response = llm.generate(prompt)
    return parse_tool_selection(response, tools)
```

### 2. 基于功能匹配

```python
def match_tool(task: str, tools: Dict[str, Tool]) -> str:
    """根据任务功能匹配工具"""
    # 分析任务类型
    task_type = analyze_task(task)
    
    # 匹配工具
    if task_type == "search":
        return "web_search"
    elif task_type == "calculation":
        return "calculator"
    elif task_type == "code":
        return "python_executor"
    # ...
```

### 3. 组合使用

```python
def complex_task(query: str):
    """复杂任务需要组合多个工具"""
    # Step 1: 搜索信息
    search_result = web_search(query)
    
    # Step 2: 分析数据
    analysis_result = python_executor(analyze_code(search_result))
    
    # Step 3: 生成报告
    report = llm.generate(f"根据分析结果生成报告：{analysis_result}")
    
    return report
```

---

## 10.5 工具使用最佳实践

### 1. 工具设计原则

```
✅ 好的工具设计：
- 功能单一明确
- 参数清晰
- 错误处理完善
- 返回值格式一致

❌ 不好的工具设计：
- 功能过于复杂
- 参数模糊
- 无错误处理
- 返回值不一致
```

### 2. 安全考虑

```python
# 安全的代码执行
def safe_execute(code: str) -> str:
    # 1. 白名单检查
    if not is_safe_code(code):
        raise SecurityError("代码包含危险操作")
    
    # 2. 沙箱执行
    result = execute_in_sandbox(code, timeout=10)
    
    # 3. 结果验证
    return sanitize_output(result)
```

### 3. 错误处理

```python
def robust_tool_call(tool: Tool, params: dict, max_retries: int = 3):
    """带重试的工具调用"""
    for attempt in range(max_retries):
        try:
            return tool.run(params)
        except ToolError as e:
            if attempt == max_retries - 1:
                raise
            # 重试前等待
            time.sleep(2 ** attempt)
```

---

## 10.6 Function Calling 格式

### OpenAI Function Calling

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    },
                    "date": {
                        "type": "string",
                        "description": "日期，格式 YYYY-MM-DD"
                    }
                },
                "required": ["city"]
            }
        }
    }
]
```

### Anthropic Tool Use

```python
tools = [
    {
        "name": "get_weather",
        "description": "获取指定城市的天气信息",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称"
                }
            },
            "required": ["city"]
        }
    }
]
```

---

## 10.7 实战：构建工具调用 Agent

```python
from typing import List, Dict, Any
import json

class ToolAgent:
    def __init__(self, llm, tools: Dict[str, callable]):
        self.llm = llm
        self.tools = tools
    
    def run(self, user_input: str) -> str:
        # 构建提示词
        prompt = self._build_prompt(user_input)
        
        # 获取 LLM 响应
        response = self.llm.generate(prompt)
        
        # 解析工具调用
        tool_calls = self._parse_tool_calls(response)
        
        # 执行工具
        results = []
        for call in tool_calls:
            result = self._execute_tool(call)
            results.append(result)
        
        # 生成最终回复
        return self._generate_final_response(user_input, results)
    
    def _build_prompt(self, user_input: str) -> str:
        tools_desc = self._format_tools()
        return f"""
你是一个智能助手，可以使用以下工具：

{tools_desc}

用户问题：{user_input}

请根据需要调用工具，格式如下：
{{
    "tool": "工具名称",
    "parameters": {{...}}
}}
"""
    
    def _execute_tool(self, call: Dict[str, Any]) -> Any:
        tool_name = call["tool"]
        params = call["parameters"]
        
        if tool_name in self.tools:
            return self.tools[tool_name](**params)
        else:
            raise ValueError(f"未知工具：{tool_name}")
```

---

## 10.8 小结

Tool Use 是 Agent 扩展能力的关键：

| 能力 | 工具类型 | 应用场景 |
|------|----------|----------|
| **信息获取** | 搜索工具 | 实时信息查询 |
| **计算能力** | 计算器 | 数学运算 |
| **代码执行** | 代码工具 | 自动化脚本 |
| **文件操作** | 文件工具 | 文档处理 |
| **API 调用** | HTTP 工具 | 服务集成 |

**关键点：**
- 工具让 Agent 突破 LLM 的局限
- 安全的工具设计至关重要
- 合理的工具选择机制

---

**下一章：** [Chapter 11: Agent 记忆系统](chapter11-memory-systems.md)

---

*最后更新：2026-03-11*
