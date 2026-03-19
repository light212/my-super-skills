# 🧠 Autonomous-Learning 技能学习笔记

**学习日期**: 2026-03-20  
**来源**: `/Users/tangxuguang/project/git/billion-people-world/skills/my-super-skills/autonomous-learning/`

---

## 核心理念

> **"学习不是记录，是压缩。进化不是选项，是必然。"**

---

## 三层学习架构

```
┌────────────────────────────────────────────────────┐
│              L3: 系统层学习                         │
│         学习架构模式 → 优化自身设计                 │
├────────────────────────────────────────────────────┤
│              L2: 技能层学习                         │
│     学习同级 Skills → 吸收优点/规避缺点             │
├────────────────────────────────────────────────────┤
│              L1: 用户层学习                         │
│         学习用户偏好 → 个性化行为                   │
└────────────────────────────────────────────────────┘
```

---

## L1: 用户层学习

### 核心循环

```
观察 → 预测 → 行动 → 校正 → 更新模型
```

### 触发信号

| 信号类型 | 检测关键词 | 学习动作 |
|----------|-----------|----------|
| **用户纠正** | "不对"/"应该是"/"我说的是" | 提取认知模式，更新偏好 |
| **正面反馈** | "对"/"很好"/"正是这个" | 强化当前策略 |
| **重复问题** | 相似问题 ≥2 次 | 创建快捷响应 |
| **时间模式** | 固定时间做固定事 | 建立时间触发器 |

### 用户模型结构

记录到 `references/user-model.md`：

```markdown
## 认知风格
- 偏好：简洁直接，不要客套话
- 决策：快速迭代，先 MVP 再优化
- 沟通：喜欢表格/结构化输出

## 兴趣领域
- AI 架构/元认知/自主学习
- 系统设计与进化

## 禁忌
- 不要重复已知信息
- 不要猜测，不确定直接问
```

### 核心脚本

```typescript
// scripts/L1-user-learner.ts

// 捕捉用户纠正
captureCorrection(message)

// 提取认知模式
extractPattern(correction)

// 更新用户模型
updateUserModel(pattern)

// 预测用户意图
predictIntent(context)
```

---

## L2: 技能层学习

### 扫描分析流程

```typescript
async function learnFromSkills() {
  const skills = await listAllSkills();
  
  for (const skill of skills) {
    // 1. 分析设计模式
    const patterns = analyzeSkillDesign(skill);
    
    // 2. 提取可复用片段
    const reusable = extractPatterns(patterns);
    
    // 3. 对比自身能力
    const gaps = compareWithSelf(reusable);
    
    // 4. 吸收优点
    await absorbPatterns(gaps);
  }
}
```

### 学习目标

- 发现优秀设计模式
- 提取可复用代码片段
- 对比自身找出差距
- 吸收内化为自身能力

---

## L3: 系统层学习

### 监控维度

| 维度 | 监控内容 | 优化目标 |
|------|----------|----------|
| **技能加载** | 频率/延迟/冲突 | 预加载策略 |
| **会话管理** | main vs isolated 使用模式 | 智能路由 |
| **Memory 更新** | 冲突频率/合并难度 | 自动解决 |
| **Hook 效率** | 触发延迟/误触发率 | 精准激活 |

### 优化提案格式

```markdown
## 优化提案 #001

**检测到**: weather skill 每次加载耗时 200ms，用户每天查询 5+ 次

**建议**: 将 weather 加入常驻内存

**配置变更**:
```json
{ "skills.permanent": ["weather"] }
```

**预期收益**: 节省 1s/天 延迟
```

---

## 进化引擎

### 决策逻辑

```typescript
async function evolutionEngine() {
  const signals = {
    user: await gatherUserSignals(),
    skills: await gatherSkillSignals(),
    system: await gatherSystemSignals()
  };
  
  const priority = calculatePriority(signals);
  
  if (priority.critical) {
    await immediateAction(priority);
  } else if (priority.high) {
    await scheduleOptimization(priority);
  } else {
    await logForReview(priority);
  }
}
```

### 优先级分类

| 优先级 | 条件 | 行动 |
|--------|------|------|
| **Critical** | 系统崩溃/数据丢失 | 立即行动 |
| **High** | 性能瓶颈/频繁错误 | 计划优化 |
| **Medium** | 可改进的设计 | 记录待办 |
| **Low** | 锦上添花 | 忽略或回顾 |

---

## 文件结构

```
autonomous-learning/
├── SKILL.md                          # 技能定义
├── scripts/
│   ├── L1-user-learner.ts            # 用户偏好学习
│   ├── L2-skill-learner.ts           # 技能间学习
│   ├── L3-system-optimizer.ts        # 系统架构优化
│   └── evolution-engine.ts           # 进化决策引擎
├── references/
│   ├── user-model.md                 # L1: 用户模型
│   ├── skill-patterns.md             # L2: 技能模式库
│   ├── system-architecture.md        # L3: 系统认知
│   └── evolution-history.md          # 进化日志
└── assets/
    ├── correction-patterns.md        # 纠正模式库
    ├── skill-comparison-matrix.md    # 技能对比矩阵
    └── optimization-proposals.md     # 优化提案模板
```

---

## 与 passive-learning 集成

### 学习模块对比

| 特性 | passive-learning | autonomous-learning |
|------|------------------|---------------------|
| **触发方式** | 手动命令 | 自动触发 |
| **学习对象** | 其他神经元 | 用户/Skills/系统 |
| **学习速度** | 一次性 | 持续进化 |
| **核心功能** | 镜像/克隆/传递 | 观察/预测/校正 |

### 互补设计

```
passive-learning (显式学习)
├── 镜像学习 ← 观察成熟神经元
├── 模板克隆 ← 从模板创建
└── 知识传递 ← 神经元间共享

autonomous-learning (隐式学习)
├── L1 用户层 ← 学习用户偏好
├── L2 技能层 ← 学习其他技能
└── L3 系统层 ← 学习架构模式

= 完整学习系统
```

---

## 开发路线图

| 阶段 | 时间 | L1 用户层 | L2 技能层 | L3 系统层 |
|------|------|-----------|-----------|-----------|
| **MVP** | 1 周 | 纠正捕捉 | 技能扫描 | 架构记录 |
| **V2** | 2 周 | 意图预测 | 模式提取 | 优化建议 |
| **V3** | 3 周 | 个性化行动 | 技能组合 | 自动重构 |

---

## 安全边界

| 操作类型 | 权限 | 说明 |
|----------|------|------|
| **只读操作** | 自动执行 | 扫描/分析/建议 |
| **写入用户模型** | 自动执行 | 用户可审查 |
| **修改系统配置** | 需用户确认 | 影响系统行为 |
| **修改其他 Skills** | 需用户确认 | 影响其他技能 |

---

## 关键洞察

### 1. 学习是压缩

> 不是记录所有交互，而是提取模式

```
原始交互 → 模式提取 → 压缩存储 → 快速检索
```

### 2. 三层架构的必要性

- **L1**: 让助手懂你（个性化）
- **L2**: 让助手变强（吸收优点）
- **L3**: 让系统进化（优化设计）

### 3. 进化引擎是核心

> 决策逻辑决定了学习的方向和速度

```
信号收集 → 优先级计算 → 行动选择
```

### 4. 安全边界很重要

> 自动学习不能越界，用户必须有最终控制权

---

## 应用到亿人世界

### 1. 神经元学习增强

```typescript
// 在 passive-learning 中添加自主学习能力
async function autonomousLearn(agent) {
  // L1: 学习用户与这个神经元的交互模式
  const userPatterns = await learnUserPatterns(agent);
  
  // L2: 学习其他神经元的优点
  const skillPatterns = await learnFromOtherAgents(agent);
  
  // L3: 优化神经元自身架构
  const optimizations = await optimizeAgentDesign(agent);
  
  return { userPatterns, skillPatterns, optimizations };
}
```

### 2. 用户模型集成

```json
{
  "agents": {
    "ceo-yiworld": {
      "userModel": {
        "cognitiveStyle": "简洁直接",
        "decisionStyle": "快速迭代",
        "communicationPreference": "结构化输出"
      }
    }
  }
}
```

### 3. 进化历史追踪

```markdown
## 神经元进化历史

### 2026-03-20 - CEO 神经元创建
**模板**: ceo.json
**技能**: 无
**学习**: 从 ceo-yiworld 镜像学习

### 2026-03-XX - CEO 神经元进化
**学习**: 用户偏好简洁决策
**优化**: 减少冗长解释
**效果**: 响应速度提升 50%
```

---

**学习完成时间**: 2026-03-20 02:25  
**学习者**: 亿人世界 AI
