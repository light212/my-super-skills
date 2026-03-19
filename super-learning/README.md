# Super-Learning - 超脑完整学习系统

_整合被动学习（镜像/克隆/传递）+ 主动学习（L1 用户/L2 技能/L3 系统）_

---

## 快速开始

### 1. 安装

```bash
# 方法 1：复制技能到 OpenClaw 技能目录
cp -r super-learning ~/.openclaw/skills/

# 方法 2：创建软链接（推荐，方便开发）
ln -s /path/to/super-learning ~/.openclaw/skills/super-learning
```

### 2. 验证安装

```bash
ls -la ~/.openclaw/skills/super-learning/
```

---

## 被动学习功能

### 镜像学习

```bash
# 新神经元观察成熟神经元
openclaw learning mirror <observer> <target>

# 示例
openclaw learning mirror new-ceo ceo-yiworld
openclaw learning mirror fe-2 fe-1
```

### 模板克隆

```bash
# 从模板创建新神经元
openclaw learning clone <template> <new-name>

# 示例
openclaw learning clone software-dev dev-1
openclaw learning clone ceo ceo-2
openclaw learning clone product-mgr pm-1
```

### 知识传递

```bash
# 神经元间共享知识
openclaw learning transfer <from> <to> [type]

# 类型：memory | skills | patterns | all
openclaw learning transfer ceo pm all
openclaw learning transfer fe-1 fe-2 skills
```

---

## 主动学习功能

### L1: 用户层学习

自动运行（Hook 触发），捕捉用户纠正并更新偏好。

**查看用户模型**:
```bash
cat ~/.openclaw/workspaces/yirenverse/my-super-skills/super-learning/references/user-model.md
```

### L2: 技能层学习

```bash
# 扫描所有技能
node scripts/L2-skill-learner.ts --scan

# 分析特定技能
node scripts/L2-skill-learner.ts --analyze skill-name
```

### L3: 系统层学习

```bash
# 收集系统指标
node scripts/L3-system-optimizer.ts --collect

# 分析系统模式
node scripts/L3-system-optimizer.ts --analyze
```

### 进化引擎

```bash
# 运行进化循环
node scripts/evolution-engine.ts --run

# 检查进化信号
node scripts/evolution-engine.ts --check
```

---

## 使用场景

### 场景 1: 创建新团队

```bash
# 1. 克隆核心团队
openclaw learning clone ceo ceo-1
openclaw learning clone product-mgr pm-1
openclaw learning clone software-dev dev-1

# 2. 镜像学习
openclaw learning mirror pm-1 ceo-1
openclaw learning mirror dev-1 pm-1

# 3. 知识传递
openclaw learning transfer ceo-1 pm-1 skills
```

### 场景 2: 用户个性化

无需手动命令，Hook 自动捕捉纠正并更新 `user-model.md`。

### 场景 3: 技能生态进化

```bash
# 每周扫描
node scripts/L2-skill-learner.ts --scan

# 查看提取的模式
cat references/skill-patterns.md
```

### 场景 4: 系统优化

```bash
# 分析运行时
node scripts/L3-system-optimizer.ts --analyze

# 查看优化提案
cat assets/optimization-proposals.md
```

---

## 文件结构

```
super-learning/
├── SKILL.md                          # 核心协议
├── README.md                         # 本文件
├── lib/                              # 被动学习核心
│   ├── mirror-learning.js
│   ├── template-clone.js
│   └── knowledge-transfer.js
├── scripts/                          # 主动学习核心
│   ├── L1-user-learner.ts
│   ├── L2-skill-learner.ts
│   ├── L3-system-optimizer.ts
│   └── evolution-engine.ts
├── references/                       # 动态参考
│   ├── user-model.md
│   ├── skill-patterns.md
│   ├── system-architecture.md
│   └── evolution-history.md
├── assets/                           # 静态资源
│   ├── correction-patterns.md
│   └── optimization-proposals.md
├── templates/                        # 神经元模板
│   ├── software-dev.json
│   ├── product-mgr.json
│   └── ceo.json
└── tests/                            # 测试
    └── learning.test.js
```

---

## 配置

编辑 `~/.openclaw/config.json` 添加：

```json
{
  "learning": {
    "passive": {
      "mirror": { "observationPeriod": "24h", "learningRate": 0.8 },
      "clone": { "copySkills": true, "copyIdentity": true },
      "transfer": { "compressionLevel": "medium" }
    },
    "active": {
      "L1": { "autoUpdateModel": true },
      "L2": { "scanInterval": "7d" },
      "L3": { "monitorInterval": "24h" }
    }
  }
}
```

---

## Hook 集成

在 `~/.openclaw/hooks.json` 添加：

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "scripts/L1-user-learner.ts --capture"
      }]
    }]
  }
}
```

---

## 测试

```bash
cd super-learning

# 运行完整测试
node tests/learning.test.js

# 测试被动学习
node tests/passive.test.js

# 测试主动学习
node tests/active.test.js
```

---

## 故障排除

### 命令找不到

```bash
# 检查技能安装
ls -la ~/.openclaw/skills/super-learning/

# 检查 OpenClaw 是否加载
openclaw skills list
```

### 镜像学习失败

```bash
# 检查目标神经元
ls -la ~/.openclaw/agents/<target>/

# 确保有 Sessions
ls -la ~/.openclaw/agents/<target>/sessions/
```

### 模板克隆失败

```bash
# 查看可用模板
ls templates/
```

---

## 理论背景

### 镜像神经元 (Rizzolatti, 1990s)

F5 区域在观察和执行时都激活 - 模仿学习的神经基础。

### HMAX 模型 (Poggio, MIT)

分层视觉处理 - 从简单特征到复杂特征的抽象。

### 整合信息论 (Koch, Allen Institute)

Φ值衡量系统整合信息量 - 意识的量化理论。

### 预测编码 (Friston)

预测误差驱动学习 - 主动推理的核心机制。

### 元认知 (Flavell)

对学习的学习 - 三层学习架构的基础。

---

## 许可证

MIT License - 亿人世界
