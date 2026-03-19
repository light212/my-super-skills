# 🧪 Super-Learning 安全测试计划

**测试原则**: 不影响主系统，所有测试在隔离环境进行

---

## 测试环境准备

### 1. 创建测试 Workspace

```bash
# 创建隔离的测试环境
mkdir -p ~/.openclaw/workspaces/super-learning-test
cd ~/.openclaw/workspaces/super-learning-test

# 初始化测试配置
cat > config.json << 'EOF'
{
  "name": "super-learning-test",
  "skills": ["super-learning"],
  "testMode": true
}
EOF
```

### 2. 备份现有配置

```bash
# 备份 Hooks 配置
cp ~/.openclaw/hooks.json ~/.openclaw/hooks.json.backup 2>/dev/null || true

# 备份技能目录
cp -r ~/.openclaw/skills/super-learning ~/.openclaw/skills/super-learning.backup 2>/dev/null || true
```

---

## 测试用例

### Test 1: 脚本语法检查 ✅

```bash
# 测试脚本能否正常加载
node --check super-learning/lib/auto-trigger.js
node --check super-learning/lib/keyword-trigger.js
node --check super-learning/scripts/integrate-hooks.js
node --check super-learning/scripts/evolution-engine.ts
```

**预期**: 无语法错误

---

### Test 2: 路径解析测试 ✅

```bash
# 测试路径解析
WORKSPACE="/tmp/test-workspace" node super-learning/lib/auto-trigger.js --test-paths
```

**预期**: 
- 能正确解析路径
- 自动创建缺失目录
- 不因路径问题崩溃

---

### Test 3: 错误处理测试 ✅

```bash
# 测试错误处理
node -e "
const { logTrigger } = await import('./super-learning/lib/auto-trigger.js');
try {
  logTrigger('test', 'test', {});
  console.log('✅ 错误处理正常');
} catch (e) {
  console.log('❌ 错误处理失败:', e.message);
}
"
```

**预期**: 不因日志写入失败而崩溃

---

### Test 4: Hook 集成测试 ⚠️

```bash
# 1. 先检查现有 Hook 配置
cat ~/.openclaw/hooks.json 2>/dev/null || echo "无现有配置"

# 2. 运行集成脚本（不实际修改）
node super-learning/scripts/integrate-hooks.js --dry-run

# 3. 如果 dry-run 成功，再实际运行
node super-learning/scripts/integrate-hooks.js
```

**预期**:
- 不破坏现有 Hooks
- 只添加缺失的 Hooks
- 支持回滚

---

### Test 5: 关键词触发测试 ✅

```bash
# 测试关键词匹配
node -e "
const { matchMessage } = await import('./super-learning/lib/keyword-trigger.js');

const tests = [
  { input: '创建一个新 CEO', expected: 'clone' },
  { input: '让 dev-2 向 dev-1 学习', expected: 'mirror' },
  { input: '把 CEO 的经验传递给 PM', expected: 'transfer' },
  { input: '让 ceo-1 和 pm-1 一起合作', expected: 'collaborate' },
];

for (const test of tests) {
  const result = matchMessage(test.input);
  console.log(test.input, '→', result?.action || '无匹配', result?.action === test.expected ? '✅' : '❌');
}
"
```

**预期**: 正确匹配所有关键词

---

### Test 6: 自动触发器测试 ✅

```bash
# 测试自动触发逻辑
node -e "
const { onAgentCreated, onAgentStarted, onCollaborationDetected } = await import('./super-learning/lib/auto-trigger.js');

// 测试 Agent 创建
console.log('测试 onAgentCreated...');
await onAgentCreated('ceo-2', { template: 'ceo' });

// 测试 Agent 启动
console.log('测试 onAgentStarted...');
await onAgentStarted('new-dev');

// 测试协作检测
console.log('测试 onCollaborationDetected...');
await onCollaborationDetected('ceo-1', 'pm-1');

console.log('✅ 自动触发器测试完成');
"
```

**预期**: 不崩溃，正确记录日志

---

### Test 7: Hook 超时测试 ✅

```bash
# 测试 Hook 命令超时保护
time bash -c 'timeout 5 node -e "setTimeout(() => console.log(\"完成\"), 100)" 2>/dev/null || true'
time bash -c 'timeout 5 node -e "setTimeout(() => console.log(\"超时\"), 10000)" 2>/dev/null || true'
```

**预期**: 
- 正常脚本 5 秒内完成
- 超时脚本被强制终止

---

### Test 8: 压力测试 ⚠️

```bash
# 模拟大量并发触发
for i in {1..100}; do
  node super-learning/lib/keyword-trigger.js "创建一个新 CEO" &
done
wait

# 检查日志
wc -l super-learning/logs/keyword-triggers.log
```

**预期**: 
- 不因并发崩溃
- 日志正确记录

---

## 回滚方案

### 如果测试失败

```bash
# 1. 恢复 Hooks 配置
cp ~/.openclaw/hooks.json.backup ~/.openclaw/hooks.json

# 2. 恢复技能目录
rm -rf ~/.openclaw/skills/super-learning
cp -r ~/.openclaw/skills/super-learning.backup ~/.openclaw/skills/super-learning

# 3. 重启 OpenClaw
openclaw gateway restart
```

---

## 测试报告模板

```markdown
## 测试结果

| 测试用例 | 状态 | 备注 |
|----------|------|------|
| Test 1: 语法检查 | ✅/❌ | |
| Test 2: 路径解析 | ✅/❌ | |
| Test 3: 错误处理 | ✅/❌ | |
| Test 4: Hook 集成 | ✅/❌ | |
| Test 5: 关键词触发 | ✅/❌ | |
| Test 6: 自动触发器 | ✅/❌ | |
| Test 7: Hook 超时 | ✅/❌ | |
| Test 8: 压力测试 | ✅/❌ | |

## 问题记录

### 问题 1
- **描述**: 
- **原因**: 
- **修复**: 

## 结论

- [ ] 可以上线
- [ ] 需要修复
- [ ] 需要更多测试
```

---

**测试负责人**: AI Assistant  
**测试日期**: 2026-03-20  
**测试环境**: Isolated Test Workspace
