# 技能模式库

_从同级 Skills 提取的设计模式_

_最后更新：2026-03-20T02:11:00.000Z_

---

## 待扫描

运行 `L2-skill-learner.ts --scan` 开始分析

---

## 已提取模式

### self-improvement

**可借鉴**:
- 三分法日志结构（ERRORS.md / LEARNINGS.md / FEATURE_REQUESTS.md）
- 纠正检测触发器
- 优先级分类系统

**需规避**:
- 日志可能过于冗长

### skill-creator

**可借鉴**:
- 渐进式披露设计（元数据 → SKILL.md → references）
- 6 步创建流程
- 自动化验证 + 打包

**需规避**:
- 步骤可能过于繁琐

### capability-evolver

**可借鉴**:
- GEP 协议（可审计的进化）
- 自修复机制
- 风险协议设计

---

## 技能对比矩阵

| Skill | 触发设计 | 工作流 | 错误处理 | 可借鉴点 | 需规避点 |
|-------|----------|--------|----------|----------|----------|
| self-improvement | 纠正检测 | 日志→提升 | 完善 | 分类清晰 | 日志冗长 |
| skill-creator | 创建指令 | 6 步流程 | 中等 | 渐进披露 | 步骤繁琐 |
| capability-evolver | /evolve 命令 | 分析→进化 | 完善 | GEP 协议 | 配置复杂 |

---

_此文件由 L2-skill-learner.ts 自动更新_
