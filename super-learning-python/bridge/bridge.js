/**
 * JavaScript ↔ Python 桥接层
 
 让 OpenClaw JavaScript 层调用 Python Super-Learning 服务
 */

const PYTHON_API_URL = process.env.SUPER_LEARNING_URL || 'http://localhost:8000';

/**
 * 调用 Python API
 */
async function callPython(action, params = {}) {
  try {
    const response = await fetch(`${PYTHON_API_URL}/${action}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(params),
    });
    
    if (!response.ok) {
      throw new Error(`Python API error: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('[SuperLearning] Python API call failed:', error);
    throw error;
  }
}

/**
 * 执行进化
 */
export async function evolve(populationSize = 50, generations = 20) {
  return await callPython('evolve', {
    population_size: populationSize,
    generations: generations,
  });
}

/**
 * 检测学习机会
 */
export async function detectLearningOpportunity(event, context) {
  return await callPython('detect', {
    event: event,
    context: context,
  });
}

/**
 * 优化策略
 */
export async function optimizeStrategy(currentStrategy, performanceData) {
  return await callPython('optimize', {
    current_strategy: currentStrategy,
    performance_data: performanceData,
  });
}

/**
 * 记录历史
 */
export async function recordHistory(event, context) {
  return await callPython('record', {
    event: event,
    context: context,
  });
}

/**
 * 创造协同网络
 */
export async function createSynergy(agents) {
  return await callPython('synergy/create', {
    agents: agents,
  });
}

/**
 * 调解冲突
 */
export async function mediateConflict(agents, conflict) {
  return await callPython('synergy/mediate', {
    agents: agents,
    conflict: conflict,
  });
}

/**
 * 元学习 - 生成个性化策略
 */
export async function metaLearn(agentId) {
  return await callPython('meta/learn', {
    agent_id: agentId,
  });
}

/**
 * 元学习 - 知识迁移
 */
export async function transferLearning(sourceAgent, targetAgent) {
  return await callPython('meta/transfer', {
    source_agent: sourceAgent,
    target_agent: targetAgent,
  });
}

/**
 * 健康检查
 */
export async function healthCheck() {
  try {
    const response = await fetch(`${PYTHON_API_URL}/health`);
    return await response.json();
  } catch (error) {
    console.error('[SuperLearning] Health check failed:', error);
    return { status: 'unhealthy', error: error.message };
  }
}

/**
 * 获取策略列表
 */
export async function listStrategies() {
  return await callPython('strategies');
}

/**
 * 初始化桥接层
 */
export async function initialize() {
  console.log('[SuperLearning] Initializing bridge...');
  
  // 健康检查
  const health = await healthCheck();
  
  if (health.status === 'healthy') {
    console.log('[SuperLearning] Python service is ready');
    console.log('  - Evolution engine:', health.evolution_engine);
    console.log('  - Detector:', health.detector);
    return true;
  } else {
    console.error('[SuperLearning] Python service is not ready');
    return false;
  }
}

// 使用示例
if (typeof window !== 'undefined') {
  // 浏览器环境
  window.SuperLearning = {
    evolve,
    detectLearningOpportunity,
    optimizeStrategy,
    recordHistory,
    createSynergy,
    mediateConflict,
    metaLearn,
    transferLearning,
    healthCheck,
    listStrategies,
    initialize,
  };
}
