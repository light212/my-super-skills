#!/usr/bin/env ts-node
/**
 * 进化决策引擎
 * 
 * 核心功能:
 * - 聚合三层学习信号
 * - 计算优先级
 * - 决策：立即行动 / 计划优化 / 记录审查
 * - 记录进化历史
 */

import { appendFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

/**
 * 获取进化日志路径
 * 支持环境变量配置或默认路径
 */
function getEvolutionLogPath(): string {
  // 优先使用环境变量
  if (process.env.OPENCLAW_STATE_DIR) {
    return join(process.env.OPENCLAW_STATE_DIR, 'skills/super-learning/references/evolution-history.md');
  }
  
  // 使用脚本所在目录的 references 目录
  const scriptDir = __dirname;
  const referencesDir = join(scriptDir, '..', 'references');
  
  // 确保目录存在
  if (!existsSync(referencesDir)) {
    mkdirSync(referencesDir, { recursive: true });
  }
  
  return join(referencesDir, 'evolution-history.md');
}

const EVOLUTION_LOG_PATH = getEvolutionLogPath();

interface EvolutionSignal {
  layer: 'L1' | 'L2' | 'L3';
  type: 'correction' | 'pattern' | 'optimization';
  priority: 'critical' | 'high' | 'medium' | 'low';
  description: string;
  suggestedAction: string;
}

interface EvolutionDecision {
  timestamp: string;
  signals: EvolutionSignal[];
  decision: 'immediate' | 'scheduled' | 'logged';
  action: string;
  result?: string;
}

/**
 * 验证信号格式
 */
export function validateSignal(signal: any): signal is EvolutionSignal {
  const validLayers = ['L1', 'L2', 'L3'];
  const validTypes = ['correction', 'pattern', 'optimization'];
  const validPriorities = ['critical', 'high', 'medium', 'low'];
  
  return signal &&
    typeof signal === 'object' &&
    validLayers.includes(signal.layer) &&
    validTypes.includes(signal.type) &&
    validPriorities.includes(signal.priority) &&
    typeof signal.description === 'string' &&
    typeof signal.suggestedAction === 'string';
}

/**
 * 验证决策格式
 */
export function validateDecision(decision: any): decision is EvolutionDecision {
  const validDecisions = ['immediate', 'scheduled', 'logged'];
  
  return decision &&
    typeof decision === 'object' &&
    typeof decision.timestamp === 'string' &&
    Array.isArray(decision.signals) &&
    decision.signals.every(validateSignal) &&
    validDecisions.includes(decision.decision) &&
    typeof decision.action === 'string';
}

/**
 * 聚合所有学习信号
 */
export function gatherSignals(): EvolutionSignal[] {
  const signals: EvolutionSignal[] = [];
  
  try {
    // L1 信号：用户层学习
    try {
      const l1Signals = gatherL1Signals();
      signals.push(...l1Signals);
    } catch (error) {
      console.error('[EvolutionEngine] Failed to gather L1 signals:', error);
    }
    
    // L2 信号：技能层学习
    try {
      const l2Signals = gatherL2Signals();
      signals.push(...l2Signals);
    } catch (error) {
      console.error('[EvolutionEngine] Failed to gather L2 signals:', error);
    }
    
    // L3 信号：系统层学习
    try {
      const l3Signals = gatherL3Signals();
      signals.push(...l3Signals);
    } catch (error) {
      console.error('[EvolutionEngine] Failed to gather L3 signals:', error);
    }
  } catch (error) {
    console.error('[EvolutionEngine] Critical error in gatherSignals:', error);
  }
  
  return signals;
}

/**
 * 收集 L1 用户层信号
 */
function gatherL1Signals(): EvolutionSignal[] {
  // TODO: 从 L1 学习模块收集信号
  return [];
}

/**
 * 收集 L2 技能层信号
 */
function gatherL2Signals(): EvolutionSignal[] {
  // TODO: 从 L2 学习模块收集信号
  return [];
}

/**
 * 收集 L3 系统层信号
 */
function gatherL3Signals(): EvolutionSignal[] {
  // TODO: 从 L3 学习模块收集信号
  return [];
}

/**
 * 计算优先级
 */
export function calculatePriority(signals: EvolutionSignal[]): EvolutionDecision {
  // 验证并过滤信号
  const validSignals = signals.filter(signal => {
    if (!validateSignal(signal)) {
      console.warn('[EvolutionEngine] Invalid signal filtered:', signal);
      return false;
    }
    return true;
  });
  
  const critical = validSignals.filter(s => s.priority === 'critical');
  const high = validSignals.filter(s => s.priority === 'high');
  
  if (critical.length > 0) {
    return {
      timestamp: new Date().toISOString(),
      signals: validSignals,
      decision: 'immediate',
      action: '立即处理关键信号',
    };
  }
  
  if (high.length > 0) {
    return {
      timestamp: new Date().toISOString(),
      signals: validSignals,
      decision: 'scheduled',
      action: '计划优化高优先级项',
    };
  }
  
  return {
    timestamp: new Date().toISOString(),
    signals,
    decision: 'logged',
    action: '记录待审查',
  };
}

/**
 * 执行决策
 */
export async function executeDecision(decision: EvolutionDecision): Promise<string> {
  try {
    switch (decision.decision) {
      case 'immediate':
        // 立即行动（需用户确认）
        console.log('[EvolutionEngine] Executing immediate action:', decision.action);
        return '已执行紧急优化';
      
      case 'scheduled':
        // 加入计划队列
        console.log('[EvolutionEngine] Scheduling optimization:', decision.action);
        return '已加入优化队列';
      
      case 'logged':
        // 仅记录
        console.log('[EvolutionEngine] Logging for review:', decision.action);
        return '已记录待审查';
      
      default:
        console.warn('[EvolutionEngine] Unknown decision type:', decision.decision);
        return '未知决策类型';
    }
  } catch (error) {
    console.error('[EvolutionEngine] Failed to execute decision:', error);
    throw error;
  }
}

/**
 * 记录进化历史
 */
export function logEvolution(decision: EvolutionDecision, result: string) {
  try {
    const entry = `
## ${decision.timestamp}

**决策**: ${decision.decision}
**行动**: ${decision.action}
**结果**: ${result}

### 信号来源
${decision.signals.map(s => `- [${s.layer}] ${s.type}: ${s.description}`).join('\n')}

---
`;
    
    // 确保文件存在
    const logDir = dirname(EVOLUTION_LOG_PATH);
    if (!existsSync(logDir)) {
      mkdirSync(logDir, { recursive: true });
    }
    
    appendFileSync(EVOLUTION_LOG_PATH, entry, 'utf-8');
    console.log('[EvolutionEngine] Logged evolution to:', EVOLUTION_LOG_PATH);
  } catch (error) {
    console.error('[EvolutionEngine] Failed to log evolution:', error);
    throw error;
  }
}

/**
 * 主进化循环
 */
export async function evolutionCycle() {
  console.log('🧬 启动进化循环...');
  
  const signals = gatherSignals();
  console.log(`收集到 ${signals.length} 个信号`);
  
  const decision = calculatePriority(signals);
  console.log(`决策：${decision.decision}`);
  
  const result = await executeDecision(decision);
  console.log(`结果：${result}`);
  
  logEvolution(decision, result);
  console.log('✅ 进化循环完成');
  
  return result;
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.includes('--run')) {
    evolutionCycle().catch(console.error);
  }
  
  if (args.includes('--check')) {
    console.log('🧬 Evolution Engine - Check Mode');
    const signals = gatherSignals();
    if (signals.length > 0) {
      console.log(`发现 ${signals.length} 个进化信号`);
      signals.forEach(s => console.log(`  [${s.priority}] ${s.description}`));
    } else {
      console.log('无进化信号');
    }
  }
}
