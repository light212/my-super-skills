#!/usr/bin/env node
/**
 * 关键词触发器 - 匹配中文用户消息
 */

import { appendFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const WORKSPACE = process.env.WORKSPACE || '/Users/tang/.openclaw/workspaces/yirenverse';
const TRIGGER_LOG_PATH = join(WORKSPACE, 'my-super-skills/super-learning/logs/keyword-triggers.log');

const logsDir = dirname(TRIGGER_LOG_PATH);
if (!existsSync(logsDir)) mkdirSync(logsDir, { recursive: true });

// 匹配中文、英文、数字、连字符
const WORD = '[\\u4e00-\\u9fa5a-zA-Z0-9_-]+';

const RULES = [
  {
    name: 'clone',
    patterns: [
      new RegExp(`创建.*?(${WORD})`, 'i'),
      new RegExp(`新建.*?(${WORD})`, 'i'),
      new RegExp(`添加.*?(${WORD})`, 'i'),
      new RegExp(`克隆.*?(${WORD})`, 'i'),
      new RegExp(`来个 (${WORD})`, 'i'),
    ],
    action: 'clone',
    extract: (match) => {
      const type = match[1];
      return { template: mapTypeToTemplate(type), name: generateAgentName(type), type };
    }
  },
  {
    name: 'mirror',
    patterns: [
      /让\s*(.*)\s* 向\s*(.*)\s* 学习/,
      /(.*)\s* 观察\s*(.*)/,
      /(.*)\s* 模仿\s*(.*)/,
    ],
    action: 'mirror',
    extract: (match) => ({ observer: match[1].trim(), target: match[2].trim() })
  },
  {
    name: 'transfer',
    patterns: [
      new RegExp(`把 (${WORD}).*?传递给 (${WORD})`, 'i'),
      new RegExp(`(${WORD}).*?教 (${WORD})`, 'i'),
      new RegExp(`(${WORD}).*?分享给 (${WORD})`, 'i'),
    ],
    action: 'transfer',
    extract: (match, message) => ({
      from: match[1],
      to: match[2],
      type: extractKnowledgeType(message)
    })
  },
  {
    name: 'collaborate',
    patterns: [
      new RegExp(`(${WORD}).*?和 (${WORD}).*?一起`, 'i'),
      new RegExp(`(${WORD}).*?与 (${WORD}).*?合作`, 'i'),
    ],
    action: 'collaborate',
    extract: (match) => ({ agents: [match[1], match[2]] })
  },
];

function mapTypeToTemplate(type) {
  const mapping = {
    'ceo': 'ceo', '总裁': 'ceo', '老板': 'ceo',
    'pm': 'product-mgr', '产品': 'product-mgr', '产品经理': 'product-mgr',
    'dev': 'software-dev', '开发': 'software-dev', '工程师': 'software-dev',
    'fe': 'fullstack-developer', '前端': 'fullstack-developer', '全栈': 'fullstack-developer',
    'be': 'software-dev', '后端': 'software-dev',
    'designer': 'product-designer', '设计': 'product-designer',
  };
  for (const [key, template] of Object.entries(mapping)) {
    if (type.toLowerCase().includes(key)) return template;
  }
  return 'software-dev';
}

function generateAgentName(type) {
  return `${mapTypeToTemplate(type)}-${Date.now()}`;
}

function extractKnowledgeType(message) {
  if (message.includes('经验') || message.includes('技能')) return 'skills';
  if (message.includes('记忆')) return 'memory';
  if (message.includes('模式')) return 'patterns';
  return 'all';
}

export function matchMessage(message) {
  for (const rule of RULES) {
    for (const pattern of rule.patterns) {
      const match = message.match(pattern);
      if (match) {
        return {
          rule: rule.name,
          action: rule.action,
          params: rule.extract(match, message),
          confidence: Math.min(1.0, match[0].length / message.length),
        };
      }
    }
  }
  return null;
}

function logTrigger(result, message) {
  const entry = `[${new Date().toISOString()}] "${message}"\n  → ${result.action}(${JSON.stringify(result.params)})\n\n`;
  appendFileSync(TRIGGER_LOG_PATH, entry, 'utf-8');
}

async function executeAction(action, params) {
  console.log(`🧠 执行：${action}`, JSON.stringify(params));
  return { success: true, action, params };
}

export async function handleMessage(message) {
  console.log(`📥 "${message}"`);
  const result = matchMessage(message);
  
  if (result) {
    console.log(`✅ ${result.rule} → ${result.action}`, result.params);
    logTrigger(result, message);
    if (result.confidence >= 0.5) {
      await executeAction(result.action, result.params);
    }
    return result;
  }
  
  console.log('⏭️ 无匹配');
  return null;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  
  if (args.includes('--test')) {
    const tests = [
      '创建一个新 CEO',
      '让新 FE 向 fe-1 学习',
      '把 CEO 的经验传递给 PM',
      'dev-1 和 pm-1 一起',
      '克隆一个产品经理',
    ];
    for (const msg of tests) {
      console.log(`\n--- "${msg}" ---`);
      await handleMessage(msg);
    }
  }
  
  if (args.includes('--message')) {
    const msg = args[args.indexOf('--message') + 1];
    if (msg) await handleMessage(msg);
  }
}
