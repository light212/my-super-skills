"""
智能 Grep 工具

用于快速搜索学习数据、模式、Agent 行为等
支持正则表达式、模糊匹配、语义搜索
"""

import re
import os
import json
import sqlite3
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass
class SearchMatch:
    """搜索结果"""
    source: str
    match_type: str  # exact, regex, fuzzy, semantic
    content: str
    context: str
    score: float
    metadata: Dict[str, Any]


class SmartGrep:
    """
    智能 Grep 工具
    
    支持多种搜索模式
    """
    
    def __init__(self, db_path: str = None):
        """
        初始化智能 Grep
        
        Args:
            db_path: 数据库路径
        """
        if db_path is None:
            db_path = os.path.expanduser(
                '~/.openclaw/super_learning/data.db'
            )
        
        self.db_path = db_path
        self.cache: Dict[str, List[Dict]] = {}
    
    def search(
        self,
        query: str,
        search_type: str = 'auto',
        limit: int = 50,
        **kwargs,
    ) -> List[SearchMatch]:
        """
        智能搜索
        
        Args:
            query: 搜索查询
            search_type: 搜索类型 (auto, exact, regex, fuzzy, semantic)
            limit: 返回数量限制
        
        Returns:
            搜索结果列表
        """
        if search_type == 'auto':
            # 自动选择搜索类型
            search_type = self._detect_search_type(query)
        
        if search_type == 'regex':
            return self._regex_search(query, limit, **kwargs)
        elif search_type == 'fuzzy':
            return self._fuzzy_search(query, limit, **kwargs)
        elif search_type == 'semantic':
            return self._semantic_search(query, limit, **kwargs)
        else:  # exact
            return self._exact_search(query, limit, **kwargs)
    
    def _detect_search_type(self, query: str) -> str:
        """检测搜索类型"""
        # 包含正则特殊字符
        if any(c in query for c in '.*+?^${}()|[]\\'):
            return 'regex'
        
        # 包含空格，可能是模糊搜索
        if ' ' in query and len(query.split()) > 2:
            return 'fuzzy'
        
        # 默认精确搜索
        return 'exact'
    
    def _exact_search(
        self,
        query: str,
        limit: int,
        case_sensitive: bool = False,
    ) -> List[SearchMatch]:
        """
        精确搜索
        
        Args:
            query: 搜索查询
            limit: 返回数量限制
            case_sensitive: 是否区分大小写
        
        Returns:
            搜索结果
        """
        results = []
        
        # 搜索数据库
        if os.path.exists(self.db_path):
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 搜索学习事件
            like_query = f'%{query}%' if not case_sensitive else query
            
            cursor.execute('''
                SELECT * FROM learning_events
                WHERE context LIKE ? OR result LIKE ?
                LIMIT ?
            ''', (like_query, like_query, limit))
            
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            for row in rows:
                event = dict(zip(columns, row))
                
                # 解析 JSON 字段
                for field in ['context', 'result']:
                    if event.get(field):
                        try:
                            event[field] = json.loads(event[field])
                        except json.JSONDecodeError:
                            pass
                
                results.append(SearchMatch(
                    source='learning_events',
                    match_type='exact',
                    content=json.dumps(event, ensure_ascii=False),
                    context=str(event.get('event_type', '')),
                    score=1.0,
                    metadata=event,
                ))
            
            conn.close()
        
        # 搜索模式文件
        patterns_file = os.path.expanduser(
            '~/.openclaw/super_learning/patterns.json'
        )
        
        if os.path.exists(patterns_file):
            with open(patterns_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                for pattern in data.get('patterns', []):
                    pattern_str = json.dumps(pattern, ensure_ascii=False)
                    
                    if (case_sensitive and query in pattern_str) or \
                       (not case_sensitive and query.lower() in pattern_str.lower()):
                        results.append(SearchMatch(
                            source='patterns',
                            match_type='exact',
                            content=pattern_str,
                            context=pattern.get('type', ''),
                            score=1.0,
                            metadata=pattern,
                        ))
        
        return results[:limit]
    
    def _regex_search(
        self,
        pattern: str,
        limit: int,
        **kwargs,
    ) -> List[SearchMatch]:
        """
        正则表达式搜索
        
        Args:
            pattern: 正则表达式
            limit: 返回数量限制
        
        Returns:
            搜索结果
        """
        results = []
        
        try:
            regex = re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
        
        # 搜索数据库
        if os.path.exists(self.db_path):
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM learning_events LIMIT 1000')
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            for row in rows[:limit]:
                event = dict(zip(columns, row))
                event_str = json.dumps(event, ensure_ascii=False)
                
                if regex.search(event_str):
                    results.append(SearchMatch(
                        source='learning_events',
                        match_type='regex',
                        content=event_str,
                        context=str(event.get('event_type', '')),
                        score=1.0,
                        metadata=event,
                    ))
            
            conn.close()
        
        return results[:limit]
    
    def _fuzzy_search(
        self,
        query: str,
        limit: int,
        threshold: float = 0.6,
        **kwargs,
    ) -> List[SearchMatch]:
        """
        模糊搜索
        
        Args:
            query: 搜索查询
            limit: 返回数量限制
            threshold: 匹配阈值 (0-1)
        
        Returns:
            搜索结果
        """
        results = []
        
        # 搜索数据库
        if os.path.exists(self.db_path):
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM learning_events LIMIT 1000')
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            for row in rows:
                event = dict(zip(columns, row))
                event_str = json.dumps(event, ensure_ascii=False)
                
                # 计算相似度
                similarity = SequenceMatcher(None, query.lower(), event_str.lower()).ratio()
                
                if similarity >= threshold:
                    results.append(SearchMatch(
                        source='learning_events',
                        match_type='fuzzy',
                        content=event_str,
                        context=str(event.get('event_type', '')),
                        score=similarity,
                        metadata=event,
                    ))
            
            conn.close()
        
        # 按相似度排序
        results.sort(key=lambda x: x.score, reverse=True)
        
        return results[:limit]
    
    def _semantic_search(
        self,
        query: str,
        limit: int,
        **kwargs,
    ) -> List[SearchMatch]:
        """
        语义搜索 (简化版)
        
        Args:
            query: 搜索查询
            limit: 返回数量限制
        
        Returns:
            搜索结果
        """
        # 简化实现：使用关键词匹配
        # 实际应该使用向量搜索
        
        keywords = query.lower().split()
        
        results = []
        
        if os.path.exists(self.db_path):
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM learning_events LIMIT 1000')
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            for row in rows:
                event = dict(zip(columns, row))
                event_str = json.dumps(event, ensure_ascii=False).lower()
                
                # 计算关键词匹配数
                match_count = sum(1 for kw in keywords if kw in event_str)
                score = match_count / len(keywords) if keywords else 0
                
                if score > 0:
                    results.append(SearchMatch(
                        source='learning_events',
                        match_type='semantic',
                        content=event_str,
                        context=str(event.get('event_type', '')),
                        score=score,
                        metadata=event,
                    ))
            
            conn.close()
        
        # 按匹配度排序
        results.sort(key=lambda x: x.score, reverse=True)
        
        return results[:limit]
    
    def search_events(
        self,
        event_type: str = None,
        agent_id: str = None,
        min_score: float = None,
        date_range: Tuple[str, str] = None,
        limit: int = 100,
    ) -> List[Dict]:
        """
        搜索学习事件
        
        Args:
            event_type: 事件类型
            agent_id: Agent ID
            min_score: 最小分数
            date_range: 日期范围 (start, end)
            limit: 返回数量限制
        
        Returns:
            事件列表
        """
        if not os.path.exists(self.db_path):
            return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = 'SELECT * FROM learning_events WHERE 1=1'
        params = []
        
        if event_type:
            query += ' AND event_type = ?'
            params.append(event_type)
        
        if agent_id:
            query += ' AND agent_id = ?'
            params.append(agent_id)
        
        if min_score is not None:
            query += ' AND performance_score >= ?'
            params.append(min_score)
        
        if date_range:
            query += ' AND timestamp >= ? AND timestamp <= ?'
            params.extend(date_range)
        
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
    
    def export_results(
        self,
        results: List[SearchMatch],
        output_path: str,
        format: str = 'json',
    ):
        """
        导出搜索结果
        
        Args:
            results: 搜索结果
            output_path: 输出路径
            format: 输出格式 (json, csv, text)
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump([
                    {
                        'source': r.source,
                        'match_type': r.match_type,
                        'content': r.content,
                        'score': r.score,
                        'metadata': r.metadata,
                    }
                    for r in results
                ], f, ensure_ascii=False, indent=2)
        
        elif format == 'csv':
            import csv
            
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['source', 'match_type', 'content', 'score'])
                
                for r in results:
                    writer.writerow([r.source, r.match_type, r.content, r.score])
        
        elif format == 'text':
            with open(output_path, 'w', encoding='utf-8') as f:
                for r in results:
                    f.write(f"[{r.match_type}] {r.source}: {r.content}\n")
                    f.write(f"Score: {r.score}\n\n")
        
        print(f"✅ 结果已导出到：{output_path}")


# 使用示例
if __name__ == "__main__":
    grep = SmartGrep()
    
    # 精确搜索
    print("🔍 精确搜索 'mirror'")
    results = grep.search('mirror', search_type='exact', limit=5)
    for r in results:
        print(f"  [{r.match_type}] {r.source}: {r.context} (score: {r.score})")
    
    # 正则搜索
    print("\n🔍 正则搜索 'event_type.*clone'")
    results = grep.search('event_type.*clone', search_type='regex', limit=5)
    for r in results:
        print(f"  [{r.match_type}] {r.source}: {r.context}")
    
    # 模糊搜索
    print("\n🔍 模糊搜索 'learning strategy'")
    results = grep.search('learning strategy', search_type='fuzzy', limit=5)
    for r in results[:3]:
        print(f"  [{r.match_type}] {r.source}: {r.context} (score: {r.score:.2f})")
    
    # 搜索事件
    print("\n🔍 搜索 clone 事件")
    events = grep.search_events(event_type='clone', min_score=0.8, limit=5)
    for event in events:
        print(f"  {event['agent_id']}: {event['performance_score']}")
