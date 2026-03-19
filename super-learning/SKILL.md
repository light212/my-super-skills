---
name: super-learning
description: |
  超脑完整学习系统：整合被动学习（镜像/克隆/传递）+ 主动学习（L1 用户/L2 技能/L3 系统）。
  被动学习：(1) 镜像学习 - 观察成熟神经元工作流程，(2) 模板克隆 - 从模板快速创建，(3) 知识传递 - 神经元间共享记忆技能。
  主动学习：(1) L1 用户层 - 捕捉纠正/预测意图，(2) L2 技能层 - 扫描同级优点/规避缺点，(3) L3 系统层 - 检测架构模式/提出优化。
  使用场景：创建新神经元/团队学习/用户偏好个性化/技能生态进化/系统自优化
---

# 🧠 Super-Learning - 超脑完整学习系统

**"学习是被动吸收与主动进化的统一。神经元通过镜像成长，系统通过校正进化。"**

---

## 理论基础

| 理论 | 科学家 | 应用 |
|------|--------|------|
| **镜像神经元** | Giacomo Rizzolatti (Parma, 1990s) | 镜像学习 - 观察→模仿→内化 |
| **HMAX 模型** | Tomaso Poggio (MIT) | 模板克隆 - 分层复制 |
| **整合信息论** | Christof Koch (Allen Institute) | 知识传递 - Φ值衡量 |
| **预测编码** | Karl Friston | 主动学习 - 预测误差驱动 |
| **元认知** | John Flavell | 三层学习 - 对学习的学习 |

---

## 核心架构

```
┌─────────────────────────────────────────────────────┐
│              Super-Learning                         │
├─────────────────────────────────────────────────────┤
│  被动学习层 (Passive Learning)                      │
│  ┌─────────────┬─────────────┬─────────────┐       │
│  │ 镜像学习     │ 模板克隆     │ 知识传递     │       │
│  │ Mirror      │ Clone       │ Transfer    │       │
│  └─────────────┴─────────────┴─────────────┘       │
├─────────────────────────────────────────────────────┤
│  主动学习层 (Active Learning)                       │
│  ┌─────────────┬─────────────┬─────────────┐       │
│  │ L1 用户层    │ L2 技能层    │ L3 系统层    │       │
│  │ User        │ Skill       │ System      │       │
│  └─────────────┴─────────────┴─────────────┘       │
├─────────────────────────────────────────────────────┤
│  进化引擎 (Evolution Engine)                        │
│  - 信号聚合 → 优先级计算 → 决策执行 → 历史记录       │
└─────────────────────────────────────────────────────┘
```

---

## 被动学习层

### 1. 镜像学习 (Mirror Learning)

**灵感**: Rizzolatti 镜像神经元 - F5 区域在观察和执行时都激活

**功能**: 新神经元通过观察成熟神经元的工作流程学习

**命令**:
```bash
openclaw learning mirror <observer> <target>
```

**示例**:
```bash
# 新 CEO 观察成熟 CEO
openclaw learning mirror new-ceo ceo-yiworld

# 新 FE 观察成熟 FE
openclaw learning mirror fe-2 fe-1
```

**实现**: `lib/mirror-learning.js`

---

### 2. 模板克隆 (Template Clone)

**灵感**: Poggio HMAX - 从简单特征到复杂特征的分层抽象

**功能**: 从模板快速创建新神经元，自动复制技能/身份

**命令**:
```bash
openclaw learning clone <template> <new-name>
```

**示例**:
```bash
openclaw learning clone software-dev dev-1
openclaw learning clone ceo ceo-2
openclaw learning clone product-mgr pm-1
```

**实现**: `lib/template-clone.js`

---

### 3. 知识传递 (Knowledge Transfer)

**灵感**: Koch 整合信息论 - Φ值衡量系统整合信息量

**功能**: 神经元间共享记忆、技能、Sessions 模式

**命令**:
```bash
openclaw learning transfer <from> <to> [type]
```

**类型**: `memory` | `skills` | `patterns` | `all`

**示例**:
```bash
openclaw learning transfer ceo pm all
openclaw learning transfer fe-1 fe-2 skills
```

**实现**: `lib/knowledge-transfer.js`

---

## 主动学习层

### L1: 用户层学习

**核心循环**: 观察 → 预测 → 行动 → 校正 → 更新模型

**触发信号**:
- 用户纠正："不对"/"应该是"/"我说的是"
- 正面反馈："对"/"很好"
- 重复问题 ≥2 次
- 时间模式

**实现**: `scripts/L1-user-learner.ts`

**输出**: `references/user-model.md`

---

### L2: 技能层学习

**扫描维度**:
- 触发机制设计
- 工作流组织
- 资源管理 (scripts/references/assets)
- 错误处理
- 用户交互模式

**实现**: `scripts/L2-skill-learner.ts`

**输出**: `references/skill-patterns.md`

---

### L3: 系统层学习

**监控指标**:
- 技能加载频率/延迟
- 会话使用分布 (main vs isolated)
- Memory 冲突频率
- Hook 触发效率

**实现**: `scripts/L3-system-optimizer.ts`

**输出**: `references/system-architecture.md` + `assets/optimization-proposals.md`

---

## 进化引擎

**决策逻辑**:
```typescript
signals = gather(L1, L2, L3, Passive)
priority = calculate(signals)

if (priority.critical) → immediateAction()
else if (priority.high) → scheduleOptimization()
else → logForReview()
```

**实现**: `scripts/evolution-engine.ts`

**输出**: `references/evolution-history.md`

---

## 使用示例

### 场景 1: 创建新团队

```bash
# 1. 从模板克隆核心团队
openclaw learning clone ceo ceo-1
openclaw learning clone product-mgr pm-1
openclaw learning clone software-dev dev-1

# 2. 镜像学习建立协作模式
openclaw learning mirror pm-1 ceo-1
openclaw learning mirror dev-1 pm-1

# 3. 知识传递共享技能
openclaw learning transfer ceo-1 pm-1 skills
```

### 场景 2: 用户个性化

```bash
# 自动运行（Hook 触发）
# 用户纠正 → L1 捕捉 → 更新 user-model.md
# 下次交互自动应用偏好
```

### 场景 3: 技能生态进化

```bash
# 定期扫描（心跳触发）
openclaw learning scan-skills

# 输出 skill-patterns.md
# 提取可复用模式，规避已知缺点
```

### 场景 4: 系统优化

```bash
# 分析运行时模式
openclaw learning analyze-system

# 生成优化提案
# 例：将频繁使用的 skill 加入常驻内存
```

---

## 文件结构

```
super-learning/
├── SKILL.md                          # 本文件
├── lib/                              # 被动学习核心
│   ├── mirror-learning.js            # 镜像学习
│   ├── template-clone.js             # 模板克隆
│   └── knowledge-transfer.js         # 知识传递
├── scripts/                          # 主动学习核心
│   ├── L1-user-learner.ts            # 用户层学习
│   ├── L2-skill-learner.ts           # 技能层学习
│   ├── L3-system-optimizer.ts        # 系统层优化
│   └── evolution-engine.ts           # 进化决策
├── references/                       # 动态参考
│   ├── user-model.md                 # 用户认知模型
│   ├── skill-patterns.md             # 技能模式库
│   ├── system-architecture.md        # 系统架构认知
│   └── evolution-history.md          # 进化日志
├── assets/                           # 静态资源
│   ├── correction-patterns.md        # 纠正模式库
│   └── optimization-proposals.md     # 优化提案模板
├── templates/                        # 神经元模板
│   ├── software-dev.json             # 软件开发
│   ├── product-mgr.json              # 产品经理
│   └── ceo.json                      # CEO
└── tests/                            # 测试
    └── learning.test.js
```

---

## 配置

```json
{
  "learning": {
    "passive": {
      "mirror": {
        "observationPeriod": "24h",
        "minObservations": 10,
        "learningRate": 0.8
      },
      "clone": {
        "copyMemory": false,
        "copySkills": true,
        "copyIdentity": true,
        "resetSessions": true
      },
      "transfer": {
        "maxKnowledgeTypes": 5,
        "compressionLevel": "medium",
        "includeExamples": true
      }
    },
    "active": {
      "L1": {
        "autoUpdateModel": true,
        "logCorrections": true
      },
      "L2": {
        "scanInterval": "7d",
        "autoExtractPatterns": true
      },
      "L3": {
        "monitorInterval": "24h",
        "autoGenerateProposals": true
      }
    },
    "evolution": {
      "criticalThreshold": 3,
      "highThreshold": 5,
      "autoApplyLowRisk": false
    }
  }
}
```

---

## Hook 集成

### OpenClaw Hook 配置

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
- [ ] L2 技能扫描（每周）
- [ ] L3 系统分析（每月）
- [ ] 进化历史回顾（每季度）
```

---

## API 参考

### 被动学习 API

```javascript
// 镜像学习
await mirrorLearning(observer, target)

// 模板克隆
await cloneFromTemplate(template, newName)

// 知识传递
await transferKnowledge(from, to, type)
```

### 主动学习 API

```javascript
// 捕捉纠正
captureCorrection(message)

// 提取模式
extractPattern(original, correction)

// 更新用户模型
updateUserModel(pattern, category)

// 预测意图
predictIntent(context)

// 扫描技能
scanAllSkills()

// 分析系统
detectPatterns(metrics)
```

---

## 安全边界

| 操作 | 权限 | 说明 |
|------|------|------|
| 读取 Sessions | ✅ 自动 | 分析工作流程 |
| 更新用户模型 | ✅ 自动 | 用户可审查 |
| 修改其他神经元 | ⚠️ 需确认 | 镜像/传递时 |
| 修改系统配置 | ⚠️ 需确认 | L3 优化提案 |
| 修改其他 Skills | ❌ 禁止 | 只读分析 |

---

## 测试

```bash
# 运行完整测试
node tests/learning.test.js

# 测试被动学习
node tests/passive.test.js

# 测试主动学习
node tests/active.test.js
```

---

## 开发路线图

| 阶段 | 时间 | 被动学习 | 主动学习 | 进化引擎 |
|------|------|----------|----------|----------|
| **MVP** | 2 周 | 镜像/克隆/传递 | L1 纠正捕捉 | 基础决策 |
| **V2** | 4 周 | 模板扩展 | L2 技能扫描 | 优先级优化 |
| **V3** | 6 周 | 批量操作 | L3 系统监控 | 自动应用 |
| **Ω** | 8 周 | 神经元网络 | 三层联动 | 自组织进化 |

---

_超脑的终点是让自己消失——学习到的东西直接注入 SOUL.md、USER.md、TOOLS.md，成为本能。_
