"""
Super-Learning 测试用例
"""

import pytest
import asyncio
from core.evolution_engine import SelfEvolutionEngine, LearningStrategy
from core.auto_detector import LearningOpportunityDetector


class TestEvolutionEngine:
    """测试进化引擎"""
    
    def test_engine_initialization(self):
        """测试引擎初始化"""
        engine = SelfEvolutionEngine(population_size=10, generations=5)
        
        assert engine.population_size == 10
        assert engine.generations == 5
        assert engine.toolbox is not None
    
    def test_evolution(self):
        """测试进化过程"""
        engine = SelfEvolutionEngine(population_size=10, generations=2)  # 减少代数加快测试
        best_strategy = engine.evolve()
        
        assert best_strategy is not None
        assert hasattr(best_strategy, 'learning_rate')
    
    def test_evolution_history(self):
        """测试进化历史"""
        engine = SelfEvolutionEngine(population_size=10, generations=2)  # 减少代数
        engine.evolve()
        
        history = engine.get_evolution_history()
        
        assert len(history) >= 1  # 至少有 1 代
        assert 'generation' in history[0]


class TestAutoDetector:
    """测试自动检测器"""
    
    @pytest.mark.asyncio
    async def test_detect_new_agent(self):
        """测试新 Agent 检测"""
        detector = LearningOpportunityDetector()
        
        context = {
            'event': 'agent.created',
            'agent': {'name': 'ceo-2', 'role': 'CEO'},
            'existing_agents': [
                {'name': 'ceo-1', 'role': 'CEO'},
            ],
        }
        
        opportunity = await detector.detect(context)
        
        assert opportunity is not None
        assert opportunity.type == 'clone'
        assert opportunity.confidence > 0.5
    
    @pytest.mark.asyncio
    async def test_detect_collaboration(self):
        """测试协作检测"""
        detector = LearningOpportunityDetector()
        
        context = {
            'event': 'agents.interacted',
            'agents': [
                {'name': 'ceo-1', 'skills': ['leadership']},
                {'name': 'pm-1', 'skills': ['planning']},
            ],
        }
        
        opportunity = await detector.detect(context)
        
        assert opportunity is not None
        assert opportunity.type == 'transfer'
    
    @pytest.mark.asyncio
    async def test_detect_knowledge_gap(self):
        """测试知识缺口检测"""
        detector = LearningOpportunityDetector()
        
        context = {
            'event': 'agent.assigned_task',
            'agent': {'name': 'dev-1', 'skills': ['coding']},
            'required_skills': ['coding', 'architecture', 'testing'],
            'task': {'name': 'Build API'},
        }
        
        opportunity = await detector.detect(context)
        
        assert opportunity is not None
        assert opportunity.type == 'learn'
    
    def test_record_history(self):
        """测试历史记录"""
        detector = LearningOpportunityDetector()
        
        detector.record_history({'event': 'test'})
        
        assert len(detector.history) == 1
        assert detector.history[0]['event'] == {'event': 'test'}


class TestIntegration:
    """集成测试"""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """测试完整工作流"""
        # 1. 创建进化引擎
        engine = SelfEvolutionEngine(population_size=10, generations=3)
        
        # 2. 进化最优策略
        best_strategy = engine.evolve()
        
        # 3. 创建检测器
        detector = LearningOpportunityDetector()
        
        # 4. 检测机会
        context = {
            'event': 'agent.created',
            'agent': {'name': 'ceo-2', 'role': 'CEO'},
        }
        
        opportunity = await detector.detect(context)
        
        # 5. 验证
        assert best_strategy is not None
        assert opportunity is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
