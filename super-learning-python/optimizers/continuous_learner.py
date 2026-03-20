"""
持续学习模块

从会话中自动提取模式，生成新技能
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict
import hashlib


@dataclass
class SessionPattern:
    """会话模式"""
    id: str
    type: str  # learning_strategy, optimization, synergy
    description: str
    success_rate: float
    occurrence_count: int
    last_seen: str
    context: Dict[str, Any]


class ContinuousLearner:
    """
    持续学习器
    
    从会话中提取模式，生成可重用技能
    """
    
    def __init__(self, patterns_db_path: str = None):
        """
        初始化持续学习器
        
        Args:
            patterns_db_path: 模式数据库路径
        """
        if patterns_db_path is None:
            patterns_db_path = os.path.expanduser(
                '~/.openclaw/super_learning/patterns.json'
            )
        
        self.patterns_db_path = patterns_db_path
        self.patterns: List[SessionPattern] = []
        self._load_patterns()
    
    def _load_patterns(self):
        """加载模式"""
        if os.path.exists(self.patterns_db_path):
            with open(self.patterns_db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.patterns = [
                    SessionPattern(**p) for p in data.get('patterns', [])
                ]
    
    def _save_patterns(self):
        """保存模式"""
        os.makedirs(os.path.dirname(self.patterns_db_path), exist_ok=True)
        
        with open(self.patterns_db_path, 'w', encoding='utf-8') as f:
            json.dump({
                'patterns': [p.__dict__ for p in self.patterns],
                'last_updated': datetime.now().isoformat(),
            }, f, ensure_ascii=False, indent=2)
    
    def extract_patterns_from_session(self, session_data: List[Dict]) -> List[SessionPattern]:
        """
        从会话中提取模式
        
        Args:
            session_data: 会话数据列表
        
        Returns:
            提取的模式列表
        """
        new_patterns = []
        
        # 1. 分析成功的学习事件 (performance_score > 0.8)
        successful_events = [
            e for e in session_data 
            if e.get('performance_score', 0) > 0.8
        ]
        
        if len(successful_events) < 3:
            # 数据不足
            return []
        
        # 2. 提取共同特征
        common_patterns = self._find_common_patterns(successful_events)
        
        # 3. 创建新模式
        for pattern_type, pattern_data in common_patterns.items():
            pattern = SessionPattern(
                id=self._generate_pattern_id(pattern_type, pattern_data),
                type=pattern_type,
                description=pattern_data['description'],
                success_rate=pattern_data['success_rate'],
                occurrence_count=pattern_data['occurrence_count'],
                last_seen=datetime.now().isoformat(),
                context=pattern_data['context'],
            )
            
            # 4. 检查是否已存在
            existing = self._find_similar_pattern(pattern)
            
            if existing:
                # 更新现有模式
                existing.occurrence_count += 1
                existing.last_seen = pattern.last_seen
                existing.success_rate = (
                    existing.success_rate * existing.occurrence_count + 
                    pattern.success_rate
                ) / (existing.occurrence_count + 1)
            else:
                # 添加新模式
                new_patterns.append(pattern)
                self.patterns.append(pattern)
        
        # 5. 保存
        self._save_patterns()
        
        return new_patterns
    
    def _find_common_patterns(self, events: List[Dict]) -> Dict[str, Dict]:
        """
        找出共同模式
        
        Args:
            events: 成功事件列表
        
        Returns:
            模式字典
        """
        patterns = defaultdict(lambda: {
            'features': defaultdict(int),
            'success_scores': [],
            'occurrence_count': 0,
        })
        
        for event in events:
            event_type = event.get('event_type', 'unknown')
            
            # 提取特征
            features = self._extract_features(event)
            
            for feature_key, feature_value in features.items():
                patterns[event_type]['features'][f"{feature_key}={feature_value}"] += 1
            
            patterns[event_type]['success_scores'].append(
                event.get('performance_score', 0)
            )
            patterns[event_type]['occurrence_count'] += 1
        
        # 转换为描述性模式
        result = {}
        
        for event_type, data in patterns.items():
            if data['occurrence_count'] < 3:
                continue
            
            # 找出最常见的特征
            top_features = sorted(
                data['features'].items(),
                key=lambda x: x[1],
                reverse=True,
            )[:5]
            
            result[event_type] = {
                'description': f"高成功率的{event_type}策略",
                'success_rate': sum(data['success_scores']) / len(data['success_scores']),
                'occurrence_count': data['occurrence_count'],
                'context': {
                    'top_features': dict(top_features),
                },
            }
        
        return result
    
    def _extract_features(self, event: Dict) -> Dict[str, Any]:
        """
        提取事件特征
        
        Args:
            event: 事件数据
        
        Returns:
            特征字典
        """
        features = {}
        
        # 学习策略特征
        if event.get('event_type') in ['clone', 'mirror', 'transfer']:
            features['strategy'] = event.get('event_type')
            
            # 时间特征
            timestamp = event.get('timestamp', '')
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                    features['hour_of_day'] = dt.hour
                    features['day_of_week'] = dt.weekday()
                except ValueError:
                    pass
            
            # Agent 特征
            features['agent_role'] = event.get('context', {}).get('role', 'unknown')
        
        return features
    
    def _generate_pattern_id(self, pattern_type: str, pattern_data: Dict) -> str:
        """生成模式 ID"""
        content = f"{pattern_type}:{json.dumps(pattern_data, sort_keys=True)}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def _find_similar_pattern(self, pattern: SessionPattern) -> SessionPattern:
        """查找相似模式"""
        for existing in self.patterns:
            if (
                existing.type == pattern.type and
                existing.description == pattern.description
            ):
                return existing
        return None
    
    def get_high_success_patterns(self, min_success_rate: float = 0.8) -> List[SessionPattern]:
        """
        获取高成功率模式
        
        Args:
            min_success_rate: 最小成功率
        
        Returns:
            高成功率模式列表
        """
        return [
            p for p in self.patterns
            if p.success_rate >= min_success_rate and p.occurrence_count >= 3
        ]
    
    def generate_skill_from_pattern(self, pattern: SessionPattern) -> Dict[str, Any]:
        """
        从模式生成技能
        
        Args:
            pattern: 模式
        
        Returns:
            技能定义
        """
        skill = {
            'name': f"pattern_{pattern.type}_{pattern.id}",
            'description': pattern.description,
            'success_rate': pattern.success_rate,
            'based_on_occurrences': pattern.occurrence_count,
            'context': pattern.context,
            'created_at': datetime.now().isoformat(),
        }
        
        return skill


# 使用示例
if __name__ == "__main__":
    learner = ContinuousLearner()
    
    # 模拟会话数据
    session_data = [
        {
            'event_type': 'mirror',
            'performance_score': 0.9,
            'timestamp': datetime.now().isoformat(),
            'context': {'role': 'CEO'},
        },
        {
            'event_type': 'mirror',
            'performance_score': 0.85,
            'timestamp': datetime.now().isoformat(),
            'context': {'role': 'CEO'},
        },
        {
            'event_type': 'mirror',
            'performance_score': 0.88,
            'timestamp': datetime.now().isoformat(),
            'context': {'role': 'CEO'},
        },
    ]
    
    # 提取模式
    patterns = learner.extract_patterns_from_session(session_data)
    
    print(f"✅ 提取了 {len(patterns)} 个模式")
    
    for pattern in patterns:
        print(f"\n📊 模式：{pattern.type}")
        print(f"   描述：{pattern.description}")
        print(f"   成功率：{pattern.success_rate:.1%}")
        print(f"   出现次数：{pattern.occurrence_count}")
        
        # 生成技能
        skill = learner.generate_skill_from_pattern(pattern)
        print(f"   生成技能：{skill['name']}")
