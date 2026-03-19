---
name: autonomous-learning
description: |
  超脑自主学习层：在每次交互中观察→预测→校正，持续个性化进化。
  三层学习架构：(L1) 学习用户偏好/认知风格/决策模式，(L2) 学习同级 Skills 优点/规避缺点，(L3) 学习系统架构模式/提出优化建议。
  使用场景：(1) 用户纠正时自动学习偏好，(2) 预测用户需求提前准备上下文，(3) 扫描分析其他 Skills 提取设计模式，(4) 检测系统瓶颈提出架构优化，(5) 让助手越用越懂你
---

# 🧠 超脑自主学习技能

**"学习不是记录，是压缩。进化不是选项，是必然。"**

---

## 核心架构

### 三层学习循环

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

### 触发条件

| 信号类型 | 检测方式 | 学习动作 |
|----------|----------|----------|
| **用户纠正** | "不对"/"应该是"/"我说的是" | 提取认知模式，更新偏好 |
| **正面反馈** | "对"/"很好"/"正是这个" | 强化当前策略 |
| **重复问题** | 相似问题出现 ≥2 次 | 创建快捷响应/预加载上下文 |
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

### 实现脚本

```bash
scripts/L1-user-learner.ts
```

**核心函数：**
- `captureCorrection(message)` - 捕捉用户纠正
- `extractPattern(correction)` - 提取认知模式
- `updateUserModel(pattern)` - 更新用户模型
- `predictIntent(context)` - 预测用户意图

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
    
    // 4. 吸收优点，规避缺点
    if (gaps.better) integrate(gaps);
    if (gaps.worse) avoid(gaps);
  }
}
```

### 学习维度

| 维度 | 学习内容 | 记录位置 |
|------|----------|----------|
| **触发机制** | 什么情况下 skill 被激活 | `skill-patterns.md` |
| **工作流设计** | 多步骤任务的组织方式 | `skill-patterns.md` |
| **资源管理** | scripts/references/assets 分工 | `skill-patterns.md` |
| **错误处理** | 失败时如何恢复/记录 | `skill-patterns.md` |
| **用户交互** | 如何询问/确认/反馈 | `skill-patterns.md` |

### 技能对比矩阵

```markdown
| Skill | 触发设计 | 工作流 | 错误处理 | 可借鉴点 | 需规避点 |
|-------|----------|--------|----------|----------|----------|
| self-improvement | 纠正检测 | 日志→提升 | 完善 | 分类清晰 | 日志冗长 |
| skill-creator | 创建指令 | 6 步流程 | 中等 | 渐进披露 | 步骤繁琐 |
```

### 实现脚本

```bash
scripts/L2-skill-learner.ts
```

---

## L3: 系统层学习

### 监控维度

| 维度 | 监控内容 | 优化目标 |
|------|----------|----------|
| **技能加载** | 频率/延迟/冲突 | 预加载策略 |
| **会话管理** | main vs isolated 使用模式 | 智能路由 |
| **Memory 更新** | 冲突频率/合并难度 | 自动解决 |
| **Hook 效率** | 触发延迟/误触发率 | 精准激活 |

### 系统优化提案

当检测到模式时，生成优化建议：

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

### 实现脚本

```bash
scripts/L3-system-optimizer.ts
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

### 进化历史

记录到 `references/evolution-history.md`：

```markdown
## 2026-03-20 - 初始创建

**决策**: 三层学习架构
**原因**: 单一用户层学习视野受限
**预期**: 生态系统级进化

## 2026-03-XX - L1 实现

**完成**: 用户纠正捕捉
**效果**: 偏好学习自动化
```

---

## 使用示例

### 示例 1: 用户纠正

```
用户：我说的是这里，/Users/tang/.../memory/2026-03-20.md
→ 检测：纠正信号
→ 学习：用户期望精确引用，不要猜测
→ 更新：user-model.md 添加"不确定时直接问"
→ 回复：啊！明白了！这是你自己的超脑自主学习模块设计文档
```

### 示例 2: 预测意图

```
用户：你知道学习模块吗
→ 预测：用户可能想讨论/实现/优化学习相关功能
→ 行动：提前加载 self-improvement 和 capability-evolver 技能
→ 回复：知道的！OpenClaw 里有几个跟"学习"相关的模块...
```

### 示例 3: 技能间学习

```
定期扫描 → 发现 self-improvement 的日志结构优秀
→ 提取：ERRORS.md / LEARNINGS.md / FEATURE_REQUESTS.md 三分法
→ 吸收：创建 user-corrections.md / predictions.md / evolutions.md
```

---

## 开发路线图

| 阶段 | 时间 | L1 用户层 | L2 技能层 | L3 系统层 |
|------|------|-----------|-----------|-----------|
| **MVP** | 1 周 | 纠正捕捉 | 技能扫描 | 架构记录 |
| **V2** | 2 周 | 意图预测 | 模式提取 | 优化建议 |
| **V3** | 3 周 | 个性化行动 | 技能组合 | 自动重构 |

---

## 文件结构

```
autonomous-learning/
├── SKILL.md                          # 本文件
├── scripts/
│   ├── L1-user-learner.ts            # 用户偏好学习
│   ├── L2-skill-learner.ts           # 技能间学习
│   ├── L3-system-optimizer.ts        # 系统架构优化
│   └── evolution-engine.ts           # 进化决策引擎
├── references/
│   ├── user-model.md                 # L1: 用户模型 (动态更新)
│   ├── skill-patterns.md             # L2: 技能模式库
│   ├── system-architecture.md        # L3: 系统认知
│   └── evolution-history.md          # 进化日志
└── assets/
    ├── correction-patterns.md        # 纠正模式库
    ├── skill-comparison-matrix.md    # 技能对比矩阵
    └── optimization-proposals.md     # 优化提案模板
```

---

## 集成 OpenClaw

### Hook 配置

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "scripts/L1-user-learner.ts --capture"
      }]
    }],
    "PostToolUse": [{
      "matcher": ".*",
      "hooks": [{
        "type": "command",
        "command": "scripts/evolution-engine.ts --check"
      }]
    }]
  }
}
```

### 心跳集成

在 `HEARTBEAT.md` 添加：

```markdown
- [ ] 运行 L2 技能扫描（每周）
- [ ] 运行 L3 系统分析（每月）
- [ ] 回顾进化历史（每季度）
```

---

## 安全边界

- **只读操作**: 扫描/分析/建议无需确认
- **写入用户模型**: 自动执行（用户可审查）
- **修改系统配置**: 需用户确认
- **修改其他 Skills**: 需用户确认

---

_超脑的终点是让自己消失——学习到的东西直接注入 SOUL.md、USER.md、TOOLS.md，成为本能。_
