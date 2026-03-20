"""
自主学习循环系统

核心循环：分辨 → 判断 → 吸收 → 壮大 → 健硕 → 成熟 → 循环
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
import numpy as np


class GrowthStage(Enum):
    """成长阶段"""
    INITIAL = "initial"       # 初始
    DISCRIMINATING = "discriminating"  # 分辨
    JUDGING = "judging"       # 判断
    ABSORBING = "absorbing"   # 吸收
    EXPANDING = "expanding"   # 壮大
    STRENGTHENING = "strengthening"  # 健硕
    MATURING = "maturing"     # 成熟


@dataclass
class LearningCycle:
    """学习循环"""
    cycle_id: str
    stage: GrowthStage
    started_at: str
    completed_at: Optional[str] = None
    inputs: List[Dict] = field(default_factory=list)
    outputs: List[Dict] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)


class AutonomousLearner:
    """
    自主学习器
    
    实现完整的自主学习循环：
    分辨 → 判断 → 吸收 → 壮大 → 健硕 → 成熟 → 循环
    """
    
    def __init__(self, state_path: str = None):
        """
        初始化自主学习器
        
        Args:
            state_path: 状态保存路径
        """
        if state_path is None:
            state_path = os.path.expanduser(
                '~/.openclaw/super_learning/autonomous_state.json'
            )
        
        self.state_path = state_path
        self.current_stage = GrowthStage.INITIAL
        self.cycles: List[LearningCycle] = []
        self.current_cycle: Optional[LearningCycle] = None
        
        # 能力指标
        self.capabilities = {
            'discrimination': 0.0,  # 分辨能力
            'judgment': 0.0,         # 判断能力
            'absorption': 0.0,       # 吸收能力
            'expansion': 0.0,        # 壮大能力
            'strengthening': 0.0,    # 健硕能力
            'maturation': 0.0,       # 成熟能力
        }
        
        self._load_state()
    
    def _load_state(self):
        """加载状态"""
        if os.path.exists(self.state_path):
            with open(self.state_path, 'r', encoding='utf-8') as f:
                state = json.load(f)
                self.capabilities = state.get('capabilities', self.capabilities)
                self.current_cycle = state.get('current_cycle')
    
    def _save_state(self):
        """保存状态"""
        os.makedirs(os.path.dirname(self.state_path), exist_ok=True)
        
        # 自定义 JSON 编码器
        class StateEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()
                if isinstance(obj, GrowthStage):
                    return obj.value
                return super().default(obj)
        
        state = {
            'capabilities': self.capabilities,
            'current_cycle': self.current_cycle.__dict__ if self.current_cycle else None,
            'last_updated': datetime.now().isoformat(),
        }
        
        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2, cls=StateEncoder)
    
    def start_cycle(self) -> LearningCycle:
        """
        开始新的学习循环
        
        Returns:
            学习循环
        """
        self.current_cycle = LearningCycle(
            cycle_id=f"cycle_{len(self.cycles) + 1}",
            stage=GrowthStage.DISCRIMINATING,
            started_at=datetime.now().isoformat(),
        )
        
        self.current_stage = GrowthStage.DISCRIMINATING
        
        print(f"🌱 开始学习循环 #{len(self.cycles) + 1}")
        print(f"   阶段：{self.current_stage.value}")
        
        return self.current_cycle
    
    def discriminate(self, inputs: List[Dict]) -> Dict[str, List[Dict]]:
        """
        分辨：识别什么是好的/坏的，什么是有用的/无用的
        
        Args:
            inputs: 输入数据列表
        
        Returns:
            分类结果 {useful: [...], useless: [...]}
        """
        if not self.current_cycle:
            self.start_cycle()
        
        self.current_cycle.stage = GrowthStage.DISCRIMINATING
        self.current_cycle.inputs = inputs
        
        # 分辨逻辑
        useful = []
        useless = []
        
        for item in inputs:
            score = self._calculate_usefulness(item)
            
            if score > 0.6:  # 阈值
                useful.append({
                    **item,
                    'usefulness_score': score,
                })
            else:
                useless.append({
                    **item,
                    'usefulness_score': score,
                })
        
        # 更新分辨能力指标
        self.capabilities['discrimination'] = self._update_capability(
            self.capabilities['discrimination'],
            len(useful) / max(len(inputs), 1)
        )
        
        result = {
            'useful': useful,
            'useless': useless,
        }
        
        self.current_cycle.outputs.append({
            'stage': 'discriminate',
            'result': result,
        })
        
        print(f"🔍 分辨完成")
        print(f"   有用：{len(useful)}")
        print(f"   无用：{len(useless)}")
        print(f"   分辨能力：{self.capabilities['discrimination']:.2f}")
        
        return result
    
    def _calculate_usefulness(self, item: Dict) -> float:
        """
        计算有用性分数
        
        Args:
            item: 输入项
        
        Returns:
            有用性分数 0-1
        """
        # 简化实现
        # 实际应该基于多个维度计算
        
        score = 0.5
        
        # 维度 1: 性能分数
        if item.get('performance_score', 0) > 0.7:
            score += 0.3
        
        # 维度 2: 发生频率
        if item.get('occurrence_count', 1) > 3:
            score += 0.2
        
        # 维度 3: 最近性
        timestamp = item.get('timestamp', '')
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp)
                days_old = (datetime.now() - dt).days
                if days_old < 7:
                    score += 0.2
                elif days_old < 30:
                    score += 0.1
            except ValueError:
                pass
        
        return min(1.0, max(0.0, score))
    
    def judge(self, useful_items: List[Dict]) -> Dict[str, List[Dict]]:
        """
        判断：评估价值，决定取舍
        
        Args:
            useful_items: 有用的项目
        
        Returns:
            判断结果 {keep: [...], discard: [...]}
        """
        if not self.current_cycle:
            raise ValueError("请先开始循环")
        
        self.current_cycle.stage = GrowthStage.JUDGING
        
        # 判断逻辑
        keep = []
        discard = []
        
        for item in useful_items:
            value_score = self._calculate_value(item)
            
            if value_score > 0.7:  # 高价值阈值
                keep.append({
                    **item,
                    'value_score': value_score,
                })
            else:
                discard.append({
                    **item,
                    'value_score': value_score,
                })
        
        # 更新判断能力指标
        self.capabilities['judgment'] = self._update_capability(
            self.capabilities['judgment'],
            len(keep) / max(len(useful_items), 1)
        )
        
        result = {
            'keep': keep,
            'discard': discard,
        }
        
        self.current_cycle.outputs.append({
            'stage': 'judge',
            'result': result,
        })
        
        print(f"⚖️  判断完成")
        print(f"   保留：{len(keep)}")
        print(f"   舍弃：{len(discard)}")
        print(f"   判断能力：{self.capabilities['judgment']:.2f}")
        
        return result
    
    def _calculate_value(self, item: Dict) -> float:
        """
        计算价值分数
        
        Args:
            item: 项目
        
        Returns:
            价值分数 0-1
        """
        # 简化实现
        score = 0.5
        
        # 维度 1:  usefulness 分数
        score += item.get('usefulness_score', 0) * 0.3
        
        # 维度 2: 成功率
        score += item.get('performance_score', 0) * 0.2
        
        return min(1.0, max(0.0, score))
    
    def absorb(self, keep_items: List[Dict]) -> List[Dict]:
        """
        吸收：内化有价值的知识/模式
        
        Args:
            keep_items: 保留的项目
        
        Returns:
            吸收的模式列表
        """
        if not self.current_cycle:
            raise ValueError("请先开始循环")
        
        self.current_cycle.stage = GrowthStage.ABSORBING
        
        # 吸收逻辑：提取模式
        absorbed_patterns = []
        
        for item in keep_items:
            pattern = self._extract_pattern(item)
            if pattern:
                absorbed_patterns.append(pattern)
        
        # 更新吸收能力指标
        self.capabilities['absorption'] = self._update_capability(
            self.capabilities['absorption'],
            len(absorbed_patterns) / max(len(keep_items), 1)
        )
        
        self.current_cycle.outputs.append({
            'stage': 'absorb',
            'result': absorbed_patterns,
        })
        
        print(f"📥 吸收完成")
        print(f"   吸收模式：{len(absorbed_patterns)}")
        print(f"   吸收能力：{self.capabilities['absorption']:.2f}")
        
        return absorbed_patterns
    
    def _extract_pattern(self, item: Dict) -> Optional[Dict]:
        """
        提取模式
        
        Args:
            item: 项目
        
        Returns:
            模式字典
        """
        # 简化实现
        if item.get('performance_score', 0) > 0.8:
            return {
                'type': item.get('event_type', 'unknown'),
                'context': item.get('context', {}),
                'success_factors': self._identify_success_factors(item),
            }
        return None
    
    def _identify_success_factors(self, item: Dict) -> List[str]:
        """识别成功因素"""
        factors = []
        
        if item.get('performance_score', 0) > 0.9:
            factors.append('high_performance')
        
        if item.get('context', {}).get('role') in ['CEO', 'PM']:
            factors.append('leadership_role')
        
        return factors
    
    def expand(self, patterns: List[Dict]) -> List[Dict]:
        """
        壮大：扩展能力边界
        
        Args:
            patterns: 吸收的模式
        
        Returns:
            扩展的能力列表
        """
        if not self.current_cycle:
            raise ValueError("请先开始循环")
        
        self.current_cycle.stage = GrowthStage.EXPANDING
        
        # 扩展逻辑：基于模式生成新能力
        expanded_capabilities = []
        
        for pattern in patterns:
            capability = self._generate_capability(pattern)
            if capability:
                expanded_capabilities.append(capability)
        
        # 更新扩展能力指标
        self.capabilities['expansion'] = self._update_capability(
            self.capabilities['expansion'],
            len(expanded_capabilities) / max(len(patterns), 1)
        )
        
        self.current_cycle.outputs.append({
            'stage': 'expand',
            'result': expanded_capabilities,
        })
        
        print(f"📈 壮大完成")
        print(f"   扩展能力：{len(expanded_capabilities)}")
        print(f"   扩展能力：{self.capabilities['expansion']:.2f}")
        
        return expanded_capabilities
    
    def _generate_capability(self, pattern: Dict) -> Optional[Dict]:
        """
        生成新能力
        
        Args:
            pattern: 模式
        
        Returns:
            能力字典
        """
        # 简化实现
        return {
            'name': f"capability_{pattern['type']}",
            'based_on': pattern['type'],
            'success_factors': pattern.get('success_factors', []),
            'level': 1,
        }
    
    def strengthen(self, capabilities: List[Dict]) -> List[Dict]:
        """
        健硕：强化核心能力
        
        Args:
            capabilities: 能力列表
        
        Returns:
            强化后的能力列表
        """
        if not self.current_cycle:
            raise ValueError("请先开始循环")
        
        self.current_cycle.stage = GrowthStage.STRENGTHENING
        
        # 强化逻辑：提升能力等级
        strengthened = []
        
        for cap in capabilities:
            strengthened_cap = self._strengthen_capability(cap)
            strengthened.append(strengthened_cap)
        
        # 更新健硕能力指标
        avg_level = np.mean([c.get('level', 1) for c in strengthened])
        self.capabilities['strengthening'] = self._update_capability(
            self.capabilities['strengthening'],
            avg_level / 5.0  # 假设最大等级为 5
        )
        
        self.current_cycle.outputs.append({
            'stage': 'strengthen',
            'result': strengthened,
        })
        
        print(f"💪 健硕完成")
        print(f"   平均等级：{avg_level:.1f}")
        print(f"   健硕能力：{self.capabilities['strengthening']:.2f}")
        
        return strengthened
    
    def _strengthen_capability(self, capability: Dict) -> Dict:
        """
        强化能力
        
        Args:
            capability: 能力
        
        Returns:
            强化后的能力
        """
        # 简化实现：提升等级
        capability['level'] = capability.get('level', 1) + 1
        return capability
    
    def mature(self, strengthened_capabilities: List[Dict]) -> Dict[str, Any]:
        """
        成熟：达到稳定状态
        
        Args:
            strengthened_capabilities: 强化后的能力
        
        Returns:
            成熟结果
        """
        if not self.current_cycle:
            raise ValueError("请先开始循环")
        
        self.current_cycle.stage = GrowthStage.MATURING
        
        # 成熟逻辑：评估整体成熟度
        maturity_score = self._calculate_maturity(strengthened_capabilities)
        
        # 更新成熟能力指标
        self.capabilities['maturation'] = self._update_capability(
            self.capabilities['maturation'],
            maturity_score
        )
        
        result = {
            'maturity_score': maturity_score,
            'capabilities': strengthened_capabilities,
            'is_mature': maturity_score > 0.8,
        }
        
        self.current_cycle.outputs.append({
            'stage': 'mature',
            'result': result,
        })
        
        self.current_cycle.completed_at = datetime.now().isoformat()
        self.current_cycle.metrics = self.capabilities.copy()
        
        # 保存循环
        self.cycles.append(self.current_cycle)
        
        print(f"🎓 成熟完成")
        print(f"   成熟度：{maturity_score:.2f}")
        print(f"   成熟能力：{self.capabilities['maturation']:.2f}")
        print(f"   是否成熟：{'是' if result['is_mature'] else '否'}")
        
        # 保存状态
        self._save_state()
        
        return result
    
    def _calculate_maturity(self, capabilities: List[Dict]) -> float:
        """
        计算成熟度
        
        Args:
            capabilities: 能力列表
        
        Returns:
            成熟度 0-1
        """
        if not capabilities:
            return 0.0
        
        # 基于能力等级计算
        avg_level = np.mean([c.get('level', 1) for c in capabilities])
        
        # 基于能力多样性计算
        unique_types = len(set(c.get('based_on', '') for c in capabilities))
        
        # 综合计算
        maturity = (avg_level / 5.0) * 0.7 + (unique_types / 10.0) * 0.3
        
        return min(1.0, max(0.0, maturity))
    
    def _update_capability(self, current: float, new: float, alpha: float = 0.1) -> float:
        """
        更新能力指标 (指数移动平均)
        
        Args:
            current: 当前值
            new: 新值
            alpha: 平滑系数
        
        Returns:
            更新后的值
        """
        return current * (1 - alpha) + new * alpha
    
    def run_full_cycle(self, inputs: List[Dict]) -> Dict[str, Any]:
        """
        运行完整的学习循环
        
        Args:
            inputs: 输入数据
        
        Returns:
            循环结果
        """
        print("\n🔄 开始完整学习循环")
        print("=" * 50)
        
        # 1. 分辨
        discriminated = self.discriminate(inputs)
        
        # 2. 判断
        judged = self.judge(discriminated['useful'])
        
        # 3. 吸收
        absorbed = self.absorb(judged['keep'])
        
        # 4. 壮大
        expanded = self.expand(absorbed)
        
        # 5. 健硕
        strengthened = self.strengthen(expanded)
        
        # 6. 成熟
        matured = self.mature(strengthened)
        
        print("=" * 50)
        print("✅ 学习循环完成\n")
        
        return matured
    
    def get_progress_report(self) -> Dict[str, Any]:
        """
        获取进度报告
        
        Returns:
            进度报告
        """
        return {
            'total_cycles': len(self.cycles),
            'current_stage': self.current_stage.value,
            'capabilities': self.capabilities,
            'overall_progress': np.mean(list(self.capabilities.values())),
            'last_cycle': self.cycles[-1].__dict__ if self.cycles else None,
        }


# 使用示例
if __name__ == "__main__":
    learner = AutonomousLearner()
    
    # 模拟输入数据
    inputs = [
        {
            'event_type': 'mirror',
            'performance_score': 0.9,
            'timestamp': datetime.now().isoformat(),
            'context': {'role': 'CEO'},
        },
        {
            'event_type': 'clone',
            'performance_score': 0.85,
            'timestamp': datetime.now().isoformat(),
            'context': {'role': 'PM'},
        },
        {
            'event_type': 'transfer',
            'performance_score': 0.5,  # 低分
            'timestamp': datetime.now().isoformat(),
            'context': {'role': 'FE'},
        },
    ]
    
    # 运行完整循环
    result = learner.run_full_cycle(inputs)
    
    # 获取进度报告
    report = learner.get_progress_report()
    
    print("📊 进度报告")
    print(f"总循环数：{report['total_cycles']}")
    print(f"当前阶段：{report['current_stage']}")
    print(f"整体进度：{report['overall_progress']:.2f}")
    print(f"\n能力指标:")
    for key, value in report['capabilities'].items():
        print(f"  {key}: {value:.2f}")
