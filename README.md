# My Super Skills - 超脑学习系统

🧠 **Super-Learning** - 完整的自主学习系统

基于神经科学 + 元认知理论，整合被动学习（镜像/克隆/传递）与主动学习（L1 用户/L2 技能/L3 系统），打造持续进化的 AI 神经元。

---

## 🚀 快速开始

### 安装到 OpenClaw

```bash
# 方法 1：软链接（推荐，方便开发）
ln -s /Users/tang/.openclaw/workspaces/yirenverse/my-super-skills/super-learning ~/.openclaw/skills/super-learning

# 方法 2：复制
cp -r /Users/tang/.openclaw/workspaces/yirenverse/my-super-skills/super-learning ~/.openclaw/skills/
```

### 验证安装

```bash
ls -la ~/.openclaw/skills/super-learning/
```

---

## 📚 可用技能

### Super-Learning (超脑学习系统)

**唯一技能，完整功能**

| 功能模块 | 描述 | 命令示例 |
|----------|------|----------|
| **镜像学习** | 观察成熟神经元工作流程 | `openclaw learning mirror new-ceo ceo-1` |
| **模板克隆** | 从模板快速创建神经元 | `openclaw learning clone software-dev dev-1` |
| **知识传递** | 神经元间共享记忆技能 | `openclaw learning transfer ceo pm skills` |
| **L1 用户学习** | 捕捉纠正，更新偏好 | 自动运行（Hook 触发） |
| **L2 技能学习** | 扫描同级优点 | `node scripts/L2-skill-learner.ts --scan` |
| **L3 系统学习** | 检测架构模式 | `node scripts/L3-system-optimizer.ts --analyze` |
| **进化引擎** | 决策优化方向 | `node scripts/evolution-engine.ts --run` |

---

## 🧠 理论基础

| 理论 | 科学家 | 应用 |
|------|--------|------|
| **镜像神经元** | Giacomo Rizzolatti (Parma, 1990s) | 镜像学习 - 观察→模仿→内化 |
| **HMAX 模型** | Tomaso Poggio (MIT) | 模板克隆 - 分层复制 |
| **整合信息论** | Christof Koch (Allen Institute) | 知识传递 - Φ值衡量 |
| **预测编码** | Karl Friston | 主动学习 - 预测误差驱动 |
| **元认知** | John Flavell | 三层学习 - 对学习的学习 |

---

## 📖 使用文档

- **[Super-Learning 完整文档](super-learning/README.md)** - 使用指南
- **[Super-Learning SKILL.md](super-learning/SKILL.md)** - 技能协议

---

## 🎯 典型场景

### 1. 创建新团队

```bash
# 克隆核心团队
openclaw learning clone ceo ceo-1
openclaw learning clone product-mgr pm-1
openclaw learning clone software-dev dev-1

# 镜像学习
openclaw learning mirror pm-1 ceo-1
openclaw learning mirror dev-1 pm-1

# 知识传递
openclaw learning transfer ceo-1 pm-1 skills
```

### 2. 用户个性化

无需手动命令，Hook 自动捕捉纠正并更新 `user-model.md`。

### 3. 技能生态进化

```bash
# 每周扫描技能
node super-learning/scripts/L2-skill-learner.ts --scan

# 查看提取的模式
cat super-learning/references/skill-patterns.md
```

### 4. 系统优化

```bash
# 分析运行时
node super-learning/scripts/L3-system-optimizer.ts --analyze

# 查看优化提案
cat super-learning/assets/optimization-proposals.md
```

---

## 📁 仓库结构

```
my-super-skills/
├── README.md                      # 本文件
├── STATS.md                       # 统计信息
└── super-learning/                # 超脑学习系统
    ├── SKILL.md                   # 核心协议
    ├── README.md                  # 使用指南
    ├── lib/                       # 被动学习核心
    │   ├── mirror-learning.js
    │   ├── template-clone.js
    │   └── knowledge-transfer.js
    ├── scripts/                   # 主动学习核心
    │   ├── L1-user-learner.ts
    │   ├── L2-skill-learner.ts
    │   ├── L3-system-optimizer.ts
    │   └── evolution-engine.ts
    ├── references/                # 动态参考
    │   ├── user-model.md
    │   ├── skill-patterns.md
    │   ├── system-architecture.md
    │   └── evolution-history.md
    ├── assets/                    # 静态资源
    │   ├── correction-patterns.md
    │   └── optimization-proposals.md
    ├── templates/                 # 神经元模板
    │   ├── ceo.json
    │   ├── product-mgr.json
    │   ├── software-dev.json
    │   └── fullstack-developer.json
    └── tests/                     # 测试
        └── learning.test.js
```

---

## 🔧 配置

### OpenClaw Hook 配置

在 `~/.openclaw/hooks.json` 添加：

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "super-learning/scripts/L1-user-learner.ts --capture"
      }]
    }]
  }
}
```

### 学习配置

在 `~/.openclaw/config.json` 添加：

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

## 🧪 测试

```bash
cd super-learning

# 运行完整测试
node tests/learning.test.js
```

---

## 📊 统计

- **技能数量**: 1 (Super-Learning)
- **代码量**: ~2700 行
- **文件数**: 20
- **神经元模板**: 4 (CEO/产品/全栈/软件开发)

详见：[STATS.md](STATS.md)

---

## 🤝 贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

---

## 📝 更新日志

### 2026-03-20 - v1.0.0

- ✅ 创建 Super-Learning 完整学习系统
- ✅ 整合被动学习（镜像/克隆/传递）
- ✅ 整合主动学习（L1/L2/L3）
- ✅ 实现进化引擎
- ✅ 提供 4 个神经元模板
- ✅ 清理冗余技能，只保留 Super-Learning

---

## 📄 许可证

MIT License - 亿人世界

---

**GitHub**: https://github.com/light212/my-super-skills
