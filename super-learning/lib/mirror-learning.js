#!/usr/bin/env node

/**
 * 镜像学习模块
 * 基于 Giacomo Rizzolatti 镜像神经元理论
 * 
 * 功能：新神经元通过观察成熟神经元学习工作流程和行为模式
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/**
 * 镜像学习配置
 */
const MIRROR_CONFIG = {
  observationPeriod: 24 * 60 * 60 * 1000, // 24 小时
  minObservations: 10,
  learningRate: 0.8,
};

/**
 * 观察目标神经元的工作流程
 * @param {string} targetAgent - 目标神经元名称
 * @returns {Promise<Object>} 工作流程数据
 */
async function observeWorkflow(targetAgent) {
  const stateDir = process.env.OPENCLAW_STATE_DIR || path.join(process.env.HOME || '~', '.openclaw');
  const agentDir = path.join(stateDir, 'agents', targetAgent);
  
  console.log(`👀 观察 ${targetAgent} 的工作流程...`);
  
  // 1. 读取目标神经元的配置
  const configPath = path.join(agentDir, 'agent', 'models.json');
  let config = {};
  try {
    const configContent = await fs.readFile(configPath, 'utf-8');
    config = JSON.parse(configContent);
  } catch (error) {
    console.warn(`⚠️  无法读取配置文件：${configPath}`);
  }
  
  // 2. 读取 Sessions 历史
  const sessionsDir = path.join(agentDir, 'sessions');
  let sessions = [];
  try {
    sessions = await fs.readdir(sessionsDir);
  } catch (error) {
    console.warn(`⚠️  无法读取 Sessions 目录：${sessionsDir}`);
  }
  
  // 3. 分析工作模式
  const workflow = {
    model: config.models?.default || 'bailian/glm-5',
    sessionCount: sessions.length,
    patterns: [],
  };
  
  // 4. 提取最近的行为模式
  const recentSessions = sessions.slice(-MIRROR_CONFIG.minObservations);
  for (const session of recentSessions) {
    const sessionPath = path.join(sessionsDir, session);
    try {
      const sessionData = await analyzeSession(sessionPath);
      workflow.patterns.push(sessionData);
    } catch (error) {
      console.warn(`⚠️  无法分析 Session: ${session}`);
    }
  }
  
  console.log(`✅ 观察到 ${workflow.sessionCount} 个 Sessions, 提取 ${workflow.patterns.length} 个模式`);
  
  return workflow;
}

/**
 * 分析单个 Session
 * @param {string} sessionPath - Session 目录路径
 * @returns {Promise<Object>} Session 分析结果
 */
async function analyzeSession(sessionPath) {
  // 读取 session 文件
  const files = await fs.readdir(sessionPath);
  const messages = [];
  
  for (const file of files) {
    if (file.endsWith('.json')) {
      try {
        const content = await fs.readFile(path.join(sessionPath, file), 'utf-8');
        messages.push(JSON.parse(content));
      } catch (error) {
        // 跳过无法读取的文件
      }
    }
  }
  
  // 分析对话模式
  const totalLength = messages.reduce((sum, m) => sum + (m.content?.length || 0), 0);
  
  return {
    messageCount: messages.length,
    avgResponseLength: messages.length > 0 ? totalLength / messages.length : 0,
    topics: extractTopics(messages),
    timestamp: new Date().toISOString(),
  };
}

/**
 * 提取主题
 * @param {Array<Object>} messages - 消息列表
 * @returns {Array<string>} 主题列表
 */
function extractTopics(messages) {
  const topics = new Set();
  for (const msg of messages) {
    if (msg.content?.includes('#')) {
      const matches = msg.content.match(/#(\w+)/g);
      if (matches) {
        matches.forEach(t => topics.add(t.replace('#', '')));
      }
    }
  }
  return Array.from(topics);
}

/**
 * 内化学习到的工作流程
 * @param {string} observerAgent - 观察者神经元名称
 * @param {Object} workflow - 工作流程数据
 * @returns {Promise<void>}
 */
async function internalizeWorkflow(observerAgent, workflow) {
  const stateDir = process.env.OPENCLAW_STATE_DIR || path.join(process.env.HOME || '~', '.openclaw');
  const agentDir = path.join(stateDir, 'agents', observerAgent);
  const learningDir = path.join(agentDir, 'agent', 'learning');
  
  // 创建学习目录
  await fs.mkdir(learningDir, { recursive: true });
  
  // 保存学习到的工作流程
  const workflowPath = path.join(learningDir, 'mirrored-workflow.json');
  const learningData = {
    learnedAt: new Date().toISOString(),
    targetAgent: workflow.targetAgent,
    workflow: workflow,
    config: MIRROR_CONFIG,
  };
  
  await fs.writeFile(workflowPath, JSON.stringify(learningData, null, 2));
  
  console.log(`📚 内化学习到的知识...`);
  console.log(`   保存到：${workflowPath}`);
}

/**
 * 验证学习效果
 * @param {string} observerAgent - 观察者神经元名称
 * @returns {Promise<boolean>} 验证是否成功
 */
async function validateLearning(observerAgent) {
  const stateDir = process.env.OPENCLAW_STATE_DIR || path.join(process.env.HOME || '~', '.openclaw');
  const agentDir = path.join(stateDir, 'agents', observerAgent);
  const learningDir = path.join(agentDir, 'agent', 'learning');
  
  try {
    const workflowPath = path.join(learningDir, 'mirrored-workflow.json');
    await fs.access(workflowPath);
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * 主函数：镜像学习
 * @param {string} observerAgent - 观察者神经元
 * @param {string} targetAgent - 目标神经元
 * @returns {Promise<boolean>} 学习是否成功
 */
async function mirrorLearning(observerAgent, targetAgent) {
  console.log(`🧠 开始镜像学习：${observerAgent} ← ${targetAgent}`);
  console.log(`   观察期：${MIRROR_CONFIG.observationPeriod / (1000 * 60 * 60)} 小时`);
  console.log(`   最小观察数：${MIRROR_CONFIG.minObservations}`);
  console.log(``);
  
  // 1. 观察目标神经元
  const workflow = await observeWorkflow(targetAgent);
  workflow.targetAgent = targetAgent;
  
  // 2. 内化学习
  await internalizeWorkflow(observerAgent, workflow);
  
  // 3. 验证学习
  console.log(`✅ 验证学习效果...`);
  const validated = await validateLearning(observerAgent);
  
  if (validated) {
    console.log(``);
    console.log(`🎉 镜像学习完成！`);
    console.log(`   学习者：${observerAgent}`);
    console.log(`   导师：${targetAgent}`);
    console.log(`   观察到 ${workflow.sessionCount} 个 Sessions`);
    console.log(`   提取到 ${workflow.patterns.length} 个模式`);
    if (workflow.patterns.length > 0) {
      const topics = workflow.patterns[0]?.topics || [];
      console.log(`   主题：${topics.join(', ') || '无'}`);
    }
    return true;
  } else {
    console.log(`❌ 学习验证失败`);
    return false;
  }
}

// CLI 入口
if (process.argv[1]?.includes('mirror-learning') || process.argv[1]?.endsWith('mirror')) {
  const [, , observer, target] = process.argv;
  
  if (!observer || !target) {
    console.log('🧠 镜像学习 - 基于镜像神经元的观察学习');
    console.log(``);
    console.log('用法：openclaw learning mirror <observer-agent> <target-agent>');
    console.log(``);
    console.log('示例：openclaw learning mirror new-ceo ceo-yiworld');
    console.log(``);
    console.log('参数:');
    console.log('  observer-agent  观察者神经元名称');
    console.log('  target-agent    目标神经元名称 (导师)');
    process.exit(1);
  }
  
  mirrorLearning(observer, target)
    .then(success => {
      process.exit(success ? 0 : 1);
    })
    .catch(error => {
      console.error(`❌ 错误：${error.message}`);
      process.exit(1);
    });
}

export { mirrorLearning, observeWorkflow, internalizeWorkflow, validateLearning, extractTopics };
