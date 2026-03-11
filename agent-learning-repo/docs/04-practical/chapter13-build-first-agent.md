# Chapter 13: 构建你的第一个 Agent

## 13.1 准备工作

### 环境要求

```bash
# Python 3.8+
python --version

# 安装依赖
pip install openai langchain chromadb
```

### API Key 配置

```bash
# 设置环境变量
export OPENAI_API_KEY="your-api-key"
```

---

## 13.2 最简单的 Agent

### 使用 OpenAI API

```python
from openai import OpenAI

client = OpenAI()

class SimpleAgent:
    def __init__(self, model="gpt-4"):
        self.model = model
        self.conversation = []
    
    def chat(self, message: str) -> str:
        # 添加用户消息
        self.conversation.append({
            "role": "user",
            "content": message
        })
        
        # 调用 API
        response = client.chat.completions.create(
            model=self.model,
            messages=self.conversation
        )
        
        # 获取回复
        reply = response.choices[0].message.content
        
        # 添加助手回复
        self.conversation.append({
            "role": "assistant",
            "content": reply
        })
        
        return reply

# 使用
agent = SimpleAgent()
print(agent.chat("你好，我是张三"))
print(agent.chat("我的名字是什么？"))
```

---

## 13.3 带工具的 Agent

### 定义工具

```python
import json

def get_weather(city: str) -> str:
    """获取指定城市的天气"""
    # 实际应用中调用天气 API
    return f"{city}今天晴，22°C"

def calculate(expression: str) -> str:
    """执行数学计算"""
    try:
        result = eval(expression)
        return str(result)
    except:
        return "计算错误"

# 工具定义
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式"}
                },
                "required": ["expression"]
            }
        }
    }
]
```

### 带工具的 Agent

```python
class ToolAgent:
    def __init__(self, model="gpt-4"):
        self.model = model
        self.client = OpenAI()
        self.tools = {
            "get_weather": get_weather,
            "calculate": calculate
        }
    
    def run(self, user_input: str) -> str:
        messages = [{"role": "user", "content": user_input}]
        
        while True:
            # 调用 LLM
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            # 检查是否有工具调用
            if message.tool_calls:
                # 添加助手消息（带工具调用）
                messages.append(message)
                
                # 执行工具
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)
                    
                    if function_name in self.tools:
                        result = self.tools[function_name](**arguments)
                    else:
                        result = f"未知工具：{function_name}"
                    
                    # 添加工具结果
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
            else:
                # 返回最终回复
                return message.content

# 使用
agent = ToolAgent()
print(agent.run("上海今天天气怎么样？"))
print(agent.run("123 乘以 456 等于多少？"))
```

---

## 13.4 带记忆的 Agent

```python
class MemoryAgent:
    def __init__(self, model="gpt-4"):
        self.model = model
        self.client = OpenAI()
        self.memory = []  # 简单列表实现
    
    def chat(self, user_input: str) -> str:
        # 添加用户消息
        self.memory.append({
            "role": "user",
            "content": user_input
        })
        
        # 构建对话历史（保留最近 10 条）
        messages = self.memory[-10:]
        
        # 调用 LLM
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        
        reply = response.choices[0].message.content
        
        # 添加助手回复
        self.memory.append({
            "role": "assistant",
            "content": reply
        })
        
        return reply

# 使用
agent = MemoryAgent()
agent.chat("我叫张三，我喜欢编程")
agent.chat("我是谁？")  # 应该记住用户是张三
```

---

## 13.5 完整示例：智能助手 Agent

```python
from openai import OpenAI
import json
from datetime import datetime

class SmartAssistant:
    def __init__(self, model="gpt-4"):
        self.model = model
        self.client = OpenAI()
        self.memory = []
        self.tools = self._setup_tools()
    
    def _setup_tools(self):
        """设置工具"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "获取指定城市的天气",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {"type": "string"}
                        },
                        "required": ["city"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search",
                    "description": "搜索互联网获取信息",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate",
                    "description": "执行数学计算",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {"type": "string"}
                        },
                        "required": ["expression"]
                    }
                }
            }
        ]
    
    def _execute_tool(self, name: str, arguments: dict) -> str:
        """执行工具"""
        if name == "get_weather":
            return f"{arguments['city']}今天晴，22°C"
        elif name == "search":
            return f"关于'{arguments['query']}'的搜索结果..."
        elif name == "calculate":
            try:
                return str(eval(arguments["expression"]))
            except:
                return "计算错误"
        return "未知工具"
    
    def chat(self, user_input: str) -> str:
        # 添加用户消息
        self.memory.append({
            "role": "user",
            "content": user_input
        })
        
        # 系统提示
        system_prompt = """
你是一个智能助手，可以帮助用户完成各种任务。
你可以使用以下工具：
1. get_weather: 获取天气
2. search: 搜索信息
3. calculate: 数学计算

请根据用户需求选择合适的工具。
"""
        
        messages = [
            {"role": "system", "content": system_prompt}
        ] + self.memory[-10:]  # 保留最近 10 条
        
        while True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            if message.tool_calls:
                messages.append(message)
                
                for tool_call in message.tool_calls:
                    result = self._execute_tool(
                        tool_call.function.name,
                        json.loads(tool_call.function.arguments)
                    )
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
            else:
                reply = message.content
                
                self.memory.append({
                    "role": "assistant",
                    "content": reply
                })
                
                return reply

# 使用示例
agent = SmartAssistant()

print("=== 智能助手演示 ===")
print(f"Q: 北京天气怎么样？")
print(f"A: {agent.chat('北京天气怎么样？')}")
print()
print(f"Q: 2 的 10 次方是多少？")
print(f"A: {agent.chat('2 的 10 次方是多少？')}")
print()
print(f"Q: 我叫张三")
print(f"A: {agent.chat('我叫张三')}")
print()
print(f"Q: 我是谁？")
print(f"A: {agent.chat('我是谁？')}")
```

---

## 13.6 调试和优化

### 调试技巧

```python
# 1. 查看完整的对话历史
print(agent.memory)

# 2. 查看工具调用
# 在 _execute_tool 方法中添加日志
print(f"调用工具：{name}，参数：{arguments}")

# 3. 错误处理
try:
    result = agent.chat(user_input)
except Exception as e:
    print(f"错误：{e}")
    # 查看详细错误信息
    import traceback
    traceback.print_exc()
```

### 优化建议

1. **优化提示词** - 清晰的系统提示
2. **限制对话长度** - 防止 token 超限
3. **工具选择优化** - 准确选择合适工具
4. **错误重试** - 自动重试失败的工具调用

---

## 13.7 下一步

恭喜你构建了第一个 Agent！接下来可以：

1. **添加更多工具** - 搜索、数据库、API 等
2. **实现长期记忆** - 使用向量数据库
3. **构建 Multi-Agent 系统** - 多个 Agent 协作
4. **部署到生产环境** - 添加安全和监控

---

**下一章：** [Chapter 14: 常见 Agent 框架对比](chapter14-frameworks-comparison.md)

---

*最后更新：2026-03-11*
