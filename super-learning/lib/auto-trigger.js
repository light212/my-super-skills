#!/usr/bin/env node
/**
 * 被动学习自动触发器
 * 
 * 核心功能:
 * - 监听 OpenClaw 事件（Agent 创建/启动/协作）
 * - 自动触发镜像学习/模板克隆/知识传递
 * - 无需用户手动命令
 */

import { readFileSync, writeFileSync, appendFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WORKSPACE = process.env.WORKSPACE || '/Users/tang/.openclaw/workspaces/yirenverse';
const CONFIG_PATH = join(WORKSPACE, 'my-super-skills/super-learning/config/auto-learning.json');
const TRIGGER_LOG_PATH = join(WORKSPACE, 'my-super-skills/super-learning/logs/auto-triggers.log');

// 确保目录存在
const logsDir = dirname(TRIGGER_LOG_PATH);
if (!existsSync(logsDir)) {
  mkdirSync(logsDir, { recursive: true });
}

/**
 * 自动学习配置
 */
const defaultConfig = {
  // 自动克隆：创建新 Agent 时从模板克隆
  autoClone: {
    enabled: true,
    templates: {
      'ceo': 'ceo',
      'pm': 'product-mgr',
      'dev': 'software-dev',
      'fe': 'fullstack-developer',
    },
    defaultTemplate: 'software-dev'
  },
  
  // 自动镜像：新 Agent 启动时向成熟 Agent 学习
  autoMirror: {
    enabled: true,
    observationPeriod: '24h',
    minObservations: 10,
    pairs: [
      { observer: 'new-*', target: '*-1' },  // 新模式：new-xxx → xxx-1
      { observer: '*-2', target: '*-1' },    // 2 号向 1 号学习
    ]
  },
  
  // 自动传递：检测到协作时传递知识
  autoTransfer: {
    enabled: true,
    rules: [
      { from: 'ceo-*', to: 'pm-*', type: 'skills' },
      { from: 'pm-*', to: 'dev-*', type: 'patterns' },
      { from: '*-1', to: '*-2', type: 'memory' },
    ]
  }
};

/**
 * 加载配置
 */
export function loadConfig() {
  try {
    if (existsSync(CONFIG_PATH)) {
      const content = readFileSync(CONFIG_PATH, 'utf-8');
      return JSON.parse(content);
    }
  } catch (e) {
    console.warn('加载配置失败，使用默认配置', e);
  }
  
  return defaultConfig;
}

/**
 * 保存配置
 */
export function saveConfig(config) {
  const configDir = dirname(CONFIG_PATH);
  if (!existsSync(configDir)) {
    mkdirSync(configDir, { recursive: true });
  }
  
  writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2), 'utf-8');
}

/**
 * 记录触发日志
 */
export function logTrigger(event, action, details) {
  const entry = {
    timestamp: new Date().toISOString(),
    event,
    action,
    details,
  };
  
  const logEntry = `[${entry.timestamp}] ${event} → ${action}\n  ${JSON.stringify(details, null, 2)}\n\n`;
  appendFileSync(TRIGGER_LOG_PATH, logEntry, 'utf-8');
  
  console.log(`🧠 自动触发：${event} → ${action}`);
}

/**
 * 事件：Agent 创建
 * 自动动作：从模板克隆
 */
export async function onAgentCreated(agentName, metadata = {}) {
  const config = loadConfig();
  
  if (!config.autoClone.enabled) {
    console.log('⏸️  自动克隆已禁用');
    return;
  }
  
  // 匹配模板
  let template = config.autoClone.defaultTemplate;
  
  for (const [pattern, tmpl] of Object.entries(config.autoClone.templates)) {
    if (agentName.includes(pattern)) {
      template = tmpl;
      break;
    }
  }
  
  // 如果用户指定了模板
  if (metadata.template) {
    template = metadata.template;
  }
  
  logTrigger('agent.created', 'clone', {
    agent: agentName,
    template,
    metadata,
  });
  
  // 执行克隆
  return await cloneFromTemplate(template, agentName);
}

/**
 * 事件：Agent 启动
 * 自动动作：安排镜像学习
 */
export async function onAgentStarted(agentName, metadata = {}) {
  const config = loadConfig();
  
  if (!config.autoMirror.enabled) {
    console.log('⏸️  自动镜像已禁用');
    return;
  }
  
  // 查找匹配的镜像对
  const target = findMirrorTarget(agentName, config.autoMirror.pairs);
  
  if (!target) {
    console.log(`⏭️  未找到 ${agentName} 的镜像目标`);
    return;
  }
  
  logTrigger('agent.started', 'mirror', {
    observer: agentName,
    target,
    period: config.autoMirror.observationPeriod,
  });
  
  // 执行镜像学习
  return await mirrorLearning(agentName, target, {
    period: config.autoMirror.observationPeriod,
    minObservations: config.autoMirror.minObservations,
  });
}

/**
 * 事件：检测到协作
 * 自动动作：知识传递
 */
export async function onCollaborationDetected(agents, context = {}) {
  const config = loadConfig();
  
  if (!config.autoTransfer.enabled) {
    console.log('⏸️  自动传递已禁用');
    return;
  }
  
  // 查找匹配的传递规则
  const rules = findTransferRules(agents, config.autoTransfer.rules);
  
  if (rules.length === 0) {
    console.log(`⏭️  未找到 ${agents.join(', ')} 的传递规则`);
    return;
  }
  
  for (const rule of rules) {
    logTrigger('collaboration.detected', 'transfer', {
      from: rule.from,
      to: rule.to,
      type: rule.type,
    });
    
    // 执行知识传递
    await transferKnowledge(rule.from, rule.to, rule.type);
  }
}

/**
 * 查找镜像目标
 */
function findMirrorTarget(observer, pairs) {
  for (const pair of pairs) {
    const { observer: obsPattern, target } = pair;
    
    // 简单模式匹配
    if (matchPattern(observer, obsPattern)) {
      // 替换通配符
      return target.replace('*', observer.replace(obsPattern.replace('*', ''), ''));
    }
  }
  
  return null;
}

/**
 * 查找传递规则
 */
function findTransferRules(agents, rules) {
  const matched = [];
  
  for (const rule of rules) {
    const fromMatch = agents.find(a => matchPattern(a, rule.from));
    const toMatch = agents.find(a => matchPattern(a, rule.to));
    
    if (fromMatch && toMatch) {
      matched.push({
        from: fromMatch,
        to: toMatch,
        type: rule.type,
      });
    }
  }
  
  return matched;
}

/**
 * 简单模式匹配
 */
function matchPattern(str, pattern) {
  if (pattern === '*') return true;
  if (pattern.endsWith('-*')) {
    return str.startsWith(pattern.replace('-*', ''));
  }
  if (pattern.startsWith('*-')) {
    return str.endsWith(pattern.replace('*-', ''));
  }
  if (pattern.includes('*')) {
    const regex = new RegExp(pattern.replace('*', '.*'));
    return regex.test(str);
  }
  return str === pattern;
}

/**
 * 执行克隆（占位符）
 */
async function cloneFromTemplate(template, newName) {
  console.log(`🧬 克隆模板：${template} → ${newName}`);
  // TODO: 调用实际的克隆逻辑
  return { success: true, template, newName };
}

/**
 * 执行镜像学习（占位符）
 */
async function mirrorLearning(observer, target, options = {}) {
  console.log(`👀 镜像学习：${observer} ← ${target}`);
  // TODO: 调用实际的镜像学习逻辑
  return { success: true, observer, target, ...options };
}

/**
 * 执行知识传递（占位符）
 */
async function transferKnowledge(from, to, type) {
  console.log(`💉 知识传递：${from} → ${to} (${type})`);
  // TODO: 调用实际的知识传递逻辑
  return { success: true, from, to, type };
}

/**
 * 初始化自动触发器
 * 注册到 OpenClaw 事件系统
 */
export function initAutoTrigger() {
  console.log('🧠 初始化自动触发器...');
  
  const config = loadConfig();
  console.log('✅ 配置加载成功');
  console.log(`   自动克隆：${config.autoClone.enabled ? '✓' : '✗'}`);
  console.log(`   自动镜像：${config.autoMirror.enabled ? '✓' : '✗'}`);
  console.log(`   自动传递：${config.autoTransfer.enabled ? '✓' : '✗'}`);
  
  // TODO: 注册到 OpenClaw Hook 系统
  // - UserPromptSubmit
  // - AgentCreated
  // - AgentStarted
  // - CollaborationDetected
  
  return {
    onAgentCreated,
    onAgentStarted,
    onCollaborationDetected,
  };
}

// CLI 入口
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  
  if (args.includes('--init')) {
    initAutoTrigger();
  }
  
  if (args.includes('--test')) {
    console.log('🧪 测试自动触发器...');
    
    // 测试事件
    await onAgentCreated('new-ceo', { template: 'ceo' });
    await onAgentStarted('new-ceo');
    await onCollaborationDetected(['ceo-1', 'pm-1']);
    
    console.log('✅ 测试完成');
  }
  
  if (args.includes('--config')) {
    const config = loadConfig();
    console.log('📋 当前配置:');
    console.log(JSON.stringify(config, null, 2));
  }
}
