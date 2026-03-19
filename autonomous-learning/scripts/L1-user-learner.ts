#!/usr/bin/env ts-node
/**
 * L1 用户层学习器
 * 
 * 核心功能:
 * - 捕捉用户纠正信号
 * - 提取认知模式
 * - 更新用户模型
 * - 预测用户意图
 */

import { readFileSync, writeFileSync, appendFileSync } from 'fs';
import { join } from 'path';

// 配置
const WORKSPACE = process.env.WORKSPACE || '/Users/tang/.openclaw/workspaces/yirenverse';
const USER_MODEL_PATH = join(WORKSPACE, 'my-super-skills/autonomous-learning/references/user-model.md');
const CORRECTION_LOG_PATH = join(WORKSPACE, 'my-super-skills/autonomous-learning/assets/correction-patterns.md');

// 纠正信号关键词
const CORRECTION_PATTERNS = [
  '不对',
  '不是',
  '应该是',
  '我说的是',
  '你错了',
  '实际上',
  '纠正',
  'No,',
  'Actually',
  'Wrong',
  'I meant',
];

interface Correction {
  timestamp: string;
  messageId: string;
  original: string;
  correction: string;
  pattern: string;
  learned: string;
}

interface UserModel {
  cognitiveStyle: string[];
  preferences: string[];
  interests: string[];
  taboos: string[];
  lastUpdated: string;
}

/**
 * 检测是否是纠正消息
 */
export function isCorrection(message: string): boolean {
  return CORRECTION_PATTERNS.some(pattern => 
    message.toLowerCase().includes(pattern.toLowerCase())
  );
}

/**
 * 提取纠正中的学习模式
 */
export function extractPattern(original: string, correction: string): string {
  // 简单实现：提取纠正的核心内容
  // TODO: 使用 NLP 提取深层认知模式
  
  if (correction.includes('我说的是')) {
    return '用户期望精确引用，不要猜测';
  }
  if (correction.includes('应该是')) {
    return '用户有明确的预期，需要确认理解';
  }
  if (correction.includes('不对') || correction.includes('不是')) {
    return '用户的理解与我不同，需要调整模型';
  }
  
  return '通用纠正模式';
}

/**
 * 读取用户模型
 */
export function readUserModel(): UserModel {
  try {
    const content = readFileSync(USER_MODEL_PATH, 'utf-8');
    // TODO: 解析 Markdown 格式
    return {
      cognitiveStyle: [],
      preferences: [],
      interests: [],
      taboos: [],
      lastUpdated: new Date().toISOString(),
    };
  } catch (e) {
    // 文件不存在，返回空模型
    return {
      cognitiveStyle: [],
      preferences: [],
      interests: [],
      taboos: [],
      lastUpdated: new Date().toISOString(),
    };
  }
}

/**
 * 更新用户模型
 */
export function updateUserModel(pattern: string, category: 'cognitiveStyle' | 'preferences' | 'interests' | 'taboos') {
  const model = readUserModel();
  
  // 避免重复
  if (!model[category].includes(pattern)) {
    model[category].push(pattern);
    model.lastUpdated = new Date().toISOString();
    
    // 写回文件
    writeUserModel(model);
    console.log(`✅ 已更新用户模型 [${category}]: ${pattern}`);
  }
}

/**
 * 写入用户模型
 */
function writeUserModel(model: UserModel) {
  const content = `# 用户认知模型

_最后更新：${model.lastUpdated}_

---

## 认知风格
${model.cognitiveStyle.map(s => `- ${s}`).join('\n') || '- （暂无数据）'}

## 偏好
${model.preferences.map(s => `- ${s}`).join('\n') || '- （暂无数据）'}

## 兴趣领域
${model.interests.map(s => `- ${s}`).join('\n') || '- （暂无数据）'}

## 禁忌
${model.taboos.map(s => `- ${s}`).join('\n') || '- （暂无数据）'}

---

_此文件由 L1-user-learner.ts 自动更新_
`;
  
  writeFileSync(USER_MODEL_PATH, content, 'utf-8');
}

/**
 * 记录纠正日志
 */
export function logCorrection(correction: Correction) {
  const logEntry = `
## [${correction.timestamp}]

**消息 ID**: ${correction.messageId}
**原始理解**: ${correction.original}
**用户纠正**: ${correction.correction}
**提取模式**: ${correction.pattern}
**学习结果**: ${correction.learned}

---
`;
  
  appendFileSync(CORRECTION_LOG_PATH, logEntry, 'utf-8');
}

/**
 * 预测用户意图（简单实现）
 */
export function predictIntent(context: string): string {
  // TODO: 基于历史模式进行预测
  // 当前只是占位符
  
  if (context.includes('学习') || context.includes('skill')) {
    return '用户可能想讨论或实现学习相关功能';
  }
  if (context.includes('项目') || context.includes('开发')) {
    return '用户可能想规划或推进项目开发';
  }
  
  return '等待更多上下文';
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.includes('--test')) {
    // 测试模式
    console.log('L1 User Learner - Test Mode');
    console.log('isCorrection("不对"): ', isCorrection('你说的不对'));
    console.log('isCorrection("很好"): ', isCorrection('很好'));
  }
  
  if (args.includes('--capture')) {
    // 捕捉模式（由 hook 调用）
    console.log('L1 User Learner - Capture Mode');
    // TODO: 从环境变量或 stdin 读取消息
  }
}
