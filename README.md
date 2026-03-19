# My Super Skills

个人超级技能集合 - 基于 OpenClaw 技能系统

## 可用技能

### 全栈开发
- fullstack-developer - 全栈开发工程师
- code-reviewer - 代码审查专家
- debugger - 调试专家
- project-planner - 项目规划师

### 产品与设计
- product-designer - 产品设计师
- user-researcher - 用户研究员

### 测试与质量
- testing-strategy - 测试策略
- jest-testing - Jest 测试
- webapp-testing - Web 应用测试

## 使用方法

```bash
# 克隆技能到 OpenClaw
ln -s /path/to/my-super-skills/<skill-name> ~/.openclaw/skills/<skill-name>
```

## 许可证

MIT License

---

## 🧠 神经元学习模块

`passive-learning/` 目录包含基于神经科学的学习模块：

### 核心功能

1. **镜像学习** (Mirror Learning)
   - 基于 Giacomo Rizzolatti 镜像神经元理论
   - 新神经元通过观察成熟神经元学习

2. **模板克隆** (Template Clone)
   - 基于 Tomaso Poggio HMAX 模型
   - 从模板快速创建新神经元，自动学习技能

3. **知识传递** (Knowledge Transfer)
   - 基于 Christof Koch 整合信息理论
   - 神经元间共享记忆和技能

### 使用示例

```bash
# 克隆全栈工程师（自动学习技能）
openclaw learning clone fullstack-developer dev-1

# 新神经元向老神经元学习
openclaw learning mirror dev-2 dev-1

# 知识传递
openclaw learning transfer dev-1 dev-2 skills
```

详见：[passive-learning/README.md](passive-learning/README.md)
