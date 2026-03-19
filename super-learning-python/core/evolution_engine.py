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
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        
        # 创建个体类
        creator.create("Individual", list, fitness=creator.FitnessMax)
        
        # 注册基因生成器（6 个参数，范围 0-1）
        for i in range(6):
            self.toolbox.register(f"attr_{i}", random.uniform, 0, 1)
        
        # 注册个体生成器
        self.toolbox.register(
            "individual",
            tools.initCycle,
            creator.Individual,
            [getattr(self.toolbox, f"attr_{i}") for i in range(6)],
            n=1
        )
        
        # 注册种群生成器
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        
        # 注册适应度函数
        self.toolbox.register("evaluate", self.evaluate_fitness)
        
        # 注册选择算子（锦标赛选择）
        self.toolbox.register("select", tools.selTournament, tournsize=3)
        
        # 注册交叉算子（模拟二进制交叉）
        self.toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=0, up=1, eta=20)
        
        # 注册变异算子（多项式变异）
        self.toolbox.register("mutate", tools.mutPolynomialBounded, low=0, up=1, eta=20, indpb=0.1)
    
    def evaluate_fitness(self, individual: List[float]) -> tuple:
        """
        评估适应度
        
        需要根据实际性能数据计算
        这里使用模拟数据
        """
        strategy = LearningStrategy.from_genome(individual)
        
        # 模拟性能评估
        # 实际应用中应该从真实数据计算
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
        执行进化
        
        Returns:
            最优学习策略
        """
        # 创建初始种群
        if initial_population:
            population = [
                self.toolbox.individual()[0]
                for _ in range(self.population_size)
            ]
            # 用初始策略替换部分个体
            for i, strategy in enumerate(initial_population[:10]):
                if i < len(population):
                    population[i] = list(strategy.to_genome())
        else:
            population = [self.toolbox.individual()[0] for _ in range(self.population_size)]
        
        # 进化循环
        for generation in range(self.generations):
            # 评估适应度
            fitnesses = map(self.toolbox.evaluate, population)
            for ind, fit in zip(population, fitnesses):
                ind.fitness.values = fit
            
            # 选择、交叉、变异
            offspring = self.toolbox.select(population, len(population))
            offspring = list(map(self.toolbox.clone, offspring))
            
            # 交叉
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < 0.7:  # 交叉概率 70%
                    self.toolbox.mate(child1[0], child2[0])
                    del child1.fitness.values
                    del child2.fitness.values
            
            # 变异
            for mutant in offspring:
                if random.random() < 0.2:  # 变异概率 20%
                    self.toolbox.mutate(mutant[0])
                    del mutant.fitness.values
            
            # 替换种群
            population = [
                ind for ind in offspring
                if ind.fitness.valid
            ]
            
            # 记录这一代
            best_ind = tools.selBest(population, 1)[0]
            self.generations_history.append({
                "generation": generation,
                "best_fitness": best_ind.fitness.values[0],
                "best_genome": list(best_ind[0]),
                "timestamp": datetime.now().isoformat(),
            })
            
            self.current_generation = generation
            
            print(f"🧬 第 {generation} 代：最佳适应度 = {best_ind.fitness.values[0]:.4f}")
        
        # 返回最优策略
        best_ind = tools.selBest(population, 1)[0]
        best_strategy = LearningStrategy.from_genome(
            list(best_ind[0]),
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
