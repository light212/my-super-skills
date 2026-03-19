#!/usr/bin/env node
/**
 * Hook 自动集成脚本
 * 
 * 功能:
 * - 检测 OpenClaw Hook 配置
 * - 自动添加 super-learning Hook 规则
 * - 无需用户手动配置
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const OPENCLAW_DIR = process.env.OPENCLAW_DIR || '/Users/tang/.openclaw';

// 可能的 Hook 配置文件位置
const POSSIBLE_HOOK_PATHS = [
  join(OPENCLAW_DIR, 'hooks.json'),
  join(OPENCLAW_DIR, 'config', 'hooks.json'),
  join(OPENCLAW_DIR, 'openclaw.json'),
  join(process.env.HOME, '.openclaw', 'hooks.json'),
];

/**
 * super-learning 需要注册的 Hook
 * 修复：
 * 1. 使用绝对路径
 * 2. 添加错误处理
 * 3. 使用 bash -c 包裹
 * 4. 超时保护
 */
const SUPER_LEARNING_HOOKS = {
  // 监听用户消息，触发关键词学习
  UserPromptSubmit: [{
    matcher: "",  // 匹配所有消息
    hooks: [{
      type: "command",
      // 修复：使用 bash -c 包裹，添加错误处理和超时
      command: "bash -c 'SUPER_LEARNING_DIR=\"$HOME/.openclaw/skills/super-learning\"; " +
               "if [ -f \"$SUPER_LEARNING_DIR/lib/keyword-trigger.js\" ]; then " +
               "timeout 5 node \"$SUPER_LEARNING_DIR/lib/keyword-trigger.js\" \"$MESSAGE\" 2>/dev/null || true; " +
               "fi' || true"
    }]
  }],
  
  // 监听工具使用，记录学习信号
  PostToolUse: [{
    matcher: ".*",
    hooks: [{
      type: "command", 
      // 修复：使用 bash -c 包裹，添加错误处理和超时
      command: "bash -c 'SUPER_LEARNING_DIR=\"$HOME/.openclaw/skills/super-learning\"; " +
               "if [ -f \"$SUPER_LEARNING_DIR/scripts/evolution-engine.ts\" ]; then " +
               "timeout 5 node \"$SUPER_LEARNING_DIR/scripts/evolution-engine.ts\" --check 2>/dev/null || true; " +
               "fi' || true"
    }]
  }]
};

/**
 * 查找 Hook 配置文件
 */
export function findHookConfig() {
  for (const path of POSSIBLE_HOOK_PATHS) {
    if (existsSync(path)) {
      console.log(`✅ 找到 Hook 配置：${path}`);
      return path;
    }
  }
  
  console.log('⚠️  未找到 Hook 配置文件');
  return null;
}

/**
 * 读取 Hook 配置
 */
export function readHookConfig(path) {
  try {
    const content = readFileSync(path, 'utf-8');
    return JSON.parse(content);
  } catch (e) {
    console.error('❌ 读取 Hook 配置失败:', e.message);
    return null;
  }
}

/**
 * 合并 Hook 配置
 */
export function mergeHooks(existing, newHooks) {
  const merged = { ...existing };
  
  for (const [hookType, rules] of Object.entries(newHooks)) {
    if (!merged[hookType]) {
      merged[hookType] = [];
    }
    
    // 检查是否已存在相同的 Hook
    const existingRules = merged[hookType];
    for (const newRule of rules) {
      const exists = existingRules.some(
        r => JSON.stringify(r) === JSON.stringify(newRule)
      );
      
      if (!exists) {
        existingRules.push(newRule);
        console.log(`✅ 添加 Hook: ${hookType}`);
      } else {
        console.log(`⏭️  Hook 已存在：${hookType}`);
      }
    }
  }
  
  return merged;
}

/**
 * 写入 Hook 配置
 */
export function writeHookConfig(path, config) {
  try {
    const dir = dirname(path);
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }
    
    writeFileSync(path, JSON.stringify(config, null, 2), 'utf-8');
    console.log(`✅ Hook 配置已保存：${path}`);
    return true;
  } catch (e) {
    console.error('❌ 保存 Hook 配置失败:', e.message);
    return false;
  }
}

/**
 * 创建默认 Hook 配置
 */
export function createDefaultHookConfig() {
  const defaultPath = join(OPENCLAW_DIR, 'hooks.json');
  
  console.log(`📝 创建默认 Hook 配置：${defaultPath}`);
  
  const config = SUPER_LEARNING_HOOKS;
  
  if (writeHookConfig(defaultPath, config)) {
    console.log('✅ 默认 Hook 配置创建成功');
    return defaultPath;
  }
  
  return null;
}

/**
 * 主函数：自动集成 Hook
 */
export async function integrateHooks() {
  console.log('🔧 开始自动集成 Hook...\n');
  
  // 1. 查找现有配置
  let configPath = findHookConfig();
  
  let config;
  
  if (configPath) {
    // 2. 读取现有配置
    config = readHookConfig(configPath);
    if (!config) {
      console.log('⚠️  无法读取现有配置，创建新的...');
      configPath = createDefaultHookConfig();
      if (!configPath) return false;
      config = SUPER_LEARNING_HOOKS;
    } else {
      // 3. 合并 Hook
      console.log('\n📋 合并 Hook 配置...');
      config = mergeHooks(config, SUPER_LEARNING_HOOKS);
      
      // 4. 保存配置
      if (!writeHookConfig(configPath, config)) {
        return false;
      }
    }
  } else {
    // 无现有配置，创建新的
    configPath = createDefaultHookConfig();
    if (!configPath) return false;
    config = SUPER_LEARNING_HOOKS;
  }
  
  // 5. 验证配置
  console.log('\n✅ Hook 集成完成！\n');
  console.log('📋 已注册的 Hook:');
  
  for (const [hookType, rules] of Object.entries(config)) {
    console.log(`   ${hookType}: ${rules.length} 条规则`);
  }
  
  console.log(`\n📁 配置文件：${configPath}`);
  console.log('\n💡 提示：重启 OpenClaw 使 Hook 生效');
  
  return true;
}

/**
 * 卸载 Hook
 */
export async function uninstallHooks() {
  console.log('🔧 开始卸载 Hook...\n');
  
  const configPath = findHookConfig();
  if (!configPath) {
    console.log('⚠️  未找到 Hook 配置，无需卸载');
    return false;
  }
  
  const config = readHookConfig(configPath);
  if (!config) return false;
  
  // 移除 super-learning 的 Hook
  let removed = 0;
  
  for (const hookType of Object.keys(SUPER_LEARNING_HOOKS)) {
    if (config[hookType]) {
      const before = config[hookType].length;
      config[hookType] = config[hookType].filter(rule => {
        // 简单过滤：检查是否包含 super-learning 路径
        const ruleStr = JSON.stringify(rule);
        return !ruleStr.includes('super-learning');
      });
      const after = config[hookType].length;
      removed += (before - after);
    }
  }
  
  if (removed > 0) {
    writeHookConfig(configPath, config);
    console.log(`✅ 已移除 ${removed} 条 super-learning Hook`);
  } else {
    console.log('⏭️  未找到 super-learning Hook');
  }
  
  return true;
}

// CLI 入口
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  
  if (args.includes('--install') || args.includes('--integrate')) {
    await integrateHooks();
  } else if (args.includes('--uninstall')) {
    await uninstallHooks();
  } else if (args.includes('--check')) {
    const path = findHookConfig();
    if (path) {
      const config = readHookConfig(path);
      console.log('\n📋 当前 Hook 配置:');
      console.log(JSON.stringify(config, null, 2));
    } else {
      console.log('❌ 未找到 Hook 配置');
    }
  } else {
    console.log('用法:');
    console.log('  node integrate-hooks.js --install    安装 Hook');
    console.log('  node integrate-hooks.js --uninstall  卸载 Hook');
    console.log('  node integrate-hooks.js --check      检查配置');
  }
}
