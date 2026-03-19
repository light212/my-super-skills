# Learning Skill - 神经元学习模块

**版本**: 1.0.0  
**作者**: 亿人世界  
**描述**: 基于神经科学的学习模块，支持镜像学习、模板克隆、知识传递

---

## 理论基础

| 理论 | 科学家 | 学习功能 |
|------|--------|----------|
| **镜像神经元** | Giacomo Rizzolatti | 观察→模仿→内化 |
| **HMAX 模型** | Tomaso Poggio | 分层复制 |
| **整合信息理论** | Christof Koch | 知识传递 |

---

## 核心功能

### 1. 镜像学习 (Mirror Learning)
- **灵感**: Giacomo Rizzolatti 镜像神经元发现
- **功能**: 新神经元通过观察成熟神经元学习
- **命令**: `openclaw learning mirror <observer> <target>`
- **示例**: `openclaw learning mirror new-ceo ceo-yiworld`

### 2. 模板克隆 (Template Clone)
- **灵感**: Tomaso Poggio HMAX 分层模型
- **功能**: 从模板快速创建新神经元
- **命令**: `openclaw learning clone <template> <new-name>`
- **示例**: `openclaw learning clone software-dev software-dev-1`

### 3. 知识传递 (Knowledge Transfer)
- **灵感**: Christof Koch 整合信息理论 (IIT)
- **功能**: 神经元间共享记忆和技能
- **命令**: `openclaw learning transfer <from> <to> [knowledge-type]`
- **示例**: `openclaw learning transfer ceo-yiworld pm-yiworld decision-making`

---

## 使用示例

```bash
# 镜像学习：新 CEO 观察成熟 CEO
openclaw learning mirror new-ceo ceo-yiworld

# 模板克隆：创建软件开发神经元
openclaw learning clone software-dev software-dev-1

# 知识传递：CEO 向 PM 传递决策知识
openclaw learning transfer ceo-yiworld pm-yiworld decision-making

# 查看所有学习记录
openclaw learning list <agent-name>
```

---

## 配置

```json
{
  "learning": {
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
  }
}
```

---

## 文件结构

```
passive-learning/
├── SKILL.md                    # 本文件
├── lib/
│   ├── mirror-learning.js      # 镜像学习
│   ├── template-clone.js       # 模板克隆
│   └── knowledge-transfer.js   # 知识传递
├── templates/
│   ├── software-dev.json       # 软件开发神经元模板
│   ├── product-mgr.json        # 产品经理神经元模板
│   └── ceo.json                # CEO 神经元模板
└── tests/
    └── learning.test.js        # 测试用例
```

---

## API 参考

### mirrorLearning(observer, target)

观察目标神经元的工作流程并内化学习。

**参数**:
- `observer` (string): 观察者神经元名称
- `target` (string): 目标神经元名称

**返回**: Promise<boolean> 学习是否成功

**示例**:
```javascript
const success = await mirrorLearning('new-ceo', 'ceo-yiworld');
```

### cloneFromTemplate(template, newName)

从模板克隆创建新神经元。

**参数**:
- `template` (string): 模板名称
- `newName` (string): 新神经元名称

**返回**: Promise<boolean> 克隆是否成功

**示例**:
```javascript
const success = await cloneFromTemplate('software-dev', 'software-dev-1');
```

### transferKnowledge(from, to, type)

从一个神经元传递知识到另一个神经元。

**参数**:
- `from` (string): 源神经元名称
- `to` (string): 目标神经元名称
- `type` (string): 知识类型 (memory|skills|patterns|all)

**返回**: Promise<boolean> 传递是否成功

**示例**:
```javascript
const success = await transferKnowledge('ceo-yiworld', 'pm-yiworld', 'skills');
```

---

## 安装

```bash
# 复制技能到 OpenClaw 技能目录
cp -r /Users/tangxuguang/Downloads/passive-learning ~/.openclaw/skills/learning

# 或者创建软链接
ln -s /Users/tangxuguang/Downloads/passive-learning ~/.openclaw/skills/learning
```

---

## 测试

```bash
# 运行测试
node tests/learning.test.js
```

---

## 许可证

MIT License - 亿人世界
