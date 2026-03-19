#!/usr/bin/env node

/**
 * 模板克隆模块
 * 基于 Tomaso Poggio HMAX 分层模型
 * 
 * 功能：从模板快速创建新神经元，复制结构和配置
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/**
 * 模板克隆配置
 */
const CLONE_CONFIG = {
  copyMemory: false,      // 不复制记忆
  copySkills: true,       // 复制技能
  copyIdentity: true,     // 复制身份
  resetSessions: true,    // 重置 Sessions
  learnFromSkillDir: true, // 从技能目录学习技能
};

/**
 * 技能目录路径
 */
const SKILL_DIRECTORIES = [
  path.join(process.env.HOME || '~', 'project/git/billion-people-world/skills/my-super-skills'), // 个人技能仓库 ⭐
  path.join(process.env.HOME || '~', 'project/git/billion-people-world/skills'),
  path.join(process.env.HOME || '~', '.openclaw/skills'),
];

/**
 * 加载模板
 * @param {string} templateName - 模板名称
 * @returns {Promise<Object>} 模板数据
 */
async function loadTemplate(templateName) {
  const templatesDir = path.join(__dirname, '..', 'templates');
  const templatePath = path.join(templatesDir, `${templateName}.json`);
  
  console.log(`📋 加载模板：${templateName}`);
  
  try {
    const templateContent = await fs.readFile(templatePath, 'utf-8');
    const template = JSON.parse(templateContent);
    console.log(`✅ 模板加载成功`);
    console.log(`   名称：${template.name || templateName}`);
    console.log(`   模型：${template.model || 'bailian/glm-5'}`);
    return template;
  } catch (error) {
    console.error(`❌ 模板不存在：${templateName}`);
    console.error(`   路径：${templatePath}`);
    console.error(``);
    console.log(`可用模板:`);
    
    // 列出可用模板
    try {
      const files = await fs.readdir(templatesDir);
      const templates = files.filter(f => f.endsWith('.json')).map(f => f.replace('.json', ''));
      templates.forEach(t => console.log(`  - ${t}`));
    } catch {
      console.log(`  (无可用模板)`);
    }
    
    process.exit(1);
  }
}

/**
 * 从技能目录学习技能
 * @param {string} skillName - 技能名称
 * @param {string} newAgentName - 新神经元名称
 * @returns {Promise<boolean>} 是否成功学习
 */
async function learnSkill(skillName, newAgentName) {
  const stateDir = process.env.OPENCLAW_STATE_DIR || path.join(process.env.HOME || '~', '.openclaw');
  const newAgentSkillDir = path.join(stateDir, 'agents', newAgentName, 'agent', 'skills', skillName);
  
  // 在技能目录中查找技能
  for (const skillDir of SKILL_DIRECTORIES) {
    const sourceSkillPath = path.join(skillDir, skillName);
    
    try {
      await fs.access(sourceSkillPath);
      
      // 复制技能到新神经元
      await fs.mkdir(newAgentSkillDir, { recursive: true });
      
      // 复制技能文件
      const files = await fs.readdir(sourceSkillPath);
      for (const file of files) {
        const sourceFile = path.join(sourceSkillPath, file);
        const destFile = path.join(newAgentSkillDir, file);
        
        const stats = await fs.stat(sourceFile);
        if (stats.isFile()) {
          await fs.copyFile(sourceFile, destFile);
        } else if (stats.isDirectory()) {
          await fs.cp(sourceFile, destFile, { recursive: true });
        }
      }
      
      console.log(`   ✅ 技能：${skillName}`);
      return true;
    } catch (error) {
      // 技能不在此目录，继续查找
    }
  }
  
  console.log(`   ⚠️  技能未找到：${skillName}`);
  return false;
}

/**
 * 学习模板中定义的所有技能
 * @param {Object} template - 模板数据
 * @param {string} newAgentName - 新神经元名称
 * @returns {Promise<void>}
 */
async function learnSkillsFromTemplate(template, newAgentName) {
  if (!CLONE_CONFIG.learnFromSkillDir || !template.skills) {
    return;
  }
  
  console.log(`📚 学习技能...`);
  
  const skillsDir = path.join(process.env.OPENCLAW_STATE_DIR || path.join(process.env.HOME || '~', '.openclaw'), 'agents', newAgentName, 'agent', 'skills');
  await fs.mkdir(skillsDir, { recursive: true });
  
  let learnedCount = 0;
  for (const skill of template.skills) {
    const success = await learnSkill(skill, newAgentName);
    if (success) {
      learnedCount++;
    }
  }
  
  console.log(`✅ 学习了 ${learnedCount}/${template.skills.length} 个技能`);
}

/**
 * 复制神经元结构
 * @param {Object} template - 模板数据
 * @param {string} newAgentName - 新神经元名称
 * @returns {Promise<void>}
 */
async function copyStructure(template, newAgentName) {
  const stateDir = process.env.OPENCLAW_STATE_DIR || path.join(process.env.HOME || '~', '.openclaw');
  const newAgentDir = path.join(stateDir, 'agents', newAgentName);
  const newAgentAgentDir = path.join(newAgentDir, 'agent');
  
  console.log(`🏗️  创建神经元结构...`);
  
  // 创建目录结构
  await fs.mkdir(newAgentAgentDir, { recursive: true });
  
  // 复制 SOUL.md
  if (CLONE_CONFIG.copyIdentity && template.soul) {
    await fs.writeFile(
      path.join(newAgentAgentDir, 'SOUL.md'),
      template.soul
    );
    console.log(`   ✅ SOUL.md`);
  }
  
  // 复制 IDENTITY.md
  if (CLONE_CONFIG.copyIdentity && template.identity) {
    await fs.writeFile(
      path.join(newAgentAgentDir, 'IDENTITY.md'),
      template.identity
    );
    console.log(`   ✅ IDENTITY.md`);
  }
  
  // 复制 AGENTS.md
  if (CLONE_CONFIG.copyIdentity && template.agents) {
    await fs.writeFile(
      path.join(newAgentAgentDir, 'AGENTS.md'),
      template.agents
    );
    console.log(`   ✅ AGENTS.md`);
  }
  
  // 创建 models.json
  const modelsConfig = {
    models: {
      default: template.model || 'bailian/glm-5',
    },
  };
  await fs.writeFile(
    path.join(newAgentAgentDir, 'models.json'),
    JSON.stringify(modelsConfig, null, 2)
  );
  console.log(`   ✅ models.json`);
  
  // 创建 auth-profiles.json
  const authConfig = {
    profiles: template.auth || {},
  };
  await fs.writeFile(
    path.join(newAgentAgentDir, 'auth-profiles.json'),
    JSON.stringify(authConfig, null, 2)
  );
  console.log(`   ✅ auth-profiles.json`);
  
  console.log(`✅ 神经元结构已创建：${newAgentName}`);
}

/**
 * 初始化 Memory
 * @param {string} newAgentName - 新神经元名称
 * @returns {Promise<void>}
 */
async function initializeMemory(newAgentName) {
  const stateDir = process.env.OPENCLAW_STATE_DIR || path.join(process.env.HOME || '~', '.openclaw');
  const memoryDir = path.join(stateDir, 'memory');
  
  await fs.mkdir(memoryDir, { recursive: true });
  
  // 创建空的 SQLite 数据库文件（占位符）
  const dbPath = path.join(memoryDir, `${newAgentName}.sqlite`);
  
  // 注意：实际创建 SQLite 数据库需要 sqlite3 库
  // 这里创建一个空文件作为占位符
  await fs.writeFile(dbPath, '');
  
  console.log(`💾 Memory 已初始化：${newAgentName}.sqlite`);
}

/**
 * 激活新神经元
 * @param {string} newAgentName - 新神经元名称
 * @returns {Promise<boolean>} 激活是否成功
 */
async function activateAgent(newAgentName) {
  console.log(`🚀 激活神经元：${newAgentName}`);
  
  // 验证神经元配置
  const stateDir = process.env.OPENCLAW_STATE_DIR || path.join(process.env.HOME || '~', '.openclaw');
  const agentDir = path.join(stateDir, 'agents', newAgentName);
  
  const requiredFiles = [
    'agent/SOUL.md',
    'agent/IDENTITY.md',
    'agent/models.json',
  ];
  
  let allPresent = true;
  for (const file of requiredFiles) {
    try {
      await fs.access(path.join(agentDir, file));
    } catch (error) {
      console.error(`❌ 缺少必需文件：${file}`);
      allPresent = false;
    }
  }
  
  if (allPresent) {
    console.log(`✅ 神经元 ${newAgentName} 已激活！`);
    return true;
  } else {
    console.log(`❌ 激活失败：缺少必需文件`);
    return false;
  }
}

/**
 * 主函数：模板克隆
 * @param {string} templateName - 模板名称
 * @param {string} newAgentName - 新神经元名称
 * @returns {Promise<boolean>} 克隆是否成功
 */
async function cloneFromTemplate(templateName, newAgentName) {
  console.log(`🧬 开始模板克隆：${templateName} → ${newAgentName}`);
  console.log(`   配置:`);
  console.log(`     复制记忆：${CLONE_CONFIG.copyMemory}`);
  console.log(`     复制技能：${CLONE_CONFIG.copySkills}`);
  console.log(`     复制身份：${CLONE_CONFIG.copyIdentity}`);
  console.log(`     重置 Sessions: ${CLONE_CONFIG.resetSessions}`);
  console.log(``);
  
  // 1. 加载模板
  const template = await loadTemplate(templateName);
  
  // 2. 复制结构
  console.log(``);
  await copyStructure(template, newAgentName);
  
  // 3. 学习技能
  console.log(``);
  await learnSkillsFromTemplate(template, newAgentName);
  
  // 4. 初始化 Memory
  if (CLONE_CONFIG.copyMemory) {
    console.log(``);
    await initializeMemory(newAgentName);
  }
  
  // 5. 激活新神经元
  console.log(``);
  const activated = await activateAgent(newAgentName);
  
  if (activated) {
    console.log(``);
    console.log(`🎉 模板克隆完成！`);
    console.log(`   新神经元：${newAgentName}`);
    console.log(`   模板：${templateName}`);
    console.log(`   模型：${template.model || 'bailian/glm-5'}`);
    return true;
  } else {
    console.log(``);
    console.log(`❌ 激活失败`);
    return false;
  }
}

// CLI 入口
if (process.argv[1]?.includes('template-clone') || process.argv[1]?.endsWith('clone')) {
  const [, , template, newName] = process.argv;
  
  if (!template || !newName) {
    console.log('🧬 模板克隆 - 基于 HMAX 模型的分层复制');
    console.log(``);
    console.log('用法：openclaw learning clone <template> <new-agent-name>');
    console.log(``);
    console.log('示例：openclaw learning clone software-dev software-dev-1');
    console.log(``);
    console.log('参数:');
    console.log('  template         模板名称');
    console.log('  new-agent-name   新神经元名称');
    process.exit(1);
  }
  
  cloneFromTemplate(template, newName)
    .then(success => {
      process.exit(success ? 0 : 1);
    })
    .catch(error => {
      console.error(`❌ 错误：${error.message}`);
      process.exit(1);
    });
}

export { cloneFromTemplate, loadTemplate, copyStructure, initializeMemory, activateAgent };
