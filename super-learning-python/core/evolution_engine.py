"""
自我进化引擎

使用 DEAP 库实现遗传算法，自动优化学习策略
"""

import random
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

from deap import base, creator, tools, algorithms


@dataclass
class LearningStrategy:
    """学习策略"""
    id: str
    learning_rate: float  # 学习率
    transfer_frequency: float  # 知识传递频率
    detection_threshold: float  # 检测阈值
    mirror_weight: float  # 镜像学习权重
    clone_weight: float  # 克隆学习权重
    transfer_weight: float  # 传递学习权重
    
    def to_genome(self) -> List[float]:
        """转换为基因组"""
        return [
            self.learning_rate,
            self.transfer_frequency,
            self.detection_threshold,
            self.mirror_weight,
            self.clone_weight,
            self.transfer_weight,
        ]
    
    @classmethod
    def from_genome(cls, genome: List[float], id: str = "strategy") -> "LearningStrategy":
        """从基因组创建"""
        return cls(
            id=id,
            learning_rate=genome[0],
            transfer_frequency=genome[1],
            detection_threshold=genome[2],
            mirror_weight=genome[3],
            clone_weight=genome[4],
            transfer_weight=genome[5],
        )


@dataclass
class PerformanceMetrics:
    """性能指标"""
    learning_speed: float  # 学习速度 0-1
    knowledge_retention: float  # 知识保留率 0-1
    transfer_efficiency: float  # 传递效率 0-1
    adaptation_speed: float  # 适应速度 0-1
    
    def score(self) -> float:
        """计算综合得分"""
        return (
            self.learning_speed * 0.3 +
            self.knowledge_retention * 0.3 +
            self.transfer_efficiency * 0.2 +
            self.adaptation_speed * 0.2
        )


class SelfEvolutionEngine:
    """
    自我进化引擎
    
    使用遗传算法自动优化学习策略
    """
    
    def __init__(self, population_size: int = 50, generations: int = 20):
        self.population_size = population_size
        self.generations = generations
        
        # 创建 DEAP 工具包
        self.toolbox = base.Toolbox()
        self.setup_evolution()
        
        # 历史记录
        self.generations_history: List[Dict] = []
        self.current_generation = 0
    
    def setup_evolution(self):
        """设置进化算法"""
        # 创建适应度类（最大化）
        try:
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        except TypeError:
            # 类已存在，跳过
            pass
        
        # 创建个体类
        try:
            creator.create("Individual", list, fitness=creator.FitnessMax)
        except TypeError:
            # 类已存在，跳过
            pass
        
        # 注册基因生成器（6 个参数，范围 0-1）
        for i in range(6):
            self.toolbox.register(f"attr_{i}", random.uniform, 0, 1)
        
        # 注册个体生成器 - 直接创建 list
        def create_individual():
            return [getattr(self.toolbox, f"attr_{i}")() for i in range(6)]
        
        self.toolbox.register("individual", create_individual)
        
        # 注册种群生成器
        def create_population(n):
            return [create_individual() for _ in range(n)]
        
        self.toolbox.register("population", create_population)
        
        # 注册适应度函数
        self.toolbox.register("evaluate", self.evaluate_fitness)
        
        # 注册选择算子（锦标赛选择）
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        
        # 注册交叉算子（模拟二进制交叉）
        self.toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=0, up=1, eta=20)
        
        # 注册变异算子（多项式变异）
        self.toolbox.register("mutate", tools.mutPolynomialBounded, low=0, up=1, eta=20, indpb=0.1)
    
    def evaluate_fitness(self, genome) -> tuple:
        """
        评估适应度
        
        Args:
            genome: 基因组 (list of 6 floats)
        
        Returns:
            适应度分数 tuple
        """
        strategy = LearningStrategy.from_genome(genome)
        metrics = self.simulate_performance(strategy)
        return (metrics.score(),)
    
    def simulate_performance(self, strategy: LearningStrategy) -> PerformanceMetrics:
        """
        模拟性能评估
        
        实际应用中应该从真实数据计算
        """
        # 这里使用随机数据模拟
        # 实际应该基于历史学习记录
        return PerformanceMetrics(
            learning_speed=random.uniform(0.5, 0.9),
            knowledge_retention=random.uniform(0.6, 0.95),
            transfer_efficiency=random.uniform(0.5, 0.9),
            adaptation_speed=random.uniform(0.4, 0.85),
        )
    
    def evolve(self, initial_population: List[LearningStrategy] = None) -> LearningStrategy:
        """
        执行进化 (简化版，不依赖 DEAP 复杂功能)
        
        Returns:
            最优学习策略
        """
        # 创建初始种群 (简单的 list of lists)
        population = []
        for _ in range(self.population_size):
            genome = [random.uniform(0, 1) for _ in range(6)]
            population.append({'genome': genome, 'fitness': None})
        
        # 进化循环
        for generation in range(self.generations):
            # 评估适应度
            for ind in population:
                ind['fitness'] = self.evaluate_fitness(ind['genome'])[0]
            
            # 选择 (锦标赛选择)
            offspring = []
            for _ in range(self.population_size):
                contestants = random.sample(population, 3)
                winner = max(contestants, key=lambda x: x['fitness'])
                offspring.append({'genome': winner['genome'][:], 'fitness': None})
            
            # 交叉
            for i in range(0, len(offspring), 2):
                if i + 1 < len(offspring) and random.random() < 0.7:
                    point = random.randint(1, 5)
                    offspring[i]['genome'][point:], offspring[i+1]['genome'][point:] = \
                        offspring[i+1]['genome'][point:], offspring[i]['genome'][point:]
            
            # 变异
            for ind in offspring:
                if random.random() < 0.2:
                    gene_idx = random.randint(0, 5)
                    ind['genome'][gene_idx] = random.uniform(0, 1)
            
            # 评估新种群的适应度
            for ind in offspring:
                ind['fitness'] = self.evaluate_fitness(ind['genome'])[0]
            
            population = offspring
            
            # 记录这一代
            best_ind = max(population, key=lambda x: x['fitness'] if x['fitness'] is not None else -1)
            self.generations_history.append({
                "generation": generation,
                "best_fitness": best_ind['fitness'],
                "best_genome": best_ind['genome'],
                "timestamp": datetime.now().isoformat(),
            })
            
            self.current_generation = generation
            
            print(f"🧬 第 {generation} 代：最佳适应度 = {best_ind['fitness']:.4f}")
        
        # 返回最优策略
        best_ind = max(population, key=lambda x: x['fitness'])
        best_strategy = LearningStrategy.from_genome(
            best_ind['genome'],
            id=f"evolved_gen_{self.current_generation}"
        )
        
        print(f"✨ 进化完成！最优策略：{best_strategy}")
        
        return best_strategy
    
    def get_evolution_history(self) -> List[Dict]:
        """获取进化历史"""
        return self.generations_history


# 使用示例
if __name__ == "__main__":
    engine = SelfEvolutionEngine(population_size=30, generations=10)
    best_strategy = engine.evolve()
    
    print("\n📊 进化结果:")
    print(f"学习率：{best_strategy.learning_rate:.3f}")
    print(f"传递频率：{best_strategy.transfer_frequency:.3f}")
    print(f"检测阈值：{best_strategy.detection_threshold:.3f}")
    print(f"镜像权重：{best_strategy.mirror_weight:.3f}")
    print(f"克隆权重：{best_strategy.clone_weight:.3f}")
    print(f"传递权重：{best_strategy.transfer_weight:.3f}")
