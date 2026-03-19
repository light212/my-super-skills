"""
优化器模块

使用 Optuna 实现超参数优化
"""

import optuna
from typing import Dict, Any, Callable
from dataclasses import dataclass


@dataclass
class OptimizationResult:
    """优化结果"""
    best_params: Dict[str, float]
    best_score: float
    trials: int
    study: optuna.Study


class StrategyOptimizer:
    """
    学习策略优化器
    
    使用 Optuna 自动搜索最优超参数
    """
    
    def __init__(self, objective_fn: Callable = None):
        """
        初始化优化器
        
        Args:
            objective_fn: 目标函数，接收 params 返回 score
        """
        self.objective_fn = objective_fn or self._default_objective
        self.study = None
        self.best_result = None
    
    def _default_objective(self, trial: optuna.Trial) -> float:
        """
        默认目标函数
        
        实际使用时应该替换为真实的性能评估函数
        """
        # 建议超参数范围
        learning_rate = trial.suggest_float('learning_rate', 0.01, 1.0, log=True)
        transfer_frequency = trial.suggest_float('transfer_frequency', 0.1, 1.0)
        detection_threshold = trial.suggest_float('detection_threshold', 0.1, 0.9)
        mirror_weight = trial.suggest_float('mirror_weight', 0.0, 1.0)
        clone_weight = trial.suggest_float('clone_weight', 0.0, 1.0)
        transfer_weight = trial.suggest_float('transfer_weight', 0.0, 1.0)
        
        # 模拟性能评估
        # 实际应该从真实数据计算
        score = (
            learning_rate * 0.3 +
            transfer_frequency * 0.2 +
            (1 - detection_threshold) * 0.2 +
            (mirror_weight + clone_weight + transfer_weight) / 3 * 0.3
        )
        
        return score
    
    def optimize(
        self,
        n_trials: int = 100,
        timeout: int = None,
        direction: str = 'maximize',
    ) -> OptimizationResult:
        """
        执行优化
        
        Args:
            n_trials: 试验次数
            timeout: 超时时间 (秒)
            direction: 优化方向 ('maximize' 或 'minimize')
        
        Returns:
            优化结果
        """
        # 创建研究
        self.study = optuna.create_study(direction=direction)
        
        # 执行优化
        self.study.optimize(
            self.objective_fn,
            n_trials=n_trials,
            timeout=timeout,
            show_progress_bar=True,
        )
        
        # 记录最佳结果
        self.best_result = OptimizationResult(
            best_params=self.study.best_params,
            best_score=self.study.best_value,
            trials=len(self.study.trials),
            study=self.study,
        )
        
        print(f"✨ 优化完成！")
        print(f"   最佳得分：{self.best_result.best_score:.4f}")
        print(f"   试验次数：{self.best_result.trials}")
        print(f"   最佳参数:")
        for key, value in self.best_result.best_params.items():
            print(f"     {key}: {value:.4f}")
        
        return self.best_result
    
    def get_optimized_strategy(self) -> Dict[str, float]:
        """获取优化后的策略"""
        if not self.best_result:
            raise ValueError("请先执行优化")
        
        return self.best_result.best_params
    
    def visualize(self, save_path: str = None):
        """
        可视化优化结果
        
        Args:
            save_path: 保存路径 (可选)
        """
        if not self.study:
            raise ValueError("请先执行优化")
        
        # 绘制优化历史
        fig1 = optuna.visualization.plot_optimization_history(self.study)
        
        # 绘制参数重要性
        fig2 = optuna.visualization.plot_param_importances(self.study)
        
        if save_path:
            fig1.write_image(f"{save_path}/optimization_history.png")
            fig2.write_image(f"{save_path}/param_importances.png")
        else:
            fig1.show()
            fig2.show()


class ParameterTuner:
    """
    参数调优器
    
    针对特定场景调优参数
    """
    
    def __init__(self):
        self.tuning_history = []
    
    def tune_for_scenario(self, scenario: str, base_params: Dict[str, float]) -> Dict[str, float]:
        """
        针对特定场景调优参数
        
        Args:
            scenario: 场景名称 ('fast_learning', 'high_retention', 'efficient_transfer')
            base_params: 基础参数
        
        Returns:
            调优后的参数
        """
        if scenario == 'fast_learning':
            # 快速学习场景
            return {
                **base_params,
                'learning_rate': min(1.0, base_params.get('learning_rate', 0.5) + 0.2),
                'detection_threshold': max(0.1, base_params.get('detection_threshold', 0.5) - 0.2),
            }
        
        elif scenario == 'high_retention':
            # 高保留率场景
            return {
                **base_params,
                'transfer_frequency': min(1.0, base_params.get('transfer_frequency', 0.5) + 0.2),
                'mirror_weight': min(1.0, base_params.get('mirror_weight', 0.33) + 0.2),
            }
        
        elif scenario == 'efficient_transfer':
            # 高效传递场景
            return {
                **base_params,
                'transfer_frequency': min(1.0, base_params.get('transfer_frequency', 0.5) + 0.3),
                'transfer_weight': min(1.0, base_params.get('transfer_weight', 0.33) + 0.3),
            }
        
        else:
            return base_params
    
    def auto_tune(
        self,
        current_params: Dict[str, float],
        performance_metrics: Dict[str, float],
    ) -> Dict[str, float]:
        """
        自动调优
        
        基于性能数据自动调整参数
        """
        tuned = current_params.copy()
        
        # 学习速度过慢
        if performance_metrics.get('learning_speed', 1.0) < 0.5:
            tuned['learning_rate'] = min(1.0, tuned.get('learning_rate', 0.5) + 0.1)
        
        # 知识保留率低
        if performance_metrics.get('knowledge_retention', 1.0) < 0.5:
            tuned['transfer_frequency'] = min(1.0, tuned.get('transfer_frequency', 0.5) + 0.1)
            tuned['mirror_weight'] = min(1.0, tuned.get('mirror_weight', 0.33) + 0.1)
        
        # 传递效率低
        if performance_metrics.get('transfer_efficiency', 1.0) < 0.5:
            tuned['transfer_frequency'] = min(1.0, tuned.get('transfer_frequency', 0.5) + 0.15)
            tuned['transfer_weight'] = min(1.0, tuned.get('transfer_weight', 0.33) + 0.15)
        
        # 适应速度慢
        if performance_metrics.get('adaptation_speed', 1.0) < 0.5:
            tuned['detection_threshold'] = max(0.1, tuned.get('detection_threshold', 0.5) - 0.1)
        
        # 记录调优历史
        self.tuning_history.append({
            'before': current_params,
            'after': tuned,
            'metrics': performance_metrics,
        })
        
        return tuned


# 使用示例
if __name__ == "__main__":
    # 优化器示例
    optimizer = StrategyOptimizer()
    result = optimizer.optimize(n_trials=50)
    
    print("\n📊 优化结果:")
    print(f"最佳参数：{result.best_params}")
    
    # 参数调优器示例
    tuner = ParameterTuner()
    
    base_params = {
        'learning_rate': 0.5,
        'transfer_frequency': 0.5,
        'detection_threshold': 0.5,
        'mirror_weight': 0.33,
        'clone_weight': 0.33,
        'transfer_weight': 0.34,
    }
    
    # 针对快速学习场景调优
    fast_params = tuner.tune_for_scenario('fast_learning', base_params)
    print(f"\n⚡ 快速学习参数：{fast_params}")
    
    # 自动调优
    performance = {
        'learning_speed': 0.4,
        'knowledge_retention': 0.6,
        'transfer_efficiency': 0.5,
        'adaptation_speed': 0.45,
    }
    
    optimized_params = tuner.auto_tune(base_params, performance)
    print(f"\n🔧 自动调优参数：{optimized_params}")
