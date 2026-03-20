"""
验证循环模块

持续评估策略效果，使用 pass@k 指标
"""

import numpy as np
from typing import Dict, List, Any, Tuple
from datetime import datetime
from dataclasses import dataclass


@dataclass
class EvaluationCheckpoint:
    """评估检查点"""
    timestamp: str
    strategy_params: Dict[str, float]
    metrics: Dict[str, float]
    pass_at_k: Dict[int, float]


class ValidationLoop:
    """
    验证循环
    
    持续评估策略效果，使用 pass@k 指标
    """
    
    def __init__(self):
        """初始化验证循环"""
        self.checkpoints: List[EvaluationCheckpoint] = []
        self.current_strategy: Dict[str, float] = {}
        self.evaluation_history: List[Dict] = []
    
    def record_evaluation(
        self,
        strategy_params: Dict[str, float],
        metrics: Dict[str, float],
        pass_results: List[bool],
    ) -> EvaluationCheckpoint:
        """
        记录评估结果
        
        Args:
            strategy_params: 策略参数
            metrics: 评估指标
            pass_results: pass/fail 结果列表
        
        Returns:
            评估检查点
        """
        # 计算 pass@k
        pass_at_k = self._calculate_pass_at_k(pass_results)
        
        checkpoint = EvaluationCheckpoint(
            timestamp=datetime.now().isoformat(),
            strategy_params=strategy_params,
            metrics=metrics,
            pass_at_k=pass_at_k,
        )
        
        self.checkpoints.append(checkpoint)
        
        return checkpoint
    
    def _calculate_pass_at_k(self, pass_results: List[bool]) -> Dict[int, float]:
        """
        计算 pass@k 指标
        
        Args:
            pass_results: pass/fail 结果列表
        
        Returns:
            pass@k 字典 {k: pass_rate}
        """
        n = len(pass_results)
        total_passes = sum(pass_results)
        
        pass_at_k = {}
        
        for k in [1, 3, 5, 10]:
            if k > n:
                pass_at_k[k] = 1.0 if total_passes > 0 else 0.0
            else:
                # pass@k = 1 - C(n-passes, k) / C(n, k)
                from math import comb
                
                n_fail = n - total_passes
                
                if n_fail >= k:
                    fail_prob = comb(n_fail, k) / comb(n, k)
                    pass_at_k[k] = 1.0 - fail_prob
                else:
                    pass_at_k[k] = 1.0
        
        return pass_at_k
    
    def get_best_strategy(self) -> Dict[str, float]:
        """
        获取最佳策略
        
        Returns:
            最佳策略参数
        """
        if not self.checkpoints:
            return {}
        
        # 根据 pass@1 排序
        best_checkpoint = max(
            self.checkpoints,
            key=lambda c: c.pass_at_k.get(1, 0),
        )
        
        return best_checkpoint.strategy_params
    
    def analyze_trends(self) -> Dict[str, Any]:
        """
        分析趋势
        
        Returns:
            趋势分析结果
        """
        if len(self.checkpoints) < 2:
            return {'error': 'Not enough data'}
        
        # 提取 pass@1 序列
        pass_at_1_series = [c.pass_at_k.get(1, 0) for c in self.checkpoints]
        
        # 计算趋势
        trend = np.polyfit(range(len(pass_at_1_series)), pass_at_1_series, 1)[0]
        
        # 计算统计
        stats = {
            'mean_pass_at_1': np.mean(pass_at_1_series),
            'std_pass_at_1': np.std(pass_at_1_series),
            'best_pass_at_1': max(pass_at_1_series),
            'worst_pass_at_1': min(pass_at_1_series),
            'trend': 'improving' if trend > 0 else 'declining' if trend < 0 else 'stable',
            'trend_slope': trend,
        }
        
        return stats
    
    def should_continue(self, min_improvement: float = 0.01) -> bool:
        """
        判断是否应该继续优化
        
        Args:
            min_improvement: 最小改进阈值
        
        Returns:
            是否继续
        """
        if len(self.checkpoints) < 5:
            return True
        
        # 检查最近 5 次的改进
        recent = self.checkpoints[-5:]
        recent_pass_at_1 = [c.pass_at_k.get(1, 0) for c in recent]
        
        improvement = recent_pass_at_1[-1] - recent_pass_at_1[0]
        
        return improvement >= min_improvement
    
    def generate_report(self) -> Dict[str, Any]:
        """
        生成验证报告
        
        Returns:
            验证报告
        """
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_evaluations': len(self.checkpoints),
            'current_strategy': self.current_strategy,
            'best_strategy': self.get_best_strategy(),
            'trends': self.analyze_trends(),
            'recommendation': self._generate_recommendation(),
        }
        
        return report
    
    def _generate_recommendation(self) -> str:
        """生成建议"""
        if len(self.checkpoints) < 2:
            return '需要更多评估数据'
        
        trends = self.analyze_trends()
        
        if 'error' in trends:
            return '数据不足，无法分析'
        
        if trends['trend'] == 'improving':
            return '继续当前优化策略'
        elif trends['trend'] == 'declining':
            return '建议调整优化方向'
        else:
            return '已达到稳定状态，可以考虑停止'


class ContinuousEvaluator:
    """
    持续评估器
    
    持续评估策略效果
    """
    
    def __init__(self, validation_loop: ValidationLoop):
        """
        初始化评估器
        
        Args:
            validation_loop: 验证循环
        """
        self.validation_loop = validation_loop
        self.evaluation_count = 0
    
    def evaluate_strategy(
        self,
        strategy_params: Dict[str, float],
        test_cases: List[Dict],
    ) -> Dict[str, Any]:
        """
        评估策略
        
        Args:
            strategy_params: 策略参数
            test_cases: 测试用例
        
        Returns:
            评估结果
        """
        pass_results = []
        metrics = {
            'success_rate': 0.0,
            'avg_score': 0.0,
            'total_score': 0.0,
        }
        
        total_score = 0.0
        
        for test_case in test_cases:
            # 模拟评估
            score = self._run_test_case(strategy_params, test_case)
            total_score += score
            
            passed = score > 0.7
            pass_results.append(passed)
        
        # 计算指标
        metrics['success_rate'] = sum(pass_results) / len(pass_results)
        metrics['avg_score'] = total_score / len(test_cases)
        metrics['total_score'] = total_score
        
        # 记录评估
        checkpoint = self.validation_loop.record_evaluation(
            strategy_params=strategy_params,
            metrics=metrics,
            pass_results=pass_results,
        )
        
        self.evaluation_count += 1
        
        return {
            'evaluation_id': self.evaluation_count,
            'metrics': metrics,
            'pass_at_k': checkpoint.pass_at_k,
            'checkpoint': checkpoint,
        }
    
    def _run_test_case(self, strategy_params: Dict[str, float], test_case: Dict) -> float:
        """
        运行测试用例
        
        Args:
            strategy_params: 策略参数
            test_case: 测试用例
        
        Returns:
            分数 0-1
        """
        # 简化实现
        # 实际应该运行真实测试
        
        # 模拟分数计算
        base_score = 0.7
        
        # 根据策略参数调整
        if strategy_params.get('learning_rate', 0.5) > 0.6:
            base_score += 0.1
        
        if strategy_params.get('transfer_frequency', 0.5) > 0.6:
            base_score += 0.1
        
        # 添加随机性
        import random
        base_score += random.uniform(-0.1, 0.1)
        
        return min(1.0, max(0.0, base_score))


# 使用示例
if __name__ == "__main__":
    validation_loop = ValidationLoop()
    evaluator = ContinuousEvaluator(validation_loop)
    
    # 模拟测试用例
    test_cases = [
        {'id': i, 'type': 'learning'}
        for i in range(20)
    ]
    
    # 评估策略
    strategy = {
        'learning_rate': 0.7,
        'transfer_frequency': 0.6,
        'detection_threshold': 0.4,
    }
    
    result = evaluator.evaluate_strategy(strategy, test_cases)
    
    print("📊 评估结果")
    print(f"评估 ID: {result['evaluation_id']}")
    print(f"成功率：{result['metrics']['success_rate']:.1%}")
    print(f"平均分：{result['metrics']['avg_score']:.3f}")
    print(f"pass@1: {result['pass_at_k'].get(1, 0):.1%}")
    print(f"pass@5: {result['pass_at_k'].get(5, 0):.1%}")
    
    # 生成报告
    report = validation_loop.generate_report()
    
    print("\n📝 验证报告")
    print(f"总评估次数：{report['total_evaluations']}")
    print(f"趋势：{report['trends'].get('trend', 'N/A')}")
    print(f"建议：{report['recommendation']}")
