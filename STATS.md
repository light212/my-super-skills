# 技能仓库统计

**仓库**: https://github.com/light212/my-super-skills  
**位置**: `/Users/tangxuguang/project/git/billion-people-world/skills/my-super-skills/`  
**创建日期**: 2026-03-20

---

## 技能列表

| 技能名称 | 描述 | 文件数 | 大小 |
|----------|------|--------|------|
| **fullstack-developer** | 全栈开发工程师 | 1 | 7.4KB |
| **code-reviewer** | 代码审查专家 | 8 | 3.2KB |
| **debugger** | 调试专家 | 1 | 1.1KB |
| **project-planner** | 项目规划师 | 1 | 0.9KB |
| **product-designer** | 产品设计师 | 1 | 0.8KB |

**总计**: 5 个技能，13.4KB

---

## 技能详情

### 1. fullstack-developer (全栈开发工程师)

**适用场景**:
- 构建完整 Web 应用
- 开发 REST/GraphQL API
- 创建 React/Next.js 前端
- 设置数据库和数据模型

**技术栈**:
- **前端**: React, Next.js, TypeScript, Tailwind CSS
- **后端**: Node.js, Express, TypeScript, JWT/OAuth
- **数据库**: PostgreSQL, MongoDB, Prisma, Redis

**文件**:
- `SKILL.md` - 技能定义

### 2. code-reviewer (代码审查专家)

**适用场景**:
- 代码审查
- 质量检查
- 最佳实践建议

**审查规则**:
- `correctness-error-handling.md` - 错误处理
- `maintainability-naming.md` - 命名规范
- `maintainability-type-hints.md` - 类型提示
- `performance-n-plus-one.md` - N+1 查询优化
- `security-sql-injection.md` - SQL 注入防护
- `security-xss-prevention.md` - XSS 防护

**文件**:
- `SKILL.md` - 技能定义
- `AGENTS.md` - Agent 配置
- `rules/` - 审查规则目录

### 3. debugger (调试专家)

**适用场景**:
- 调试复杂问题
- 定位 Bug
- 性能分析

**文件**:
- `SKILL.md` - 技能定义

### 4. project-planner (项目规划师)

**适用场景**:
- 项目规划
- 任务分解
- 时间估算

**文件**:
- `SKILL.md` - 技能定义

### 5. product-designer (产品设计师)

**适用场景**:
- 产品设计
- 用户体验优化
- 界面设计

**文件**:
- `SKILL.md` - 技能定义

---

## 使用统计

### 技能使用频率

```bash
# 查看技能被 Agent 使用情况
ls -la ~/.openclaw/agents/*/agent/skills/ | grep -E "fullstack-developer|code-reviewer|debugger"
```

### 技能学习效果

```bash
# 查看神经元学习的技能
ls -la ~/.openclaw/agents/<agent-name>/agent/skills/
```

---

## 添加新技能

### 1. 创建技能目录

```bash
cd /Users/tangxuguang/project/git/billion-people-world/skills/my-super-skills
mkdir <skill-name>
```

### 2. 创建 SKILL.md

```markdown
---
name: <skill-name>
description: 技能描述
license: MIT
---

# 技能名称

技能详细说明...
```

### 3. 提交并推送

```bash
git add .
git commit -m "feat: 添加 <skill-name> 技能"
git push
```

---

## 与学习模块集成

学习模块会自动从以下目录查找技能：

1. `~/project/git/billion-people-world/skills/my-super-skills/` ⭐ (优先)
2. `~/project/git/billion-people-world/skills/`
3. `~/.openclaw/skills/`

### 示例：克隆全栈工程师

```bash
# 使用学习模块克隆
openclaw learning clone fullstack-developer dev-1

# 输出:
📚 学习技能...
   ✅ 技能：fullstack-developer (从 my-super-skills 仓库)
✅ 学习了 1/1 个技能
```

---

## 许可证

MIT License - 亿人世界
