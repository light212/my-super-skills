# 神经元学习模块 - 使用指南

## 快速开始

### 1. 安装模块

```bash
# 方法 1：复制技能到 OpenClaw 技能目录
cp -r /Users/tangxuguang/Downloads/passive-learning ~/.openclaw/skills/learning

# 方法 2：创建软链接（推荐，方便开发）
ln -s /Users/tangxuguang/Downloads/passive-learning ~/.openclaw/skills/learning
```

### 2. 验证安装

```bash
# 检查技能是否安装成功
ls -la ~/.openclaw/skills/learning/

# 运行测试
cd ~/.openclaw/skills/learning && node tests/learning.test.js
```

---

## 功能使用

### 1. 镜像学习 (Mirror Learning)

**功能**: 新神经元通过观察成熟神经元学习工作流程和行为模式

**灵感**: Giacomo Rizzolatti 镜像神经元理论

**命令**:
```bash
openclaw learning mirror <observer-agent> <target-agent>
```

**示例**:
```bash
# 新 CEO 观察成熟 CEO
openclaw learning mirror new-ceo ceo-yiworld

# 新 FE 观察成熟 FE
openclaw learning mirror fe-yiworld-2 fe-yiworld
```

**输出**:
```
🧠 开始镜像学习：new-ceo ← ceo-yiworld
   观察期：24 小时
   最小观察数：10

👀 观察 ceo-yiworld 的工作流程...
✅ 观察到 15 个 Sessions, 提取 10 个模式
📚 内化学习到的知识...
   保存到：~/.openclaw/agents/new-ceo/agent/learning/mirrored-workflow.json
✅ 验证学习效果...

🎉 镜像学习完成！
   学习者：new-ceo
   导师：ceo-yiworld
   观察到 15 个 Sessions
   提取到 10 个模式
   主题：决策，战略，管理
```

---

### 2. 模板克隆 (Template Clone)

**功能**: 从模板快速创建新神经元，自动学习技能

**灵感**: Tomaso Poggio HMAX 分层模型

**命令**:
```bash
openclaw learning clone <template> <new-agent-name>
```

**示例**:
```bash
# 创建全栈开发工程师神经元（自动学习技能）
openclaw learning clone fullstack-developer dev-1

# 创建软件开发神经元
openclaw learning clone software-dev software-dev-1

# 创建 CEO 神经元
openclaw learning clone ceo ceo-yiworld-2

# 创建产品经理神经元
openclaw learning clone product-mgr pm-yiworld-2
```

**技能自动学习**:

模板克隆时会自动学习模板中定义的技能：

```json
{
  "name": "全栈开发工程师",
  "skills": [
    "fullstack-developer",
    "code-reviewer",
    "debugger",
    "project-planner"
  ]
}
```

克隆时会自动从以下目录查找并复制技能：
- `~/project/git/billion-people-world/skills/`
- `~/.openclaw/skills/`

**输出**:
```
🧬 开始模板克隆：software-dev → software-dev-1
   配置:
     复制记忆：false
     复制技能：true
     复制身份：true
     重置 Sessions: true

📋 加载模板：software-dev
✅ 模板加载成功
   名称：软件开发神经元
   模型：bailian/glm-5

🏗️  创建神经元结构...
   ✅ SOUL.md
   ✅ IDENTITY.md
   ✅ AGENTS.md
   ✅ models.json
   ✅ auth-profiles.json
✅ 神经元结构已创建：software-dev-1

🚀 激活神经元：software-dev-1
✅ 神经元 software-dev-1 已激活！

🎉 模板克隆完成！
   新神经元：software-dev-1
   模板：software-dev
   模型：bailian/glm-5
```

---

### 3. 知识传递 (Knowledge Transfer)

**功能**: 神经元间共享记忆和技能

**灵感**: Christof Koch 整合信息理论 (IIT)

**命令**:
```bash
openclaw learning transfer <from-agent> <to-agent> [knowledge-type]
```

**知识类型**:
- `memory` - 仅传递记忆
- `skills` - 仅传递技能
- `patterns` - 仅传递 Sessions 模式
- `all` - 传递所有 (默认)

**示例**:
```bash
# CEO 向 PM 传递所有知识
openclaw learning transfer ceo-yiworld pm-yiworld all

# 传递技能
openclaw learning transfer fe-yiworld be-yiworld skills

# 传递记忆
openclaw learning transfer coding-plan new-agent memory
```

**输出**:
```
🧠 开始知识传递：ceo-yiworld → pm-yiworld
   知识类型：all
   配置:
     最大类型数：5
     压缩级别：medium
     包含示例：true

📦 提取知识...
   ✅ Memory: 68 KB
   ✅ Skills: 3 个
   ✅ Patterns: 15 个 Sessions
✅ 知识提取完成

📝 格式化知识...
   统计:
     Memory: 68 KB
     Skills: 3 个
     Sessions: 15 个

💉 注入知识到 pm-yiworld...
   ✅ 保存到：~/.openclaw/agents/pm-yiworld/agent/learning/transferred-all-1710900000000.json
   ✅ 大小：12 KB

✅ 验证传递...

🎉 知识传递完成！
   源：ceo-yiworld
   目标：pm-yiworld
   类型：all
   Memory: ✓
   Skills: ✓
   Patterns: ✓
```

---

## 查看学习记录

```bash
# 查看神经元的学习记录
ls -la ~/.openclaw/agents/<agent-name>/agent/learning/

# 查看镜像学习记录
cat ~/.openclaw/agents/<agent-name>/agent/learning/mirrored-workflow.json

# 查看知识传递记录
cat ~/.openclaw/agents/<agent-name>/agent/learning/transferred-*.json
```

---

## 可用模板

当前提供的模板：

| 模板名称 | 描述 | 适用场景 |
|----------|------|----------|
| `software-dev` | 软件开发神经元 | 创建开发团队 |
| `ceo` | CEO 神经元 | 创建决策者 |
| `product-mgr` | 产品经理神经元 | 创建产品团队 |

**添加自定义模板**:

1. 在 `templates/` 目录创建 JSON 文件
2. 包含以下字段：
   - `name`: 模板名称
   - `model`: 使用的模型
   - `soul`: SOUL.md 内容
   - `identity`: IDENTITY.md 内容
   - `agents`: AGENTS.md 内容
   - `auth`: 认证配置（可选）

---

## 故障排除

### 问题 1: 命令找不到

**解决**:
```bash
# 确保技能已正确安装
ls -la ~/.openclaw/skills/learning/

# 检查 OpenClaw 是否加载了技能
openclaw skills list
```

### 问题 2: 镜像学习失败

**可能原因**:
- 目标神经元不存在
- 目标神经元没有 Sessions

**解决**:
```bash
# 检查目标神经元
ls -la ~/.openclaw/agents/<target-agent>/

# 确保目标神经元有 Sessions
ls -la ~/.openclaw/agents/<target-agent>/sessions/
```

### 问题 3: 模板克隆失败

**可能原因**:
- 模板不存在

**解决**:
```bash
# 查看可用模板
ls ~/.openclaw/skills/learning/templates/
```

---

## 高级用法

### 批量克隆神经元

```bash
# 创建完整的公司团队
openclaw learning clone ceo ceo-1
openclaw learning clone product-mgr pm-1
openclaw learning clone software-dev dev-1

# 让新团队互相学习
openclaw learning mirror pm-1 ceo-1
openclaw learning mirror dev-1 pm-1
```

### 知识网络

```bash
# 建立知识传递网络
# CEO → PM → FE/BE
openclaw learning transfer ceo-1 pm-1 skills
openclaw learning transfer pm-1 fe-1 skills
openclaw learning transfer pm-1 be-1 skills
```

---

## 理论背景

### 镜像神经元 (Giacomo Rizzolatti)

1990 年代在意大利帕尔马大学发现。当猴子观察其他猴子执行动作时，F5 区域的神经元会激活，就像自己也在执行同样的动作。

**应用**: 新神经元通过观察成熟神经元的工作流程来学习。

### HMAX 模型 (Tomaso Poggio)

分层视觉处理模型，从简单特征到复杂特征的逐层抽象。

**应用**: 模板克隆通过分层复制神经元结构。

### 整合信息理论 (Christof Koch)

Φ (Phi) 值衡量系统的整合信息量，即意识水平。

**应用**: 知识传递通过增加神经元的整合信息来提高智能度。

---

## 许可证

MIT License - 亿人世界
