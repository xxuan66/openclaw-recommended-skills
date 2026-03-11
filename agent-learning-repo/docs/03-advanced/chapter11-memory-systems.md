# Chapter 11: Agent 记忆系统

## 11.1 为什么 Agent 需要记忆？

### LLM 的记忆局限

```
标准 LLM 对话：
用户：我叫张三，喜欢编程
Agent：你好张三，很高兴认识你！
用户：我喜欢什么？
Agent：抱歉，我没有这个信息（忘记之前的对话）
```

### 记忆系统的作用

```
┌─────────────────────────────────────────────────────────┐
│                      Agent 记忆系统                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐  │
│  │   短期记忆    │    │   长期记忆    │    │ 工作记忆 │  │
│  │  (会话级)    │    │   (永久)     │    │ (任务级) │  │
│  └──────────────┘    └──────────────┘    └──────────┘  │
│         ↓                    ↓                ↓        │
│  ┌──────────────────────────────────────────────────┐  │
│  │                 记忆检索系统                       │  │
│  └──────────────────────────────────────────────────┘  │
│                         ↓                               │
│              "张三喜欢编程" → 可被检索                    │
└─────────────────────────────────────────────────────────┘
```

---

## 11.2 记忆类型

### 1. 短期记忆（Short-term Memory）

**特点：**
- 当前会话有效
- 容量有限
- 自动过期

**实现：**
```python
class ShortTermMemory:
    def __init__(self, max_size: int = 10):
        self.messages = []
        self.max_size = max_size
    
    def add(self, message: str):
        self.messages.append({
            "content": message,
            "timestamp": datetime.now()
        })
        # 限制容量
        if len(self.messages) > self.max_size:
            self.messages.pop(0)
    
    def get_recent(self, n: int = 5) -> List[str]:
        return self.messages[-n:]
```

### 2. 长期记忆（Long-term Memory）

**特点：**
- 持久化存储
- 无限容量
- 可检索

**实现：**
```python
class LongTermMemory:
    def __init__(self, vector_db):
        self.vector_db = vector_db
    
    def store(self, key: str, content: str):
        """存储长期记忆"""
        embedding = self.get_embedding(content)
        self.vector_db.insert({
            "id": key,
            "content": content,
            "embedding": embedding
        })
    
    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        """检索相关记忆"""
        query_embedding = self.get_embedding(query)
        results = self.vector_db.search(query_embedding, top_k)
        return [r["content"] for r in results]
```

### 3. 工作记忆（Working Memory）

**特点：**
- 任务相关的临时存储
- 中间计算结果
- 任务完成后清空

**实现：**
```python
class WorkingMemory:
    def __init__(self):
        self.data = {}
    
    def set(self, key: str, value: Any):
        self.data[key] = value
    
    def get(self, key: str) -> Any:
        return self.data.get(key)
    
    def clear(self):
        self.data.clear()
```

---

## 11.3 记忆存储方式

### 1. 向量数据库（Vector Database）

```
记忆内容 → Embedding → 向量存储 → 相似度检索
```

**常用向量数据库：**
- ChromaDB
- Pinecone
- Weaviate
- Qdrant

**示例：**
```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("memories")

# 存储
collection.add(
    documents=["张三喜欢编程", "张三是程序员"],
    ids=["mem1", "mem2"]
)

# 检索
results = collection.query(
    query_texts=["张三的爱好"],
    n_results=2
)
```

### 2. 图数据库（Graph Database）

```
实体 → 关系 → 实体
    ↓
  知识图谱
```

**适用场景：**
- 复杂关系存储
- 知识推理
- 因果链分析

### 3. 关系数据库

```
结构化数据存储：
- 用户信息
- 任务记录
- 事件日志
```

---

## 11.4 记忆检索策略

### 1. 基于相似度的检索

```python
def retrieve_by_similarity(query: str, memories: List[str]) -> List[str]:
    """基于语义相似度检索记忆"""
    query_embedding = embed(query)
    
    scored_memories = []
    for memory in memories:
        memory_embedding = embed(memory)
        similarity = cosine_similarity(query_embedding, memory_embedding)
        scored_memories.append((memory, similarity))
    
    # 按相似度排序
    scored_memories.sort(key=lambda x: x[1], reverse=True)
    
    return [m for m, _ in scored_memories[:5]]
```

### 2. 基于时间的检索

```python
def retrieve_recent_memories(days: int = 7) -> List[str]:
    """检索最近 N 天的记忆"""
    cutoff = datetime.now() - timedelta(days=days)
    return [m for m in all_memories if m.timestamp > cutoff]
```

### 3. 基于重要性的检索

```python
def retrieve_important_memories(threshold: float = 0.8) -> List[str]:
    """检索重要记忆"""
    return [m for m in all_memories if m.importance > threshold]
```

---

## 11.5 记忆管理

### 1. 记忆压缩

```
原始记忆（大量）
    ↓
压缩/摘要
    ↓
精简记忆（核心信息）
```

**实现：**
```python
def compress_memories(memories: List[str]) -> str:
    """压缩多个记忆为一个摘要"""
    prompt = f"""
    请将以下记忆压缩为一个简洁的摘要：
    
    {chr(10).join(memories)}
    """
    return llm.generate(prompt)
```

### 2. 记忆遗忘

```python
def forget_old_memories(days: int = 30):
    """遗忘超过 N 天的低重要性记忆"""
    cutoff = datetime.now() - timedelta(days=days)
    
    for memory in all_memories:
        if memory.timestamp < cutoff and memory.importance < 0.5:
            memory.delete()
```

### 3. 记忆更新

```python
def update_memory(memory_id: str, new_content: str):
    """更新已有的记忆"""
    memory = get_memory(memory_id)
    
    # 合并新旧内容
    prompt = f"""
    旧记忆：{memory.content}
    新信息：{new_content}
    
    请合并为更新后的记忆：
    """
    
    updated = llm.generate(prompt)
    memory.update(updated)
```

---

## 11.6 实战：完整记忆系统

```python
class AgentMemorySystem:
    def __init__(self, vector_db):
        self.short_term = ShortTermMemory(max_size=20)
        self.long_term = LongTermMemory(vector_db)
        self.working = WorkingMemory()
    
    def remember(self, content: str, importance: float = 0.5):
        """存储记忆"""
        # 短期记忆
        self.short_term.add(content)
        
        # 重要记忆存入长期记忆
        if importance > 0.7:
            self.long_term.store(
                key=f"mem_{datetime.now().timestamp()}",
                content=content
            )
    
    def recall(self, query: str) -> List[str]:
        """检索记忆"""
        # 短期记忆
        short_term_results = self.short_term.get_recent(5)
        
        # 长期记忆
        long_term_results = self.long_term.retrieve(query, top_k=3)
        
        # 合并结果
        return short_term_results + long_term_results
    
    def think(self, context: str) -> str:
        """基于记忆进行思考"""
        # 检索相关记忆
        relevant_memories = self.recall(context)
        
        prompt = f"""
        上下文：{context}
        
        相关记忆：
        {chr(10).join(relevant_memories)}
        
        基于以上信息，给出分析和建议：
        """
        
        return llm.generate(prompt)
```

---

## 11.7 记忆系统的挑战

| 挑战 | 说明 | 解决方案 |
|------|------|----------|
| **记忆爆炸** | 记忆太多，检索效率下降 | 压缩、遗忘策略 |
| **记忆冲突** | 不同记忆矛盾 | 时效性、可信度加权 |
| **隐私问题** | 用户数据安全 | 加密、访问控制 |
| **检索质量** | 检索到不相关记忆 | 改进 embedding、重排序 |

---

## 11.8 小结

记忆系统是 Agent 实现长期智能的关键：

| 记忆类型 | 作用 | 存储方式 |
|----------|------|----------|
| **短期记忆** | 当前会话 | 内存列表 |
| **长期记忆** | 持久知识 | 向量数据库 |
| **工作记忆** | 任务状态 | 临时存储 |

**关键点：**
- 记忆让 Agent 有"连续性"
- 检索策略决定记忆质量
- 记忆管理防止系统过载

---

**下一章：** [Chapter 12: Agent 安全与对齐](chapter12-safety-alignment.md)

---

*最后更新：2026-03-11*
