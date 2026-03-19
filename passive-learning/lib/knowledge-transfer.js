#!/usr/bin/env node

/**
 * 知识传递模块
 * 基于 Christof Koch 整合信息理论 (IIT)
 * 
 * 功能：神经元间共享记忆和技能，通过突触连接传递知识
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/**
 * 知识传递配置
 */
const TRANSFER_CONFIG = {
  maxKnowledgeTypes: 5,
  compressionLevel: 'medium',
  includeExamples: true,
};

/**
 * 提取知识
 * @param {string} fromAgent - 源神经元名称
 * @param {string} knowledgeType - 知识类型 (memory|skills|patterns|all)
 * @returns {Promise<Object>} 知识数据
 */
async function extractKnowledge(fromAgent, knowledgeType) {
  const stateDir = process.env.OPENCLAW_STATE_DIR || path.join(process.env.HOME || '~', '.openclaw');
  const agentDir = path.join(stateDir, 'agents', fromAgent);
  
  console.log(`📦 提取 ${fromAgent} 的知识：${knowledgeType}`);
  
  const knowledge = {
    type: knowledgeType,
    extractedAt: new Date().toISOString(),
    sourceAgent: fromAgent,
    data: {},
  };
  
  // 1. 提取 Memory
  if (knowledgeType === 'memory' || knowledgeType === 'all') {
    const memoryDir = path.join(stateDir, 'memory');
    const memoryFile = path.join(memoryDir, `${fromAgent}.sqlite`);
    
    try {
      await fs.access(memoryFile);
      const stats = await fs.stat(memoryFile);
      knowledge.data.memory = {
        exists: true,
        path: memoryFile,
        size: stats.size,
        lastModified: stats.mtime.toISOString(),
      };
      console.log(`   ✅ Memory: ${Math.round(stats.size / 1024)} KB`);
    } catch (error) {
      knowledge.data.memory = { exists: false };
      console.log(`   ⚠️  Memory: 不存在`);
    }
  }
  
  // 2. 提取 Skills
  if (knowledgeType === 'skills' || knowledgeType === 'all') {
    const agentAgentDir = path.join(agentDir, 'agent');
    const skills = [];
    
    // 查找技能相关文件
    try {
      const files = await fs.readdir(agentAgentDir);
      for (const file of files) {
        if (file.endsWith('.md') && file !== 'SOUL.md' && file !== 'IDENTITY.md' && file !== 'AGENTS.md') {
          const content = await fs.readFile(path.join(agentAgentDir, file), 'utf-8');
          skills.push({
            name: file.replace('.md', ''),
            content: content,
            size: content.length,
          });
        }
      }
      
      knowledge.data.skills = skills;
      console.log(`   ✅ Skills: ${skills.length} 个`);
    } catch (error) {
      knowledge.data.skills = [];
      console.log(`   ⚠️  Skills: 无法读取`);
    }
  }
  
  // 3. 提取 Sessions 模式
  if (knowledgeType === 'patterns' || knowledgeType === 'all') {
    const sessionsDir = path.join(agentDir, 'sessions');
    
    try {
      const sessions = await fs.readdir(sessionsDir);
      knowledge.data.patterns = {
        sessionCount: sessions.length,
        recentSessions: sessions.slice(-5),
        totalSize: 0, // 可以计算总大小
      };
      console.log(`   ✅ Patterns: ${sessions.length} 个 Sessions`);
    } catch (error) {
      knowledge.data.patterns = { sessionCount: 0, recentSessions: [] };
      console.log(`   ⚠️  Patterns: 无法读取`);
    }
  }
  
  console.log(`✅ 知识提取完成`);
  return knowledge;
}

/**
 * 格式化知识
 * @param {Object} knowledge - 知识数据
 * @returns {Promise<Object>} 格式化后的知识
 */
async function formatKnowledge(knowledge) {
  console.log(`📝 格式化知识...`);
  
  // 压缩知识（可选）
  const formatted = {
    ...knowledge,
    compressed: TRANSFER_CONFIG.compressionLevel !== 'none',
    formattedAt: new Date().toISOString(),
  };
  
  // 计算统计信息
  formatted.stats = {
    memorySize: knowledge.data.memory?.size || 0,
    skillCount: knowledge.data.skills?.length || 0,
    sessionCount: knowledge.data.patterns?.sessionCount || 0,
  };
  
  console.log(`   统计:`);
  console.log(`     Memory: ${Math.round(formatted.stats.memorySize / 1024)} KB`);
  console.log(`     Skills: ${formatted.stats.skillCount} 个`);
  console.log(`     Sessions: ${formatted.stats.sessionCount} 个`);
  
  return formatted;
}

/**
 * 注入知识到目标神经元
 * @param {string} toAgent - 目标神经元名称
 * @param {Object} formattedKnowledge - 格式化后的知识
 * @returns {Promise<void>}
 */
async function injectKnowledge(toAgent, formattedKnowledge) {
  const stateDir = process.env.OPENCLAW_STATE_DIR || path.join(process.env.HOME || '~', '.openclaw');
  const toAgentDir = path.join(stateDir, 'agents', toAgent);
  const learningDir = path.join(toAgentDir, 'agent', 'learning');
  
  console.log(`💉 注入知识到 ${toAgent}...`);
  
  // 创建学习目录
  await fs.mkdir(learningDir, { recursive: true });
  
  // 保存知识
  const knowledgePath = path.join(
    learningDir,
    `transferred-${formattedKnowledge.type}-${Date.now()}.json`
  );
  
  await fs.writeFile(knowledgePath, JSON.stringify(formattedKnowledge, null, 2));
  
  console.log(`   ✅ 保存到：${knowledgePath}`);
  console.log(`   ✅ 大小：${Math.round(JSON.stringify(formattedKnowledge).length / 1024)} KB`);
}

/**
 * 验证传递
 * @param {string} toAgent - 目标神经元名称
 * @returns {Promise<boolean>} 验证是否成功
 */
async function validateTransfer(toAgent) {
  const stateDir = process.env.OPENCLAW_STATE_DIR || path.join(process.env.HOME || '~', '.openclaw');
  const toAgentDir = path.join(stateDir, 'agents', toAgent);
  const learningDir = path.join(toAgentDir, 'agent', 'learning');
  
  try {
    const files = await fs.readdir(learningDir);
    const transferredFiles = files.filter(f => f.startsWith('transferred-'));
    return transferredFiles.length > 0;
  } catch (error) {
    return false;
  }
}

/**
 * 主函数：知识传递
 * @param {string} fromAgent - 源神经元
 * @param {string} toAgent - 目标神经元
 * @param {string} knowledgeType - 知识类型
 * @returns {Promise<boolean>} 传递是否成功
 */
async function transferKnowledge(fromAgent, toAgent, knowledgeType = 'all') {
  console.log(`🧠 开始知识传递：${fromAgent} → ${toAgent}`);
  console.log(`   知识类型：${knowledgeType}`);
  console.log(`   配置:`);
  console.log(`     最大类型数：${TRANSFER_CONFIG.maxKnowledgeTypes}`);
  console.log(`     压缩级别：${TRANSFER_CONFIG.compressionLevel}`);
  console.log(`     包含示例：${TRANSFER_CONFIG.includeExamples}`);
  console.log(``);
  
  // 1. 提取知识
  console.log(`📦 提取知识...`);
  const knowledge = await extractKnowledge(fromAgent, knowledgeType);
  
  // 2. 格式化
  console.log(``);
  const formatted = await formatKnowledge(knowledge);
  
  // 3. 注入
  console.log(``);
  await injectKnowledge(toAgent, formatted);
  
  // 4. 验证
  console.log(``);
  console.log(`✅ 验证传递...`);
  const validated = await validateTransfer(toAgent);
  
  if (validated) {
    console.log(``);
    console.log(`🎉 知识传递完成！`);
    console.log(`   源：${fromAgent}`);
    console.log(`   目标：${toAgent}`);
    console.log(`   类型：${knowledgeType}`);
    console.log(`   Memory: ${formatted.stats.memorySize > 0 ? '✓' : '✗'}`);
    console.log(`   Skills: ${formatted.stats.skillCount > 0 ? '✓' : '✗'}`);
    console.log(`   Patterns: ${formatted.stats.sessionCount > 0 ? '✓' : '✗'}`);
    return true;
  } else {
    console.log(``);
    console.log(`❌ 传递验证失败`);
    return false;
  }
}

// CLI 入口
if (process.argv[1]?.includes('knowledge-transfer') || process.argv[1]?.endsWith('transfer')) {
  const [, , from, to, type] = process.argv;
  
  if (!from || !to) {
    console.log('🧠 知识传递 - 基于整合信息理论的知识共享');
    console.log(``);
    console.log('用法：openclaw learning transfer <from-agent> <to-agent> [knowledge-type]');
    console.log(``);
    console.log('示例：openclaw learning transfer ceo-yiworld pm-yiworld skills');
    console.log(``);
    console.log('参数:');
    console.log('  from-agent      源神经元名称');
    console.log('  to-agent        目标神经元名称');
    console.log('  knowledge-type  知识类型 (memory|skills|patterns|all, 默认: all)');
    process.exit(1);
  }
  
  transferKnowledge(from, to, type || 'all')
    .then(success => {
      process.exit(success ? 0 : 1);
    })
    .catch(error => {
      console.error(`❌ 错误：${error.message}`);
      process.exit(1);
    });
}

export { transferKnowledge, extractKnowledge, formatKnowledge, injectKnowledge, validateTransfer };
