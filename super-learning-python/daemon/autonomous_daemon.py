#!/usr/bin/env python3
"""
自主学习守护进程

完全自动化运行，无需人工干预
自动分辨 → 判断 → 吸收 → 壮大 → 健硕 → 成熟 → 循环
"""

import os
import sys
import time
import json
import signal
import atexit
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from autonomous.learner import AutonomousLearner
from data_collector.collector import DataCollector
from search.nested_search import NestedSearchEngine


class AutonomousDaemon:
    """
    自主学习守护进程
    
    自动运行：
    - 每 5 分钟：检查新数据
    - 每 30 分钟：运行学习循环
    - 每 1 小时：评估成熟度
    - 每 24 小时：生成报告
    """
    
    def __init__(self, config_path: str = None):
        """
        初始化守护进程
        
        Args:
            config_path: 配置文件路径
        """
        if config_path is None:
            config_path = os.path.expanduser(
                '~/.openclaw/super_learning/daemon_config.json'
            )
        
        self.config_path = config_path
        self.config = self._load_config()
        
        # 核心组件
        self.learner = AutonomousLearner()
        self.collector = DataCollector()
        self.search_engine = NestedSearchEngine()
        
        # 运行状态
        self.running = False
        self.last_check = None
        self.last_cycle = None
        self.last_report = None
        
        # 注册退出处理
        atexit.register(self._cleanup)
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _load_config(self) -> dict:
        """加载配置"""
        default_config = {
            'check_interval': 300,       # 5 分钟
            'cycle_interval': 1800,      # 30 分钟
            'report_interval': 86400,    # 24 小时
            'min_data_points': 10,       # 最小数据点
            'auto_start': True,          # 自动启动
            'log_path': os.path.expanduser(
                '~/.openclaw/super_learning/daemon.log'
            ),
        }
        
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                default_config.update(config)
        
        return default_config
    
    def _save_config(self):
        """保存配置"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def _log(self, message: str, level: str = 'INFO'):
        """日志记录"""
        timestamp = datetime.now().isoformat()
        log_line = f"[{timestamp}] [{level}] {message}\n"
        
        log_path = self.config['log_path']
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(log_line)
        
        print(log_line.strip())
    
    def _signal_handler(self, signum, frame):
        """信号处理"""
        self._log(f"收到信号 {signum}，准备退出", 'WARN')
        self.running = False
    
    def _cleanup(self):
        """清理资源"""
        self._log("守护进程退出", 'INFO')
    
    def check_new_data(self) -> int:
        """
        检查新数据
        
        Returns:
            新数据数量
        """
        now = datetime.now()
        
        # 获取上次检查时间
        if self.last_check:
            start_time = self.last_check.isoformat()
        else:
            # 第一次运行，获取最近 1 小时的数据
            start_time = (now - timedelta(hours=1)).isoformat()
        
        # 搜索新数据
        queries = [
            {
                'filters': {
                    'timestamp_gte': start_time,
                }
            }
        ]
        
        results = self.search_engine.search(
            queries=queries,
            max_depth=1,
            min_precision=0.0,
        )
        
        new_count = len(results)
        
        if new_count > 0:
            self._log(f"发现 {new_count} 条新数据", 'INFO')
        
        self.last_check = now
        
        return new_count
    
    def run_learning_cycle(self) -> dict:
        """
        运行学习循环
        
        Returns:
            循环结果
        """
        self._log("开始学习循环", 'INFO')
        
        # 获取数据
        events = self.collector.get_events(limit=100)
        
        if len(events) < self.config['min_data_points']:
            self._log(
                f"数据不足 ({len(events)}/{self.config['min_data_points']})",
                'WARN'
            )
            return {'status': 'insufficient_data'}
        
        # 准备输入数据
        inputs = []
        for event in events[:50]:  # 限制数量
            inputs.append({
                'event_type': event.get('event_type'),
                'performance_score': event.get('performance_score', 0),
                'timestamp': event.get('timestamp'),
                'context': event.get('context', {}),
                'result': event.get('result'),
            })
        
        # 运行完整循环
        result = self.learner.run_full_cycle(inputs)
        
        self.last_cycle = datetime.now()
        
        self._log(
            f"学习循环完成，成熟度：{result.get('maturity_score', 0):.2f}",
            'INFO'
        )
        
        return result
    
    def generate_report(self) -> str:
        """
        生成报告
        
        Returns:
            报告路径
        """
        now = datetime.now()
        
        # 获取进度报告
        progress = self.learner.get_progress_report()
        
        # 生成报告内容
        report = {
            'generated_at': now.isoformat(),
            'uptime_hours': (now - self.last_cycle).total_seconds() / 3600 if self.last_cycle else 0,
            'progress': progress,
            'config': self.config,
        }
        
        # 保存报告
        report_path = os.path.expanduser(
            f'~/.openclaw/super_learning/reports/report_{now.strftime("%Y%m%d_%H%M%S")}.json'
        )
        
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        self.last_report = now
        
        self._log(f"报告已生成：{report_path}", 'INFO')
        
        return report_path
    
    def run(self):
        """运行守护进程"""
        self._log("=" * 50)
        self._log("自主学习守护进程启动")
        self._log(f"配置：检查间隔={self.config['check_interval']}s")
        self._log("=" * 50)
        
        self.running = True
        
        while self.running:
            try:
                now = datetime.now()
                
                # 1. 检查新数据 (每 5 分钟)
                new_data = self.check_new_data()
                
                # 2. 运行学习循环 (每 30 分钟且有新数据)
                if (
                    new_data > 0 and
                    self.last_cycle and
                    (now - self.last_cycle).total_seconds() >= self.config['cycle_interval']
                ):
                    self.run_learning_cycle()
                elif not self.last_cycle:
                    # 第一次运行
                    self.run_learning_cycle()
                
                # 3. 生成报告 (每 24 小时)
                if (
                    self.last_report and
                    (now - self.last_report).total_seconds() >= self.config['report_interval']
                ):
                    self.generate_report()
                elif not self.last_report:
                    # 第一次运行，1 分钟后生成报告
                    if (now - self.last_cycle).total_seconds() > 60:
                        self.generate_report()
                
                # 等待
                time.sleep(self.config['check_interval'])
                
            except KeyboardInterrupt:
                self._log("收到中断信号", 'WARN')
                break
            except Exception as e:
                self._log(f"错误：{e}", 'ERROR')
                time.sleep(60)  # 错误后等待 1 分钟
        
        self._log("守护进程停止", 'INFO')


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='自主学习守护进程')
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='配置文件路径'
    )
    parser.add_argument(
        '--foreground',
        action='store_true',
        help='前台运行'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='显示状态'
    )
    
    args = parser.parse_args()
    
    # 显示状态
    if args.status:
        status_path = os.path.expanduser(
            '~/.openclaw/super_learning/daemon_status.json'
        )
        
        if os.path.exists(status_path):
            with open(status_path, 'r', encoding='utf-8') as f:
                status = json.load(f)
                print(json.dumps(status, indent=2, ensure_ascii=False))
        else:
            print("守护进程未运行")
        return
    
    # 创建守护进程
    daemon = AutonomousDaemon(config_path=args.config)
    
    if args.foreground:
        # 前台运行
        daemon.run()
    else:
        # 后台运行
        import daemon as python_daemon
        
        with python_daemon.DaemonContext():
            daemon.run()


if __name__ == '__main__':
    main()
