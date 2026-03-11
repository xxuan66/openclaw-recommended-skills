# Chapter 7: Chain-of-Thought 思维链

## 7.1 什么是 Chain-of-Thought (CoT)？

**Chain-of-Thought（思维链）** 是一种引导 LLM 进行逐步推理的提示技术，让模型在给出最终答案之前，先展示其推理过程。

---

## 7.2 为什么需要 CoT？

### 传统方法的问题

```
问题：一列火车以 60km/h 的速度行驶 2 小时，然后以 80km/h 的速度行驶 3 小时，总距离是多少？

传统方法（直接回答）：
答案：300km

问题：
- 复杂问题直接回答容易出错
- 无法展示推理过程
- 难以调试和验证
```

### CoT 方法

```
问题：同上

CoT 方法：
Step 1: 计算第一段距离
        60km/h × 2h = 120km

Step 2: 计算第二段距离
        80km/h × 3h = 240km

Step 3: 计算总距离
        120km + 240km = 360km

答案：360km
```

---

## 7.3 CoT 的类型

### 1. Zero-Shot CoT

**方法：** 只需在问题后加上"Let's think step by step"

```
问题：如果一个班级有 30 人，60% 是女生，女生中有 40% 戴眼镜，戴眼镜的女生有多少人？

Let's think step by step:
Step 1: 女生人数 = 30 × 60% = 18人
Step 2: 戴眼镜的女生 = 18 × 40% = 7.2人
Step 3: 人数必须是整数，所以是 7人

答案：7人
```

### 2. Few-Shot CoT

**方法：** 提供几个带推理过程的示例

```
示例1：
问题：苹果 3 元一个，买 5 个需要多少钱？
推理：3 × 5 = 15
答案：15元

示例2：
问题：一本书 25 元，打 8 折后多少钱？
推理：25 × 0.8 = 20
答案：20元

问题：一个笔记本 8 元，买 4 个打 9 折，需要多少钱？
推理：首先计算原价 8 × 4 = 32，然后打 9 折 32 × 0.9 = 28.8
答案：28.8元
```

### 3. Auto-CoT

**方法：** 自动为每个问题生成推理链

```python
def auto_cot(question):
    # 自动生成推理提示
    prompt = f"""
    问题：{question}
    
    请按照以下步骤推理：
    1. 识别关键信息
    2. 确定解题方法
    3. 逐步计算
    4. 验证答案
    """
    return llm.generate(prompt)
```

---

## 7.4 CoT 的实现

### 提示词模板

```python
COT_PROMPT = """
请逐步推理，回答以下问题。

问题：{question}

请按照以下格式输出：
Step 1: [推理步骤1]
Step 2: [推理步骤2]
...
Final Answer: [最终答案]
"""

# 使用
answer = llm.generate(COT_PROMPT.format(question="你的问题"))
```

### 代码实现

```python
class CoTAgent:
    def __init__(self, llm):
        self.llm = llm
    
    def solve(self, question: str) -> Dict[str, Any]:
        """使用 CoT 方法解决问题"""
        prompt = self._build_prompt(question)
        response = self.llm.generate(prompt)
        
        return self._parse_response(response)
    
    def _build_prompt(self, question: str) -> str:
        return f"""
请逐步推理，回答以下问题：

问题：{question}

推理步骤：
1. 分析问题
2. 识别关键信息
3. 确定解题方法
4. 逐步计算
5. 验证答案

请输出每一步的推理过程和最终答案。
"""
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        # 解析推理步骤和答案
        lines = response.strip().split('\n')
        steps = []
        answer = None
        
        for line in lines:
            if line.startswith('Step'):
                steps.append(line)
            elif 'Final Answer' in line or '答案' in line:
                answer = line.split(':')[-1].strip()
        
        return {
            "steps": steps,
            "answer": answer,
            "full_response": response
        }
```

---

## 7.5 CoT 的优势

### 1. 提高准确性

```
实验数据（GSM8K 数学题）：
- 无 CoT：~18% 准确率
- 有 CoT：~75% 准确率
```

### 2. 可解释性

```
用户可以看到：
- 模型是如何思考的
- 每一步的推理逻辑
- 可能出错的地方
```

### 3. 便于调试

```
如果答案错误，可以：
- 定位到具体哪个推理步骤出错
- 针对性地修正
- 提高模型的可靠性
```

---

## 7.6 CoT 的应用场景

### 适用场景

| 场景 | 示例 |
|------|------|
| **数学推理** | 应用题、计算题 |
| **逻辑推理** | 谜题、逻辑题 |
| **多步骤问题** | 复杂的任务分解 |
| **因果推理** | 分析原因和结果 |
| **代码调试** | 定位和修复 bug |

### 不适用场景

| 场景 | 原因 |
|------|------|
| 简单事实查询 | 无需推理 |
| 创意写作 | 不需要逻辑推理 |
| 闲聊 | 无明确目标 |

---

## 7.7 CoT 的高级技巧

### 1. Self-Consistency

```
方法：生成多个推理路径，选择最一致的答案

问题 → 推理路径1 → 答案A
     → 推理路径2 → 答案A  ← 最一致
     → 推理路径3 → 答案B

最终选择：答案A
```

### 2. Tree of Thoughts (ToT)

```
          问题
           |
     ┌─────┼─────┐
     ↓     ↓     ↓
   思路1 思路2 思路3
     |     |     |
   ┌─┴─┐ ┌─┴─┐ ┌─┴─┐
   ↓   ↓ ↓   ↓ ↓   ↓
  子思路...
```

### 3. Graph of Thoughts (GoT)

```
更复杂的推理图，支持合并、回溯等操作
```

---

## 7.8 小结

CoT 是一种强大的推理技术：

| 优点 | 说明 |
|------|------|
| **提高准确性** | 分步推理减少错误 |
| **可解释性** | 展示推理过程 |
| **便于调试** | 定位问题所在 |
| **通用性** | 适用于各种推理任务 |

**核心思想：** 把复杂问题分解为简单的步骤，逐步推理。

---

**下一章：** [Chapter 8: Planning & Reasoning](chapter08-planning-reasoning.md)

---

*最后更新：2026-03-11*
