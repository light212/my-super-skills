"""
数据分析与优化模块

基于真实数据优化学习策略
"""

import json
import numpy as np
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
from data_collector.collector import DataCollector


class DataAnalyzer:
    """
    数据分析师
    
    分析学习数据，发现模式和趋势
    """
    
    def __init__(self, collector: DataCollector):
        """
        初始化分析师
        
        Args:
            collector: 数据收集器
        """
        self.collector = collector
    
    def analyze_event_types(self) -> Dict[str, Any]:
        """
        分析事件类型分布
        
        Returns:
            事件类型统计
        """
        events = self.collector.get_events(limit=1000)
        
        if not events:
            return {'error': 'No events found'}
        
        # 统计事件类型
        type_counts = {}
        type_scores = {}
        
        for event in events:
            event_type = event['event_type']
            score = event.get('performance_score', 0.0)
            
            if event_type not in type_counts:
                type_counts[event_type] = 0
                type_scores[event_type] = []
            
            type_counts[event_type] += 1
            type_scores[event_type].append(score)
        
        # 计算平均分
        type_avg_scores = {
            event_type: np.mean(scores) if scores else 0.0
            for event_type, scores in type_scores.items()
        }
        
        # 排序
        sorted_types = sorted(
            type_counts.items(),
            key=lambda x: type_avg_scores.get(x[0], 0),
            reverse=True,
        )
        
        return {
            'total_events': len(events),
            'type_distribution': dict(sorted_types),
            'type_avg_scores': type_avg_scores,
            'best_type': sorted_types[0][0] if sorted_types else None,
        }
    
    def analyze_time_patterns(self) -> Dict[str, Any]:
        """
        分析时间模式
        
        Returns:
            时间模式统计
        """
        events = self.collector.get_events(limit=1000)
        
        if not events:
            return {'error': 'No events found'}
        
        # 按小时统计
        hour_scores = {hour: [] for hour in range(24)}
        day_scores = {day: [] for day in range(7)}
        
        for event in events:
            try:
                timestamp = datetime.fromisoformat(event['timestamp'])
                hour = timestamp.hour
                day = timestamp.weekday()
                score = event.get('performance_score', 0.0)
                
                hour_scores[hour].append(score)
                day_scores[day].append(score)
            except (ValueError, KeyError):
                continue
        
        # 计算平均分
        hour_avg = {
            hour: np.mean(scores) if scores else 0.0
            for hour, scores in hour_scores.items()
        }
        
        day_avg = {
            day: np.mean(scores) if scores else 0.0
            for day, scores in day_scores.items()
        }
        
        # 找出最佳时间
        best_hour = max(hour_avg.items(), key=lambda x: x[1])[0]
        best_day = max(day_avg.items(), key=lambda x: x[1])[0]
        
        return {
            'best_hour': best_hour,
            'best_day': best_day,
            'hourly_pattern': hour_avg,
            'daily_pattern': day_avg,
        }
    
    def analyze_agent_performance(self) -> Dict[str, Any]:
        """
        分析 Agent 表现
        
        Returns:
            Agent 表现统计
        """
        agents = self.collector.get_all_agents_stats()
        
        if not agents:
            return {'error': 'No agents found'}
        
        # 排序
        sorted_agents = sorted(
            agents,
            key=lambda x: x.get('avg_score', 0),
            reverse=True,
        )
        
        # 计算统计
        scores = [agent.get('avg_score', 0) for agent in agents]
        
        return {
            'total_agents': len(agents),
            'avg_score': np.mean(scores) if scores else 0.0,
            'best_agent': sorted_agents[0] if sorted_agents else None,
            'worst_agent': sorted_agents[-1] if sorted_agents else None,
            'top_agents': sorted_agents[:5],
        }
    
    def generate_insights(self) -> List[Dict[str, Any]]:
        """
        生成洞察
        
        Returns:
            洞察列表
        """
        insights = []
        
        # 分析事件类型
        event_analysis = self.analyze_event_types()
        if 'error' not in event_analysis:
            best_type = event_analysis.get('best_type')
            if best_type:
                insights.append({
                    'type': 'event_type',
                    'insight': f'最佳学习方式是 {best_type}',
                    'confidence': 0.8,
                    'action': f'增加{best_type}的使用频率',
                })
        
        # 分析时间模式
        time_analysis = self.analyze_time_patterns()
        if 'error' not in time_analysis:
            best_hour = time_analysis.get('best_hour')
            if best_hour is not None:
                insights.append({
                    'type': 'time_pattern',
                    'insight': f'最佳学习时间是 {best_hour}:00',
                    'confidence': 0.7,
                    'action': f'在{best_hour}:00 左右安排重要学习',
                })
        
        # 分析 Agent 表现
        agent_analysis = self.analyze_agent_performance()
        if 'error' not in agent_analysis:
            best_agent = agent_analysis.get('best_agent')
            if best_agent:
                insights.append({
                    'type': 'agent_performance',
                    'insight': f'{best_agent["agent_id"]} 表现最佳',
                    'confidence': 0.9,
                    'action': f'学习{best_agent["agent_id"]}的策略',
                })
        
        return insights


class StrategyOptimizer:
    """
    策略优化器
    
    基于数据优化学习策略
    """
    
    def __init__(self, collector: DataCollector, analyzer: DataAnalyzer):
        """
        初始化优化器
        
        Args:
            collector: 数据收集器
            analyzer: 数据分析师
        """
        self.collector = collector
        self.analyzer = analyzer
    
    def optimize_parameters(self) -> Dict[str, float]:
        """
        优化策略参数
        
        Returns:
            优化后的参数
        """
        # 获取洞察
        insights = self.analyzer.generate_insights()
        
        # 基于洞察调整参数
        optimized = {
            'learning_rate': 0.5,
            'transfer_frequency': 0.5,
            'detection_threshold': 0.5,
            'mirror_weight': 0.33,
            'clone_weight': 0.33,
            'transfer_weight': 0.34,
        }
        
        for insight in insights:
            if insight['type'] == 'event_type':
                # 根据最佳事件类型调整权重
                best_type = insight.get('insight', '').split()[-1]
                
                if 'mirror' in best_type:
                    optimized['mirror_weight'] = min(1.0, optimized['mirror_weight'] + 0.2)
                elif 'clone' in best_type:
                    optimized['clone_weight'] = min(1.0, optimized['clone_weight'] + 0.2)
                elif 'transfer' in best_type:
                    optimized['transfer_weight'] = min(1.0, optimized['transfer_weight'] + 0.2)
                    optimized['transfer_frequency'] = min(1.0, optimized['transfer_frequency'] + 0.1)
            
            elif insight['type'] == 'time_pattern':
                # 根据最佳时间调整检测阈值
                optimized['detection_threshold'] = max(0.1, optimized['detection_threshold'] - 0.1)
            
            elif insight['type'] == 'agent_performance':
                # 学习最佳 Agent 的策略
                optimized['learning_rate'] = min(1.0, optimized['learning_rate'] + 0.1)
        
        return optimized
    
    def generate_report(self) -> Dict[str, Any]:
        """
        生成优化报告
        
        Returns:
            优化报告
        """
        report = {
            'generated_at': datetime.now().isoformat(),
            'data_summary': {
                'total_events': len(self.collector.get_events(limit=10000)),
                'total_agents': len(self.collector.get_all_agents_stats()),
            },
            'insights': self.analyzer.generate_insights(),
            'optimized_parameters': self.optimize_parameters(),
            'recommendations': [],
        }
        
        # 生成建议
        insights = report['insights']
        
        if len(insights) > 0:
            report['recommendations'].append({
                'priority': 'high',
                'action': '应用优化后的参数',
                'expected_improvement': '10-20%',
            })
        
        if report['data_summary']['total_events'] < 100:
            report['recommendations'].append({
                'priority': 'medium',
                'action': '收集更多数据',
                'reason': '当前数据量不足，建议至少收集 100 个事件',
            })
        
        return report


# 使用示例
if __name__ == "__main__":
    collector = DataCollector()
    analyzer = DataAnalyzer(collector)
    optimizer = StrategyOptimizer(collector, analyzer)
    
    # 生成报告
    report = optimizer.generate_report()
    
    print("📊 优化报告")
    print(f"生成时间：{report['generated_at']}")
    print(f"数据量：{report['data_summary']['total_events']} 个事件")
    print(f"Agent 数：{report['data_summary']['total_agents']} 个")
    print(f"洞察数：{len(report['insights'])} 个")
    print(f"建议数：{len(report['recommendations'])} 个")
    
    print("\n🔧 优化参数:")
    for key, value in report['optimized_parameters'].items():
        print(f"  {key}: {value:.3f}")
    
    print("\n💡 洞察:")
    for insight in report['insights']:
        print(f"  - {insight['insight']} (置信度：{insight['confidence']:.0%})")
    
    print("\n📝 建议:")
    for rec in report['recommendations']:
        print(f"  [{rec['priority']}] {rec['action']}")
