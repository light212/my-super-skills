"""
数据收集模块

收集真实学习数据，用于优化算法
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import sqlite3


@dataclass
class LearningEvent:
    """学习事件"""
    event_type: str  # clone, mirror, transfer, learn
    agent_id: str
    timestamp: str
    context: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    performance_score: float = 0.0


class DataCollector:
    """
    数据收集器
    
    收集真实学习数据，存储到 SQLite 数据库
    """
    
    def __init__(self, db_path: str = None):
        """
        初始化数据收集器
        
        Args:
            db_path: 数据库路径，默认使用环境变量或默认路径
        """
        if db_path is None:
            db_path = os.environ.get(
                'SUPER_LEARNING_DB',
                os.path.expanduser('~/.openclaw/super_learning/data.db')
            )
        
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        # 确保目录存在
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建学习事件表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                context TEXT,
                result TEXT,
                performance_score REAL DEFAULT 0.0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建 Agent 表现表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agent_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL UNIQUE,
                total_events INTEGER DEFAULT 0,
                avg_score REAL DEFAULT 0.0,
                best_score REAL DEFAULT 0.0,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建策略效果表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS strategy_effectiveness (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy_params TEXT NOT NULL,
                event_count INTEGER DEFAULT 0,
                avg_score REAL DEFAULT 0.0,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_event(self, event: LearningEvent):
        """
        记录学习事件
        
        Args:
            event: 学习事件
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO learning_events
            (event_type, agent_id, timestamp, context, result, performance_score)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            event.event_type,
            event.agent_id,
            event.timestamp,
            json.dumps(event.context),
            json.dumps(event.result) if event.result else None,
            event.performance_score,
        ))
        
        # 更新 Agent 表现
        cursor.execute('''
            INSERT OR REPLACE INTO agent_performance
            (agent_id, total_events, avg_score, best_score, last_updated)
            SELECT 
                ?,
                COALESCE((SELECT total_events FROM agent_performance WHERE agent_id = ?), 0) + 1,
                (
                    SELECT AVG(performance_score) 
                    FROM learning_events 
                    WHERE agent_id = ?
                ),
                MAX(?, COALESCE((SELECT best_score FROM agent_performance WHERE agent_id = ?), 0)),
                CURRENT_TIMESTAMP
            FROM learning_events
            WHERE agent_id = ?
        ''', (
            event.agent_id,
            event.agent_id,
            event.agent_id,
            event.performance_score,
            event.agent_id,
            event.agent_id,
        ))
        
        conn.commit()
        conn.close()
    
    def get_events(
        self,
        agent_id: str = None,
        event_type: str = None,
        start_date: str = None,
        end_date: str = None,
        limit: int = 100,
    ) -> List[Dict]:
        """
        获取学习事件
        
        Args:
            agent_id: Agent ID
            event_type: 事件类型
            start_date: 开始日期
            end_date: 结束日期
            limit: 返回数量限制
        
        Returns:
            事件列表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT * FROM learning_events WHERE 1=1'
        params = []
        
        if agent_id:
            query += ' AND agent_id = ?'
            params.append(agent_id)
        
        if event_type:
            query += ' AND event_type = ?'
            params.append(event_type)
        
        if start_date:
            query += ' AND timestamp >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND timestamp <= ?'
            params.append(end_date)
        
        query += ' ORDER BY timestamp DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        events = [dict(zip(columns, row)) for row in rows]
        
        # 解析 JSON 字段
        for event in events:
            if event.get('context'):
                event['context'] = json.loads(event['context'])
            if event.get('result'):
                event['result'] = json.loads(event['result'])
        
        conn.close()
        return events
    
    def get_agent_stats(self, agent_id: str) -> Optional[Dict]:
        """
        获取 Agent 统计
        
        Args:
            agent_id: Agent ID
        
        Returns:
            统计数据
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM agent_performance WHERE agent_id = ?
        ''', (agent_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        
        return None
    
    def get_all_agents_stats(self) -> List[Dict]:
        """
        获取所有 Agent 统计
        
        Returns:
            统计数据列表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM agent_performance ORDER BY avg_score DESC')
        rows = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        stats = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        return stats
    
    def export_data(self, output_path: str):
        """
        导出数据到 JSON 文件
        
        Args:
            output_path: 输出文件路径
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 导出所有事件
        cursor.execute('SELECT * FROM learning_events ORDER BY timestamp')
        events = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        events_list = [dict(zip(columns, row)) for row in events]
        
        # 解析 JSON 字段
        for event in events_list:
            if event.get('context'):
                event['context'] = json.loads(event['context'])
            if event.get('result'):
                event['result'] = json.loads(event['result'])
        
        # 导出 Agent 统计
        cursor.execute('SELECT * FROM agent_performance')
        agents = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        agents_list = [dict(zip(columns, row)) for row in agents]
        
        # 写入 JSON 文件
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'events': events_list,
                'agents': agents_list,
                'exported_at': datetime.now().isoformat(),
            }, f, ensure_ascii=False, indent=2)
        
        conn.close()
        
        print(f"✅ 数据已导出到：{output_path}")
        print(f"   事件数：{len(events_list)}")
        print(f"   Agent 数：{len(agents_list)}")


# 使用示例
if __name__ == "__main__":
    collector = DataCollector()
    
    # 记录事件
    event = LearningEvent(
        event_type='clone',
        agent_id='ceo-1',
        timestamp=datetime.now().isoformat(),
        context={
            'template': 'ceo-template',
            'role': 'CEO',
        },
        result={
            'success': True,
            'duration_ms': 1500,
        },
        performance_score=0.85,
    )
    
    collector.record_event(event)
    print("✅ 事件已记录")
    
    # 获取统计
    stats = collector.get_agent_stats('ceo-1')
    print(f"📊 Agent 统计：{stats}")
    
    # 导出数据
    collector.export_data('/tmp/super_learning_data.json')
