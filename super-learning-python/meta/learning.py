"""
元学习模块

学习如何学习，生成个性化策略
"""

import random
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LearningStrategy:
    """学习策略"""
    methods: List[str]
    timing: str
    sequence: List[str]
    personalized: bool = False


@dataclass
class KnowledgeTransfer:
    """知识迁移"""
    source: str
    target: str
    knowledge_items: List[Dict]
    efficiency: float


class MetaLearner:
    """
    元学习器
    
    学习如何学习，生成个性化策略
    """
    
    def __init__(self):
        self.learning_histories: Dict[str, List[Dict]] = {}
        self.strategies: Dict[str, LearningStrategy] = {}
        self.transfer_history: List[KnowledgeTransfer] = []
    
    async def learn_how_to_learn(self, agent: Dict) -> LearningStrategy:
        """
        学习如何学习
        
        为 Agent 生成个性化学习策略
        
        Args:
            agent: Agent 信息
        
        Returns:
            个性化学习策略
        """
        agent_id = agent.get('id', 'unknown')
        
        # 1. 分析历史学习效果
        history = self.learning_histories.get(agent_id, [])
        
        if history:
            effective_methods = self._analyze_effective_methods(history)
            optimal_timing = self._analyze_optimal_timing(history)
            best_sequence = self._analyze_best_sequence(history)
        else:
            # 没有历史数据，使用默认策略
            effective_methods = ['mirror', 'clone']
            optimal_timing = 'morning'
            best_sequence = ['basic', 'advanced']
        
        # 2. 生成个性化策略
        strategy = LearningStrategy(
            methods=effective_methods,
            timing=optimal_timing,
            sequence=best_sequence,
            personalized=True,
        )
        
        self.strategies[agent_id] = strategy
        
        print(f"🧠 元学习：为 {agent_id} 生成了个性化学习策略")
        print(f"   方法：{effective_methods}")
        print(f"   时机：{optimal_timing}")
        print(f"   顺序：{best_sequence}")
        
        return strategy
    
    async def transfer_learning(
        self,
        source_agent: Dict,
        target_agent: Dict,
    ) -> KnowledgeTransfer:
        """
        跨 Agent 知识迁移
        
        Args:
            source_agent: 源 Agent
            target_agent: 目标 Agent
        
        Returns:
            知识迁移结果
        """
        # 1. 分析源 Agent 的知识结构
        source_knowledge = self._analyze_knowledge_structure(source_agent)
        
        # 2. 分析目标 Agent 的知识缺口
        target_gaps = self._analyze_knowledge_gaps(target_agent)
        
        # 3. 识别可迁移的知识
        transferable = self._identify_transferable(source_knowledge, target_gaps)
        
        # 4. 优化迁移顺序
        sequence = self._optimize_transfer_sequence(transferable)
        
        # 5. 执行迁移
        transferred = []
        for knowledge in sequence:
            # 模拟知识迁移
            transferred.append({
                'type': knowledge['type'],
                'from': source_agent.get('name', ''),
                'to': target_agent.get('name', ''),
            })
        
        # 6. 记录迁移历史
        transfer = KnowledgeTransfer(
            source=source_agent.get('name', ''),
            target=target_agent.get('name', ''),
            knowledge_items=transferred,
            efficiency=len(transferred) / max(len(transferable), 1),
        )
        
        self.transfer_history.append(transfer)
        
        print(f"🔄 跨 Agent 知识迁移完成")
        print(f"   从 {transfer.source} 到 {transfer.target}")
        print(f"   迁移 {len(transfer.knowledge_items)} 项知识")
        print(f"   效率：{transfer.efficiency:.2%}")
        
        return transfer
    
    def record_learning_experience(
        self,
        agent_id: str,
        method: str,
        result: Dict,
    ):
        """
        记录学习经验
        
        用于后续分析
        """
        if agent_id not in self.learning_histories:
            self.learning_histories[agent_id] = []
        
        self.learning_histories[agent_id].append({
            'method': method,
            'result': result,
            'timestamp': datetime.now().isoformat(),
        })
        
        # 保留最近 100 条记录
        if len(self.learning_histories[agent_id]) > 100:
            self.learning_histories[agent_id] = self.learning_histories[agent_id][-100:]
    
    def _analyze_effective_methods(self, history: List[Dict]) -> List[str]:
        """分析有效的学习方法"""
        method_scores = {}
        
        for record in history:
            method = record.get('method', 'unknown')
            score = record.get('result', {}).get('score', 0.5)
            
            if method not in method_scores:
                method_scores[method] = []
            
            method_scores[method].append(score)
        
        # 计算平均得分
        method_averages = {
            method: sum(scores) / len(scores)
            for method, scores in method_scores.items()
        }
        
        # 选择得分最高的方法
        sorted_methods = sorted(
            method_averages.items(),
            key=lambda x: x[1],
            reverse=True,
        )
        
        # 返回前 3 个方法
        return [method for method, _ in sorted_methods[:3]]
    
    def _analyze_optimal_timing(self, history: List[Dict]) -> str:
        """分析最佳学习时机"""
        # 简化实现
        # 实际应该分析时间戳和学习效果的关系
        timings = ['morning', 'afternoon', 'evening']
        return random.choice(timings)
    
    def _analyze_best_sequence(self, history: List[Dict]) -> List[str]:
        """分析最佳学习顺序"""
        # 简化实现
        sequences = [
            ['basic', 'intermediate', 'advanced'],
            ['mirror', 'clone', 'transfer'],
            ['theory', 'practice', 'review'],
        ]
        return random.choice(sequences)
    
    def _analyze_knowledge_structure(self, agent: Dict) -> Dict:
        """分析知识结构"""
        return {
            'facts': agent.get('knowledge', {}).get('facts', []),
            'patterns': agent.get('knowledge', {}).get('patterns', []),
            'strategies': agent.get('knowledge', {}).get('strategies', []),
        }
    
    def _analyze_knowledge_gaps(self, agent: Dict) -> List[str]:
        """分析知识缺口"""
        # 简化实现
        # 实际应该对比理想知识结构
        required = ['leadership', 'strategy', 'communication']
        current = agent.get('skills', [])
        
        gaps = [skill for skill in required if skill not in current]
        return gaps
    
    def _identify_transferable(
        self,
        source_knowledge: Dict,
        target_gaps: List[str],
    ) -> List[Dict]:
        """识别可迁移的知识"""
        transferable = []
        
        for gap in target_gaps:
            # 查找源知识中相关的部分
            for category, items in source_knowledge.items():
                for item in items:
                    if gap.lower() in item.lower():
                        transferable.append({
                            'type': category,
                            'content': item,
                            'relevance': 0.8,
                        })
        
        return transferable
    
    def _optimize_transfer_sequence(
        self,
        transferable: List[Dict],
    ) -> List[Dict]:
        """优化迁移顺序"""
        # 按相关性排序
        return sorted(
            transferable,
            key=lambda x: x.get('relevance', 0),
            reverse=True,
        )
    
    def get_transfer_stats(self) -> Dict:
        """获取迁移统计"""
        if not self.transfer_history:
            return {
                'total_transfers': 0,
                'average_efficiency': 0,
                'most_active_source': None,
                'most_active_target': None,
            }
        
        total = len(self.transfer_history)
        avg_efficiency = sum(t.efficiency for t in self.transfer_history) / total
        
        # 统计最活跃的源和目标
        sources = {}
        targets = {}
        
        for transfer in self.transfer_history:
            sources[transfer.source] = sources.get(transfer.source, 0) + 1
            targets[transfer.target] = targets.get(transfer.target, 0) + 1
        
        most_active_source = max(sources.items(), key=lambda x: x[1])[0] if sources else None
        most_active_target = max(targets.items(), key=lambda x: x[1])[0] if targets else None
        
        return {
            'total_transfers': total,
            'average_efficiency': avg_efficiency,
            'most_active_source': most_active_source,
            'most_active_target': most_active_target,
        }


# 使用示例
if __name__ == "__main__":
    import asyncio
    
    async def main():
        learner = MetaLearner()
        
        # 记录学习经验
        learner.record_learning_experience(
            agent_id='ceo-1',
            method='mirror',
            result={'score': 0.8, 'retention': 0.7},
        )
        
        learner.record_learning_experience(
            agent_id='ceo-1',
            method='clone',
            result={'score': 0.6, 'retention': 0.5},
        )
        
        # 生成个性化策略
        agent = {'id': 'ceo-1', 'name': 'CEO-1'}
        strategy = await learner.learn_how_to_learn(agent)
        
        # 知识迁移
        source = {
            'name': 'ceo-1',
            'skills': ['leadership', 'strategy'],
            'knowledge': {
                'facts': ['leadership_fact_1', 'strategy_fact_1'],
                'patterns': ['leadership_pattern_1'],
                'strategies': ['strategy_1'],
            },
        }
        
        target = {
            'name': 'pm-1',
            'skills': ['planning'],
        }
        
        transfer = await learner.transfer_learning(source, target)
        
        # 统计
        stats = learner.get_transfer_stats()
        print(f"\n📊 迁移统计：{stats}")
    
    asyncio.run(main())
