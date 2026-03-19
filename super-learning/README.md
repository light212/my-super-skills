# Super-Learning - 超脑完整学习系统

_整合被动学习（镜像/克隆/传递）+ 主动学习（L1 用户/L2 技能/L3 系统）_

---

## 🚀 快速开始

### 1. 安装

```bash
# 方法 1：复制技能到 OpenClaw 技能目录
cp -r super-learning ~/.openclaw/skills/

# 方法 2：创建软链接（推荐，方便开发）
ln -s /Users/tang/.openclaw/workspaces/yirenverse/my-super-skills/super-learning ~/.openclaw/skills/super-learning
```

### 2. 验证安装

```bash
ls -la ~/.openclaw/skills/super-learning/
```

### 3. 启用自动触发 🤖

```bash
# 初始化自动触发器
node ~/.openclaw/skills/super-learning/lib/auto-trigger.js --init

# 测试自动触发
node ~/.openclaw/skills/super-learning/lib/auto-trigger.js --test

# 查看配置
node ~/.openclaw/skills/super-learning/lib/auto-trigger.js --config
```

### 4. 配置自动学习

编辑 `~/.openclaw/skills/super-learning/config/auto-learning.json`：

```json
{
  "autoClone": { "enabled": true },
  "autoMirror": { "enabled": true },
  "autoTransfer": { "enabled": true }
}
```

---

## 🤖 被动学习（自动触发）

**无需手动命令！** 系统自动检测事件并触发学习。

### 自动触发场景

| 事件 | 自动动作 | 配置 |
|------|----------|------|
| **创建新 Agent** | 从模板克隆 | `autoClone` |
| **Agent 启动** | 安排镜像学习 | `autoMirror` |
| **检测到协作** | 知识传递 | `autoTransfer` |

### 示例

```
用户："创建一个新 CEO"
→ 自动：克隆 ceo 模板 + 安排镜像 ceo-1 + 传递必要知识

用户："新 FE 加入团队"
→ 自动：克隆 developer 模板 + 镜像学习 fe-1
```

### 配置规则

```json
{
  "autoClone": {
    "templates": {
      "ceo": "ceo",
      "pm": "product-mgr",
      "dev": "software-dev"
    }
  },
  "autoMirror": {
    "pairs": [
      { "observer": "new-*", "target": "*-1" },
      { "observer": "*-2", "target": "*-1" }
    ]
  },
  "autoTransfer": {
    "rules": [
      { "from": "ceo-*", "to": "pm-*", "type": "skills" }
    ]
  }
}
```

---

## 📖 手动命令（可选）

### 镜像学习

```bash
openclaw learning mirror <observer> <target>

# 示例
openclaw learning mirror new-ceo ceo-yiworld
openclaw learning mirror fe-2 fe-1
```

### 模板克隆

```bash
openclaw learning clone <template> <new-name>

# 示例
openclaw learning clone software-dev dev-1
openclaw learning clone ceo ceo-2
```

### 知识传递

```bash
openclaw learning transfer <from> <to> [type]

# 类型：memory | skills | patterns | all
openclaw learning transfer ceo pm all
openclaw learning transfer fe-1 fe-2 skills
```

---

## 🧠 主动学习

### L1: 用户层学习

自动运行（Hook 触发），捕捉用户纠正并更新偏好。

### L2: 技能层学习

```bash
node scripts/L2-skill-learner.ts --scan
```

### L3: 系统层学习

```bash
node scripts/L3-system-optimizer.ts --analyze
```

### 进化引擎

```bash
node scripts/evolution-engine.ts --run
```

---

## 📁 文件结构

```
super-learning/
├── SKILL.md                          # 核心协议
├── README.md                         # 本文件
├── lib/                              # 被动学习核心
│   ├── mirror-learning.js
│   ├── template-clone.js
│   ├── knowledge-transfer.js
│   └── auto-trigger.js               # 🆕 自动触发器
├── scripts/                          # 主动学习核心
├── config/                           # 🆕 配置文件
│   └── auto-learning.json
├── logs/                             # 🆕 日志目录
│   └── auto-triggers.log
├── references/                       # 动态参考
├── assets/                           # 静态资源
├── templates/                        # 神经元模板
└── tests/                            # 测试
```

---

## 🧪 测试

```bash
cd super-learning

# 运行完整测试
node tests/learning.test.js

# 测试自动触发
node lib/auto-trigger.js --test
```

---

## 🔧 配置

### 自动学习配置

位置：`config/auto-learning.json`

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `autoClone.enabled` | 启用自动克隆 | `true` |
| `autoMirror.enabled` | 启用自动镜像 | `true` |
| `autoTransfer.enabled` | 启用自动传递 | `true` |
| `autoMirror.observationPeriod` | 镜像观察期 | `24h` |
| `autoMirror.minObservations` | 最小观察数 | `10` |

---

## 📊 日志

自动触发日志：`logs/auto-triggers.log`

```bash
# 查看触发历史
cat logs/auto-triggers.log

# 实时监控
tail -f logs/auto-triggers.log
```

---

**许可证**: MIT License - 亿人世界
