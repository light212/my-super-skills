"""
Super-Learning API

FastAPI 接口，供 OpenClaw JavaScript 层调用
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio

from .core.evolution_engine import SelfEvolutionEngine, LearningStrategy
from .core.auto_detector import LearningOpportunityDetector, LearningOpportunity


app = FastAPI(
    title="Super-Learning API",
    description="自我进化学习系统",
    version="2.0.0",
)

# CORS 中间件（允许 JavaScript 调用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============ 数据模型 ============

class EvolutionRequest(BaseModel):
    """进化请求"""
    population_size: int = 50
    generations: int = 20
    initial_strategies: Optional[List[Dict]] = None


class EvolutionResponse(BaseModel):
    """进化响应"""
    best_strategy: Dict
    generations: int
    history: List[Dict]


class DetectionRequest(BaseModel):
    """检测请求"""
    event: str
    context: Dict[str, Any]


class DetectionResponse(BaseModel):
    """检测响应"""
    opportunity: Optional[Dict]
    message: str


class OptimizeRequest(BaseModel):
    """优化请求"""
    current_strategy: Dict
    performance_data: Dict[str, float]


class OptimizeResponse(BaseModel):
    """优化响应"""
    optimized_strategy: Dict
    improvements: Dict[str, float]


# ============ 全局状态 ============

evolution_engine: Optional[SelfEvolutionEngine] = None
detector: Optional[LearningOpportunityDetector] = None


@app.on_event("startup")
async def startup_event():
    """启动时初始化"""
    global evolution_engine, detector
    
    evolution_engine = SelfEvolutionEngine(
        population_size=50,
        generations=20
    )
    
    detector = LearningOpportunityDetector()
    
    print("🚀 Super-Learning API 启动完成")


# ============ API 接口 ============

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Super-Learning API",
        "version": "2.0.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "evolution_engine": "ready" if evolution_engine else "not_initialized",
        "detector": "ready" if detector else "not_initialized",
    }


@app.post("/evolve", response_model=EvolutionResponse)
async def evolve(request: EvolutionRequest):
    """
    执行进化
    
    使用遗传算法优化学习策略
    """
    if not evolution_engine:
        raise HTTPException(status_code=503, detail="Evolution engine not initialized")
    
    # 转换初始策略
    initial_strategies = None
    if request.initial_strategies:
        initial_strategies = [
            LearningStrategy(**strategy)
            for strategy in request.initial_strategies
        ]
    
    # 执行进化（在后台线程中运行，避免阻塞）
    loop = asyncio.get_event_loop()
    best_strategy = await loop.run_in_executor(
        None,
        lambda: evolution_engine.evolve(initial_strategies)
    )
    
    # 返回结果
    return EvolutionResponse(
        best_strategy={
            "id": best_strategy.id,
            "learning_rate": best_strategy.learning_rate,
            "transfer_frequency": best_strategy.transfer_frequency,
            "detection_threshold": best_strategy.detection_threshold,
            "mirror_weight": best_strategy.mirror_weight,
            "clone_weight": best_strategy.clone_weight,
            "transfer_weight": best_strategy.transfer_weight,
        },
        generations=evolution_engine.current_generation,
        history=evolution_engine.get_evolution_history()[-10:],  # 最近 10 代
    )


@app.post("/detect", response_model=DetectionResponse)
async def detect(request: DetectionRequest):
    """
    检测学习机会
    
    自动检测各种学习机会
    """
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not initialized")
    
    # 检测机会
    opportunity = await detector.detect(request.context)
    
    if opportunity:
        return DetectionResponse(
            opportunity={
                "type": opportunity.type,
                "confidence": opportunity.confidence,
                "agents": opportunity.agents,
                "context": opportunity.context,
                "action": opportunity.action,
                "timestamp": opportunity.timestamp,
            },
            message=f"检测到 {opportunity.type} 机会",
        )
    else:
        return DetectionResponse(
            opportunity=None,
            message="未检测到学习机会",
        )


@app.post("/record")
async def record_history(request: DetectionRequest):
    """
    记录历史
    
    用于模式学习
    """
    if not detector:
        raise HTTPException(status_code=503, detail="Detector not initialized")
    
    detector.record_history(request.context)
    
    return {
        "status": "recorded",
        "history_size": len(detector.history),
    }


@app.post("/optimize", response_model=OptimizeResponse)
async def optimize(request: OptimizeRequest):
    """
    优化策略
    
    基于性能数据优化当前策略
    """
    if not evolution_engine:
        raise HTTPException(status_code=503, detail="Evolution engine not initialized")
    
    # 简化实现：基于性能数据调整策略
    current = request.current_strategy
    performance = request.performance_data
    
    # 计算改进
    improvements = {}
    
    if performance.get("learning_speed", 0) < 0.5:
        improvements["learning_rate"] = min(1.0, current.get("learning_rate", 0.5) + 0.1)
    
    if performance.get("transfer_efficiency", 0) < 0.5:
        improvements["transfer_frequency"] = min(1.0, current.get("transfer_frequency", 0.5) + 0.1)
    
    if performance.get("adaptation_speed", 0) < 0.5:
        improvements["detection_threshold"] = max(0.0, current.get("detection_threshold", 0.5) - 0.1)
    
    # 应用改进
    optimized = {**current, **improvements}
    
    return OptimizeResponse(
        optimized_strategy=optimized,
        improvements=improvements,
    )


@app.get("/strategies")
async def list_strategies():
    """列出所有策略"""
    if not evolution_engine:
        return {"strategies": []}
    
    history = evolution_engine.get_evolution_history()
    
    strategies = []
    for record in history:
        strategies.append({
            "generation": record["generation"],
            "fitness": record["best_fitness"],
            "timestamp": record["timestamp"],
        })
    
    return {
        "strategies": strategies,
        "total": len(strategies),
    }


@app.get("/strategies/{strategy_id}")
async def get_strategy(strategy_id: str):
    """获取特定策略"""
    if not evolution_engine:
        raise HTTPException(status_code=503, detail="Evolution engine not initialized")
    
    history = evolution_engine.get_evolution_history()
    
    for record in history:
        if record.get("id") == strategy_id or f"gen_{record['generation']}" == strategy_id:
            return {
                "strategy": record,
            }
    
    raise HTTPException(status_code=404, detail="Strategy not found")


# ============ 斡旋造化接口 ============

@app.post("/synergy/create")
async def create_synergy(agents: List[str]):
    """
    创造群体智能
    
    协调多个 Agent，创造新能力
    """
    # TODO: 实现斡旋造化引擎
    return {
        "status": "created",
        "synergy_id": f"synergy_{len(agents)}",
        "agents": agents,
        "message": f"创建了 {len(agents)} 个 Agent 的协同网络",
    }


@app.post("/synergy/mediate")
async def mediate_conflict(agents: List[str], conflict: Dict):
    """
    调解冲突
    
    斡旋多个 Agent 之间的冲突
    """
    # TODO: 实现冲突调解
    return {
        "status": "mediated",
        "solution": "compromise",
        "message": "冲突已调解",
    }


# ============ 元学习接口 ============

@app.post("/meta/learn")
async def meta_learn(agent_id: str):
    """
    元学习
    
    学习如何学习，生成个性化策略
    """
    # TODO: 实现元学习
    return {
        "status": "learned",
        "strategy": {
            "methods": ["mirror", "clone"],
            "timing": "morning",
            "sequence": ["basic", "advanced"],
        },
        "message": f"为 {agent_id} 生成了个性化学习策略",
    }


@app.post("/meta/transfer")
async def transfer_learning(source_agent: str, target_agent: str):
    """
    跨 Agent 知识迁移
    """
    # TODO: 实现知识迁移
    return {
        "status": "transferred",
        "source": source_agent,
        "target": target_agent,
        "knowledge_items": 5,
        "message": f"知识从 {source_agent} 迁移到 {target_agent}",
    }


# ============ 主函数 ============

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 启动 Super-Learning API...")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
