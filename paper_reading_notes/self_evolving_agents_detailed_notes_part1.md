# 📚 自进化智能体综述 - 详细阅读笔记

## 论文基本信息

| 项目 | 内容 |
|------|------|
| **论文标题** | A Survey of Self-Evolving Agents: What, When, How, and Where to Evolve on the Path to Artificial Super Intelligence |
| **中文标题** | 自进化智能体综述：通往人工超级智能之路的进化维度 |
| **作者** | Huan-ang Gao, Jiayi Geng, Wenyue Hua, Mengkang Hu, Xinzhe Juan 等 27 位作者 |
| **单位** | 普林斯顿大学、清华大学、卡内基梅隆大学、上海交通大学等 |
| **arXiv 编号** | arXiv:2507.21046v4 |
| **提交日期** | 2025 年 7 月 28 日 (v1), 2026 年 1 月 16 日 (v4 最新版本) |
| **页数** | 77 页 |
| **图表** | 9 幅图 |
| **研究领域** | cs.AI (人工智能) |
| **发表状态** | Transactions on Machine Learning Research (01/2026) |
| **GitHub 仓库** | https://github.com/CharlesQ9/Self-Evolving-Agents |

---

# 第 1 章 引言 (Introduction)

## 1.1 研究背景与动机

### 核心问题

**LLM 的根本局限性**：
> "Large Language Models (LLMs) have demonstrated remarkable capabilities across a wide range of tasks. Yet, they remain fundamentally static, unable to adapt their internal parameters when encountering novel tasks, evolving knowledge domains, or dynamic interaction contexts."

**翻译**：大型语言模型（LLM）在广泛任务上展现出卓越能力，但它们本质上是**静态的**，无法在遇到新任务、演进的知识域或动态交互上下文时适应其内部参数。

**关键瓶颈**：
- 当 LLM 被部署到开放式、交互式环境时，这种静态性成为关键瓶颈
- 传统的知识检索机制不足以应对
- 需要能够**动态适应感知、推理和行动**的智能体

### 范式转变

> "This emerging need for dynamic, continual adaptation signals a conceptual shift in artificial intelligence: from scaling up static models to developing self-evolving agents."

**翻译**：这种对动态、持续适应的新兴需求标志着人工智能的概念转变：**从扩展静态模型转向开发自进化智能体**。

### 终极愿景：人工超级智能 (ASI)

> "This shift is currently driving us toward a promising and transformative path to Artificial Super Intelligence (ASI), where the agents not only can learn and evolve from experience with an unpredictable speed but also perform at or above human-level intelligence across a wide array of tasks."

**翻译**：这一转变正驱动我们走向通往**人工超级智能 (ASI)** 的有前景和变革性的路径，其中智能体不仅能以不可预测的速度从经验中学习和进化，还能在广泛任务上达到或超越人类水平的智能。

## 1.2 自进化智能体的定义

### 核心定义

> "Unlike traditional pipelines where human engineers curate data and schedule updates, a self-evolving agent is capable of continuously learning from new data, interactions, and experiences in real-time, leading to systems that are more robust, versatile, and capable of tackling complex, dynamic real-world problems."

**翻译**：与传统人类工程师策划数据和安排更新的管道不同，**自进化智能体**能够实时地从新数据、交互和经验中持续学习，从而产生更稳健、更多功能、能够解决复杂动态现实世界问题的系统。

### 自主性的定位

自进化的定义**不仅由使用的算法决定，更由自主性的位置决定**：
- 传统方法：人类策划数据 + 安排更新
- 自进化：智能体自主从交互中学习

## 1.3 现有研究的不足

### 现有综述的局限性

1. **Luo et al. (2025a)**：讨论了几种进化方式（如自学习、多智能体协同进化），但仅作为综合智能体分类中的附属组件

2. **Liu et al. (2025a)**：明确介绍了智能体不同组件的进化（如工具、提示），但覆盖范围有限

3. **Tao et al. (2024)**：专注于语言模型本身的进化，而非更广泛的智能体概念

### 核心研究缺口

> "Therefore, there is no systematic survey devoted to a dedicated, comprehensive investigation of self-evolving agents as a first-class research paradigm."

**翻译**：因此，没有系统性综述致力于将自进化智能体作为**一流研究范式**进行专门、全面的调查。

### 未探索的基本问题

1. **What**: 智能体的哪些方面应该进化？
2. **When**: 适应应该在何时发生？
3. **How**: 在实践中如何实现这种进化？

## 1.4 本文贡献

### 四大核心贡献

1. **统一理论框架**
   > "We establish a unified theoretical framework for characterizing self-evolutionary processes in agent systems, anchored around three fundamental dimensions: what evolves, how it evolves, and when it evolves, providing clear design guidance for future self-evolving agentic systems."
   
   **翻译**：建立统一理论框架，围绕三个基本维度（进化什么、如何进化、何时进化）刻画智能体系统中的自进化过程，为末来自进化智能体系统提供清晰的设计指导。

2. **评估体系研究**
   > "We further investigate the evaluation benchmark or environment tailored for self-evolving agents, highlighting emerging metrics and challenges related to adaptability, robustness, and real-world complexity."
   
   **翻译**：进一步研究针对自进化智能体的评估基准或环境，强调与适应性、稳健性和现实世界复杂性相关的新兴指标和挑战。

3. **实际应用展示**
   > "We showcase several key real-world applications across various domains, including autonomous software engineering, personalized education, healthcare, and intelligent virtual assistance, illustrating the practical potential of self-evolving agents."
   
   **翻译**：展示跨多个领域的关键实际应用，包括自主软件工程、个性化教育、医疗保健和智能虚拟助手，说明自进化智能体的实际潜力。

4. **挑战与方向识别**
   > "We identify critical open challenges and promising future research directions, emphasizing aspects like safety, personalization, multi-agent co-evolution, and scalability."
   
   **翻译**：识别关键的开放性挑战和前景广阔的未来研究方向，强调安全性、个性化、多智能体协同进化和可扩展性等方面。

## 1.5 论文组织结构

### 章节安排

| 章节 | 主题 | 核心问题 |
|------|------|----------|
| **第 2 章** | 定义与基础 | 形式化定义、与其他范式关系 |
| **第 3 章** | What to Evolve | 进化什么（模型、记忆、工具、架构） |
| **第 4 章** | When to Evolve | 何时进化（测试时内/测试时际） |
| **第 5 章** | How to Evolve | 如何进化（奖励基、模仿、群体） |
| **第 6 章** | Where to Evolve | 在哪里进化（通用/专业领域） |
| **第 7 章** | Evaluation | 评估指标、基准、范式 |
| **第 8 章** | Future Directions | 未来方向、开放挑战 |
| **第 9 章** | Conclusion | 结论 |

### 分类体系图 (Figure 2)

论文提出了自进化智能体的四维分类体系：
- **What**: 模型、上下文、工具、架构
- **When**: 测试时内进化、测试时际进化
- **How**: 奖励基、模仿与示范、群体与进化方法
- **Where**: 通用领域、专业领域（编码、GUI、金融、医疗、教育）

---

# 第 2 章 定义与基础 (Definitions and Foundations)

## 2.1 形式化定义

### 2.1.1 环境 (Environment)

**定义**：智能体系统的环境（包括用户和执行环境，如 Linux shell）定义为**部分可观测马尔可夫决策过程 (POMDP)**，表示为元组：

$$E = (\mathcal{G}, \mathcal{S}, \mathcal{A}, T, R, \Omega, O, \gamma)$$

**各组件详解**：

| 符号 | 名称 | 定义 | 示例 |
|------|------|------|------|
| $\mathcal{G}$ | 目标集合 | 潜在目标的集合 | 用户查询 |
| $g \in \mathcal{G}$ | 目标 | 智能体需要实现的任务目标 | "写一个 Python 脚本" |
| $\mathcal{S}$ | 状态集合 | 环境内部状态的集合 | 文件系统状态、内存状态 |
| $s \in \mathcal{S}$ | 状态 | 环境的特定内部状态 | 当前打开的文件列表 |
| $\mathcal{A}$ | 动作集合 | 动作的集合 | 文本推理、检索、工具调用 |
| $a \in \mathcal{A}$ | 动作 | 特定动作 | "执行代码"、"搜索文档" |
| $T$ | 状态转移函数 | $T(s'|s,a)$ 输出下一状态的概率分布 | 执行动作后的环境变化 |
| $R$ | 奖励函数 | $R: \mathcal{S} \times \mathcal{A} \times \mathcal{G} \rightarrow \mathcal{R}$ | 任务完成度评分 |
| $r = R(s,a,g)$ | 反馈/奖励 | 通常为标量分数或文本反馈 | "代码运行成功"、得分 0.8 |
| $\Omega$ | 观测集合 | 智能体可访问的观测集合 | 屏幕内容、终端输出 |
| $O$ | 观测函数 | $O(o'|s,a)$ 输出下一观测的概率分布 | 执行动作后看到的内容 |
| $\gamma$ | 折扣因子 | 未来奖励的折扣系数 | 通常 0.9-0.99 |

### 2.1.2 智能体系统 (Agent System)

**定义**：(多) 智能体系统定义为：

$$\Pi = (\Gamma, \{\psi_i\}, \{C_i\}, \{\mathcal{W}_i\})$$

**各组件详解**：

| 组件 | 符号 | 详细描述 | 示例 |
|------|------|----------|------|
| **架构** | $\Gamma$ | 决定智能体系统的控制流或多智能体间的协作结构 | 图结构、代码结构组织的节点序列 $(N_1, N_2, ...)$ |
| **LLM/MLLM** | $\psi_i$ | 底层语言模型/多模态语言模型 | GPT-4、Claude、Llama |
| **上下文** | $C_i$ | 上下文信息，包括提示 $P_i$ 和记忆 $M_i$ | 系统提示、对话历史、知识库 |
| **工具集** | $\mathcal{W}_i$ | 可用工具/API 的集合 | 代码解释器、搜索引擎、数据库 |

**节点定义**：每个节点 $N_i$ 包含：
- $\psi_i$: 底层 LLM/MLLM
- $C_i$: 上下文信息（提示 $P_i$ + 记忆 $M_i$）
- $\mathcal{W}_i$: 可用工具/API 集合

**智能体策略**：在每个节点，智能体策略是函数：

$$\pi_{\theta_i}(\cdot|o)$$

- 输入：观测 $o$
- 输出：下一动作的概率分布
- 参数：$\theta_i = (\psi_i, C_i)$
- 动作空间：自然语言空间 ∪ 工具空间 $\mathcal{W}_i$

**任务执行轨迹**：对于给定任务 $\mathcal{T} = (E, g)$（由环境 $E$ 和对应目标 $g \in \mathcal{G}$ 表示），智能体系统遵循拓扑 $\Gamma$ 生成轨迹：

$$\tau = (o_0, a_0, o_1, a_1, ...)$$

并接收反馈 $r$（来自外部环境或内部信号，如自信度或评估者反馈）。

### 2.1.3 自进化策略 (Self-evolving Strategy)

**定义**：自进化策略是转换函数 $f$，基于生成的轨迹 $\tau$ 和外部/内部反馈 $r$，将当前智能体系统映射到新状态：

$$f(\Pi, \tau, r) = \Pi' = (\Gamma', \{\psi'_i\}, \{C'_i\}, \{\mathcal{W}'_i\}) \quad (公式 1)$$

**关键要点**：
- 输入：当前智能体 $\Pi$ + 轨迹 $\tau$ + 反馈 $r$
- 输出：进化后的智能体 $\Pi'$
- 可进化组件：架构 $\Gamma$、模型 $\psi$、上下文 $C$、工具集 $\mathcal{W}$

### 2.1.4 自进化智能体的目标 (Objective)

**效用函数**：设 $U$ 为效用函数，通过分配标量分数 $U(\Pi, \mathcal{T}) \in \mathbb{R}$ 来衡量智能体系统 $\Pi$ 在给定任务 $\mathcal{T}$ 上的性能。

**效用来源**：
- 任务特定反馈 $r$（如奖励信号或文本评估）
- 其他性能指标（如完成时间、准确性、稳健性）

**进化序列**：给定任务序列 $(\mathcal{T}_0, \mathcal{T}_1, ..., \mathcal{T}_n)$ 和初始智能体系统 $\Pi_0$，自进化策略 $f$ 递归生成进化的智能体系统序列 $(\Pi_1, \Pi_2, ..., \Pi_n)$：

$$\Pi_{j+1} = f(\Pi_j, \tau_j, r_j) \quad (公式 2)$$

其中 $\tau_j$ 和 $r_j$ 是任务 $\mathcal{T}_j$ 上的轨迹和反馈。

**总体目标**：设计自进化智能体的总体目标是构建策略 $f$，使得跨任务的累积效用最大化：

$$\max_f \sum_{j=0}^{n} U(\Pi_j, \mathcal{T}_j) \quad (公式 3)$$

### 2.1.5 操作性定义 (Operational Definition)

**正式定义**：
> "A self-evolving agent is the agent that modifies its internal parameters, contextual state, toolset, or architectural topology based on its own trajectories or feedback signals, with the explicit objective of improving future performance."

**翻译**：**自进化智能体**是基于自身轨迹或反馈信号修改其内部参数、上下文状态、工具集或架构拓扑的智能体，其明确目标是提高未来性能。

### 三个纳入标准

| 标准 | 要求 | 排除情况 |
|------|------|----------|
| **(i) 经验依赖** | 更新必须由轨迹、自生成数据或环境反馈驱动，针对智能体的策略局限性或能力边界 | 通用数据合成 |
| **(ii) 持久效应** | 产生持久的策略改变效果 | 瞬态指令跟随行为 |
| **(iii) 自主探索** | 具有自主探索或自发起学习的机制 | 完全被动学习 |

### 自主性光谱

```
原型进化 ←————————————→ 强自进化
(迭代引导)                (完全自主诊断和重构)
```

**说明**：
- **被动学习**：完全由外部提供的数据或时间表触发
- **主动学习**：自发起的探索、反思或结构修改（如使用自我反思收集数据）
- **排除**：静态管道（如标准蒸馏），其中数据生成与智能体的交互历史无关

**现实定位**：
> "As this field is rapidly forming, fully autonomous self-evolution without human intervention represents an aspirational goal rather than the current norm."

**翻译**：由于这个领域正在快速形成，**完全自主的无需人类干预的自进化**代表一个理想目标而非当前规范。

**本综述的包容性**：
- 不设定严格的排除阈值而忽视早期阶段发展
- 分析从**原型进化**（如迭代引导或反馈驱动提示）到**强自进化**（完全自主诊断和重构）的各种机制
- 提供全面视角，展示不同方法如何促进范式向完全自主的进展

## 2.2 与其他研究工作的关系

### 2.2.1 课程学习 (Curriculum Learning)

**定义**：
> "Curriculum learning is a training strategy in which data are presented in order of increasing difficulty."

**翻译**：课程学习是一种训练策略，其中数据按**难度递增**的顺序呈现。

**核心组件**：
1. **难度测量器**：量化每个训练数据点的难度级别
2. **训练调度器**：根据难度级别重新组织模型接收的数据点顺序

**应用领域**：
- 计算机视觉 (Guo et al., 2018; Jiang et al., 2014; Liu et al., 2023a)
- 自然语言处理 (Platanios et al., 2019; Tay et al., 2019)
- 语音识别 (Braun et al., 2017; Lotfian and Busso, 2019)
- LLM 后训练阶段微调 (Wang et al., 2025o; Zhang et al., 2025o; Parashar et al., 2025)

**与自进化智能体的区别**：

| 维度 | 课程学习 | 自进化智能体 |
|------|----------|--------------|
| **数据集** | 静态数据集 | 动态环境中的序列任务 |
| **进化对象** | 仅模型参数 | 模型参数 + 非参数组件（记忆、工具） |
| **学习主动性** | 被动接受数据顺序 | 主动探索环境 |

### 2.2.2 终身学习 (Lifelong Learning)

**定义**：
> "Lifelong learning refers to the ability of AI models to continuously and adaptively learn when exposed to new tasks and environments, while retaining previously acquired knowledge and abilities."

**翻译**：终身学习指 AI 模型在暴露于新任务和环境时**持续自适应学习**的能力，同时保留先前获得的知识和能力。

**别名**：持续学习 (continual learning)、增量学习 (incremental learning)

**核心目标**：在暴露于新数据或任务时，实现**保留现有知识**（稳定性）和**获取新知识**（可塑性）之间的平衡。

**关键挑战**：灾难性遗忘 (Catastrophic Forgetting)
- McCloskey and Cohen, 1989
- Ratcliff, 1990
- Rolnick et al., 2019

**与自进化智能体的两个根本区别**：

#### 区别 1：记忆功能和使用时机

| 方面 | 终身学习 | 自进化智能体 |
|------|----------|--------------|
| **记忆机制** | 经验重放缓冲、情景记忆 | 运行时上下文（提示、工作记忆、对话历史） |
| **功能角色** | 训练时工具，用于通过梯度计算优化参数 | 测试时状态，直接影响动作生成而无需参数更新 |
| **本质区别** | 训练时重放 (training-time replay) | 测试时状态适应 (test-time state adaptation) |

#### 区别 2：学习主动性

| 方面 | 终身学习 | 自进化智能体 |
|------|----------|--------------|
| **知识获取** | 主要通过外部提供的任务序列**被动**获取 | **主动**探索环境 + 结合内部反思/自我评估机制 |
| **学习轨迹** | 由外部定义 | 由智能体自主引导 |

**相关工作的定位**：
- 自改进 LLM 方法 (Huang et al., 2022; Yuan et al., 2024c)：通过自生成数据和自我批评迭代优化模型，可视为专注于**以模型为中心改进**的终身学习实例
- 自进化智能体：超越此范式，涵盖**系统级进化**，包括工具获取、架构重构和环境探索

### 2.2.3 模型编辑与遗忘 (Model Editing and Unlearning)

#### 模型编辑 (Model Editing)

**定义**：
> "Model editing and unlearning aim to efficiently and precisely modify specific knowledge in AI models while preserving irrelevant knowledge and avoiding full retraining."

**翻译**：模型编辑和遗忘旨在**高效精确地修改**AI 模型中的特定知识，同时保留无关知识并避免完全重新训练。

**典型应用**：执行高效精确的局部事实更新
- 示例：将"2021 年奥运会主办城市"的答案从"东京"修改为"巴黎"

**发展历程**：
- 早期方法：专注于原子知识三元组
- 后期扩展：各种可信相关任务 (Fang et al., 2025a; Huang et al., 2025a)
- 最新研究：终身模型编辑 (Chen et al., 2024c)，顺序执行模型编辑

#### 模型遗忘 (Model Unlearning)

**早期重点**：移除隐私相关信息 (Chen et al., 2021)

**LLM 时代应用**：增强 LLM 安全性
- 移除有害知识
- 消除偏见
- 符合法规要求

**与终身学习的比较**：

| 方面 | 终身学习 | 模型编辑 |
|------|----------|----------|
| **共同目标** | 获取新知识/能力，同时减轻灾难性遗忘 | 同左 |
| **实现方式** | 依赖广泛的基于梯度的全参数微调 | 通常以靶向方式仅修改小部分参数 |

**与自进化智能体的比较**：

| 方面 | 模型编辑 | 自进化智能体 |
|------|----------|--------------|
| **可修改组件** | 仅模型参数 | 模型参数 + 非参数组件（记忆、工具） |
| **执行流程** | 依赖算法设计师预定义的管道 | 可基于环境观察或内部反馈信号自发采用更多样灵活的策略 |

### 2.2.4 自进化智能体的定位 (Positioning)

论文通过**两个互补视角**澄清这些范式之间的关系：

#### 视角 1：问题设定视角 (Problem-setting View)

**课程学习和终身学习**源于具体的学习问题：

| 范式 | 解决的问题 | 核心关注点 |
|------|------------|------------|
| **课程学习** | 如何构建不同难度的训练样本，使模型更有效处理复杂样本 | 经验如何为学习者组织 |
| **终身学习** | 如何随时间获取新能力，同时减轻灾难性遗忘 | 经验如何为学习者组织 |

**共同特点**：
- 由要解决的问题驱动
- 主要规定**经验如何为学习者组织**
- 而非智能体本身如何在参数更新之外适应

#### 视角 2：解决方案范式视角 (Solution-paradigm View)

**模型编辑和自进化智能体**作为解决方案出现：

| 范式 | 提出的机制 | 核心特点 |
|------|------------|----------|
| **模型编辑** | 提供更新或修改系统的程序 | 靶向程序（通常是局部参数调整）来纠正或插入知识 |
| **自进化智能体** | 将适应作为一级能力 | 不仅参数更新，还包括运行时上下文、记忆、工具和工作流结构的变化 |

**双视角框架总结**：

```
问题设定视角                    解决方案范式视角
     ↓                               ↓
课程学习 ←————————————→ 模型编辑
     ↓                               ↓
终身学习 ←————————————→ 自进化智能体
```

**自进化智能体的系统级定位**：
> "Self-evolving agents thus represent a system-level solution paradigm: they include parameter-level editing as one update pathway while enabling broader, persistent, and interaction-driven evolution across multiple components of an agent."

**翻译**：因此，自进化智能体代表**系统级解决方案范式**：它们将参数级编辑作为一种更新路径，同时实现跨智能体多个组件的更广泛、持久和交互驱动的进化。

### 2.2.5 范式对比总结表 (Table 1)

| 范式 | 运行时上下文 | 工具集进化 | 动态任务 | 测试时适应 | 主动探索 | 结构变化 | 自我反思与评估 |
|------|-------------|-----------|---------|-----------|---------|---------|---------------|
| **课程学习** | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **终身学习** | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ |
| **模型编辑** | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |
| **自进化智能体** | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

**关键洞察**：自进化智能体是**唯一涵盖所有七个维度**的范式，代表最全面的适应和进化框架。

---

# 第 3 章 进化什么？(What to Evolve?)

## 3.1 核心问题

> "A self-evolving agent differs from a static agent not by what components it contains, but by which internal states can be autonomously modified based on its own trajectories, reflections, and feedback signals."

**翻译**：自进化智能体与静态智能体的区别**不在于包含哪些组件**，而在于**哪些内部状态可以基于自身轨迹、反思和反馈信号自主修改**。

**本节关键问题**：识别智能体系统 $\Pi = (\Gamma, \{\psi_i\}, \{C_i\}, \{\mathcal{W}_i\})$ 内的**进化位点 **(evolutionary loci)——系统的哪些部分的状态可以以经验驱动和持久的方式重写，实现累积自我改进。

## 3.2 四大进化支柱

根据 2.1 节的公式化，这些进化位点与智能体系统的**四大支柱**对齐：

```
智能体系统 Π = (Γ, {ψ_i}, {C_i}, {W_i})
                  ↓      ↓      ↓      ↓
              架构    模型   上下文   工具
```

### 进化路径概览

1. **模型 {ψ_i}**：智能体的认知核心
   - 参数可通过自生成监督、执行轨迹或环境反馈持续更新
   - 代表作品：Zhou et al. (2025e), Wang et al. (2025p)

2. **上下文 {C_i}**：包括指令和长期记忆
   - 随着智能体反思、存储和检索经验而进化
   - 塑造未来决策
   - 代表作品：Xiang et al. (2025), Khattab et al. (2023), Chhikara et al. (2025)

3. **工具 {W_i}**：可执行技能
   - 自主创建 (Qiu et al., 2025b)
   - 迭代精炼 (Qu et al., 2025)
   - 可扩展管理 (Wang et al., 2025j)
   - 基于可验证的交互信号

4. **架构 Γ**：系统架构和协作结构
   - 架构优化 (Hu et al., 2024c; Zhang et al., 2024c)
   - 协作结构优化 (Wan et al., 2025)
   - 实现超越单个组件的结构适应

## 3.3 进化位点总结表 (Table 2)

论文在 Table 2 中展示了代表性自进化智能体方法在四大进化支柱上的定位，使用实心圆点 (•) 标记方法积极进化的维度。

（完整表格见后续详细方法分析部分）

---

*注：由于内容长度限制，这是详细笔记的前半部分。后续章节（第 3-9 章）的详细翻译和整理将在下一个文档中继续。*

**已覆盖内容**：
- ✅ 完整引言（研究背景、动机、贡献、组织结构）
- ✅ 完整定义与基础（形式化定义、与其他范式关系）
- ✅ 第 3 章开篇（进化什么的核心问题和四大支柱）

**待继续内容**：
- 第 3 章详细方法分析（模型、上下文、工具、架构进化）
- 第 4 章 何时进化（测试时内/测试时际）
- 第 5 章 如何进化（奖励基、模仿、群体方法）
- 第 6 章 在哪里进化（通用/专业领域）
- 第 7 章 评估（目标、指标、基准、范式）
- 第 8 章 未来方向
- 第 9 章 结论
