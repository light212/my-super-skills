"""
自动检测器

自动检测学习机会：
- 新 Agent 创建
- 协作机会
- 知识缺口
- 模式识别
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LearningOpportunity:
    """学习机会"""
    type: str  # clone, mirror, transfer, learn, optimize
    confidence: float  # 置信度 0-1
    agents: List[str]  # 涉及的 Agent
    context: Dict[str, Any]  # 上下文信息
    action: str  # 建议动作
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class LearningOpportunityDetector:
    """
    学习机会检测器
    
    自动检测各种学习机会
    """
    
    def __init__(self):
        self.detectors = [
            self.detect_new_agent,
            self.detect_collaboration,
            self.detect_knowledge_gap,
            self.detect_pattern,
            self.detect_stagnation,
        ]
        
        # 历史模式
        self.history: List[Dict] = []
    
    async def detect(self, context: Dict[str, Any]) -> Optional[LearningOpportunity]:
        """
        检测学习机会
        
        Args:
            context: 上下文信息
        
        Returns:
            学习机会，如果没有则返回 None
        """
        for detector in self.detectors:
            opportunity = await detector(context)
            if opportunity:
                return opportunity
        
        return None
    
    async def detect_new_agent(self, context: Dict) -> Optional[LearningOpportunity]:
        """
        检测新 Agent 创建
        
        当新 Agent 创建时，建议自动克隆模板
        """
        if context.get("event") == "agent.created":
            agent = context.get("agent", {})
            agent_name = agent.get("name", "")
            agent_role = agent.get("role", "")
            
            # 检测是否已有成熟 Agent
            existing_agents = context.get("existing_agents", [])
            similar_agents = [
                a for a in existing_agents
                if a.get("role") == agent_role
            ]
            
            if similar_agents:
                # 建议从相似 Agent 克隆
                return LearningOpportunity(
                    type="clone",
                    confidence=0.9,
                    agents=[agent_name],
                    context={
                        "template": similar_agents[0]["name"],
                        "role": agent_role,
                    },
                    action=f"clone {similar_agents[0]['name']} to {agent_name}",
                )
            else:
                # 建议从模板克隆
                return LearningOpportunity(
                    type="clone",
                    confidence=0.8,
                    agents=[agent_name],
                    context={
                        "template": self._map_role_to_template(agent_role),
                        "role": agent_role,
                    },
                    action=f"clone template to {agent_name}",
                )
        
        return None
    
    async def detect_collaboration(self, context: Dict) -> Optional[LearningOpportunity]:
        """
        检测协作机会
        
        当多个 Agent 互动时，建议知识传递
        """
        if context.get("event") == "agents.interacted":
            agents = context.get("agents", [])
            
            if len(agents) >= 2:
                # 分析能力互补性
                complementarities = self._analyze_complementarities(agents)
                
                if complementarities:
                    return LearningOpportunity(
                        type="transfer",
                        confidence=0.7,
                        agents=[a["name"] for a in agents],
                        context={
                            "complementarities": complementarities,
                        },
                        action=f"transfer knowledge between {', '.join([a['name'] for a in agents])}",
                    )
        
        return None
    
    async def detect_knowledge_gap(self, context: Dict) -> Optional[LearningOpportunity]:
        """
        检测知识缺口
        
        当 Agent 缺少必要技能时，建议学习
        """
        if context.get("event") == "agent.assigned_task":
            agent = context.get("agent", {})
            required_skills = context.get("required_skills", [])
            agent_skills = agent.get("skills", [])
            
            missing_skills = [
                skill for skill in required_skills
                if skill not in agent_skills
            ]
            
            if missing_skills:
                return LearningOpportunity(
                    type="learn",
                    confidence=0.8,
                    agents=[agent.get("name", "")],
                    context={
                        "missing_skills": missing_skills,
                        "task": context.get("task", {}),
                    },
                    action=f"teach {agent.get('name')} skills: {', '.join(missing_skills)}",
                )
        
        return None
    
    async def detect_pattern(self, context: Dict) -> Optional[LearningOpportunity]:
        """
        检测模式
        
        从历史中学习模式，建议优化
        """
        # 分析历史数据
        if len(self.history) >= 10:
            patterns = self._analyze_patterns()
            
            if patterns:
                return LearningOpportunity(
                    type="optimize",
                    confidence=0.6,
                    agents=[],
                    context={
                        "patterns": patterns,
                    },
                    action=f"optimize strategy based on patterns",
                )
        
        return None
    
    async def detect_stagnation(self, context: Dict) -> Optional[LearningOpportunity]:
        """
        检测停滞
        
        当 Agent 长时间没有进步时，建议新的学习策略
        """
        if context.get("event") == "agent.performance_review":
            agent = context.get("agent", {})
            performance_history = agent.get("performance_history", [])
            
            if len(performance_history) >= 5:
                # 检测是否停滞
                recent_scores = performance_history[-5:]
                if max(recent_scores) - min(recent_scores) < 0.05:
                    return LearningOpportunity(
                        type="optimize",
                        confidence=0.7,
                        agents=[agent.get("name", "")],
                        context={
                            "stagnation": True,
                            "recent_scores": recent_scores,
                        },
                        action=f"try new learning strategy for {agent.get('name')}",
                    )
        
        return None
    
    def _map_role_to_template(self, role: str) -> str:
        """将角色映射到模板"""
        mapping = {
            "CEO": "ceo",
            "PM": "product-mgr",
            "FE": "fullstack-developer",
            "BE": "software-dev",
            "QA": "software-dev",
            "DESIGNER": "product-designer",
        }
        return mapping.get(role, "software-dev")
    
    def _analyze_complementarities(self, agents: List[Dict]) -> List[Dict]:
        """分析 Agent 之间的互补性"""
        complementarities = []
        
        for i, agent1 in enumerate(agents):
            for agent2 in agents[i+1:]:
                skills1 = set(agent1.get("skills", []))
                skills2 = set(agent2.get("skills", []))
                
                # 找出互补的技能
                gaps1 = skills2 - skills1
                gaps2 = skills1 - skills2
                
                if gaps1 or gaps2:
                    complementarities.append({
                        "agents": [agent1["name"], agent2["name"]],
                        "gaps": list(gaps1 | gaps2),
                        "potential": len(gaps1 | gaps2) / max(len(skills1), len(skills2), 1),
                    })
        
        return sorted(complementarities, key=lambda x: x["potential"], reverse=True)
    
    def _analyze_patterns(self) -> List[Dict]:
        """分析历史模式"""
        # 简化实现
        # 实际应该用机器学习算法
        return [
            {
                "type": "time_pattern",
                "description": "早晨学习效果更好",
                "confidence": 0.7,
            },
            {
                "type": "strategy_pattern",
                "description": "镜像学习比克隆学习更有效",
                "confidence": 0.6,
            },
        ]
    
    def record_history(self, event: Dict):
        """记录历史"""
        self.history.append({
            "event": event,
            "timestamp": datetime.now().isoformat(),
        })
        
        # 保留最近 100 条记录
        if len(self.history) > 100:
            self.history = self.history[-100:]
