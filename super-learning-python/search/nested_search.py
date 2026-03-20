"""
嵌套搜索精准定位系统

支持多层级、多维度、递归搜索，精准定位目标
"""

import os
import json
import re
import sqlite3
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class SearchNode:
    """搜索节点"""
    level: int
    query: str
    search_type: str
    results: List[Dict] = field(default_factory=list)
    children: List['SearchNode'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NestedSearchResult:
    """嵌套搜索结果"""
    query_tree: SearchNode
    total_matches: int
    precision_score: float
    path: List[str]
    content: Dict[str, Any]
    context: str
    relevance_score: float


class NestedSearchEngine:
    """
    嵌套搜索引擎
    
    支持：
    - 多层级搜索
    - 多维度过滤
    - 递归定位
    - 精准匹配
    """
    
    def __init__(self, db_path: str = None):
        """
        初始化嵌套搜索引擎
        
        Args:
            db_path: 数据库路径
        """
        if db_path is None:
            db_path = os.path.expanduser(
                '~/.openclaw/super_learning/data.db'
            )
        
        self.db_path = db_path
        self.cache: Dict[str, NestedSearchResult] = {}
    
    def search(
        self,
        queries: Union[str, List[Union[str, Dict]]],
        max_depth: int = 3,
        min_precision: float = 0.7,
    ) -> List[NestedSearchResult]:
        """
        嵌套搜索
        
        Args:
            queries: 查询列表，可以是：
                - 字符串：精确查询
                - 字典：{query: str, type: str, filters: dict}
            max_depth: 最大嵌套深度
            min_precision: 最小精度阈值
        
        Returns:
            搜索结果列表
        """
        # 构建查询树
        if isinstance(queries, str):
            queries = [queries]
        
        root_node = SearchNode(
            level=0,
            query='root',
            search_type='root',
        )
        
        # 执行嵌套搜索
        results = self._recursive_search(
            node=root_node,
            queries=queries,
            depth=0,
            max_depth=max_depth,
        )
        
        # 过滤低精度结果
        filtered_results = [
            r for r in results
            if r.precision_score >= min_precision
        ]
        
        # 按精度排序
        filtered_results.sort(key=lambda x: x.precision_score, reverse=True)
        
        return filtered_results
    
    def _recursive_search(
        self,
        node: SearchNode,
        queries: List[Union[str, Dict]],
        depth: int,
        max_depth: int,
    ) -> List[NestedSearchResult]:
        """
        递归搜索
        
        Args:
            node: 当前搜索节点
            queries: 查询列表
            depth: 当前深度
            max_depth: 最大深度
        
        Returns:
            搜索结果列表
        """
        results = []
        
        # 基础情况：达到最大深度或没有更多查询
        if depth >= max_depth or not queries:
            return self._finalize_search(node)
        
        # 处理当前查询
        current_query = queries[0]
        remaining_queries = queries[1:]
        
        # 解析查询
        if isinstance(current_query, str):
            query_str = current_query
            search_type = 'exact'
            filters = {}
        else:
            query_str = current_query.get('query', '')
            search_type = current_query.get('type', 'exact')
            filters = current_query.get('filters', {})
        
        # 执行搜索
        search_results = self._execute_search(
            query=query_str,
            search_type=search_type,
            filters=filters,
            context=node.results if node.results else None,
        )
        
        # 更新节点
        node.query = query_str
        node.search_type = search_type
        node.results = search_results
        
        # 如果没有结果，剪枝
        if not search_results:
            return []
        
        # 如果有剩余查询，继续递归
        if remaining_queries:
            for result in search_results[:10]:  # 限制分支数量
                child_node = SearchNode(
                    level=depth + 1,
                    query=query_str,
                    search_type=search_type,
                    metadata=result,
                )
                
                node.children.append(child_node)
                
                # 递归搜索
                child_results = self._recursive_search(
                    node=child_node,
                    queries=remaining_queries,
                    depth=depth + 1,
                    max_depth=max_depth,
                )
                
                results.extend(child_results)
        else:
            # 没有剩余查询，finalize
            results = self._finalize_search(node)
        
        return results
    
    def _execute_search(
        self,
        query: str,
        search_type: str,
        filters: Dict[str, Any],
        context: List[Dict] = None,
    ) -> List[Dict]:
        """
        执行搜索
        
        Args:
            query: 查询字符串
            search_type: 搜索类型
            filters: 过滤器
            context: 上下文（用于嵌套搜索）
        
        Returns:
            搜索结果
        """
        if context:
            # 在上下文中搜索
            return self._search_in_context(
                query=query,
                search_type=search_type,
                filters=filters,
                context=context,
            )
        else:
            # 在数据库中搜索
            return self._search_in_database(
                query=query,
                search_type=search_type,
                filters=filters,
            )
    
    def _search_in_database(
        self,
        query: str,
        search_type: str,
        filters: Dict[str, Any],
    ) -> List[Dict]:
        """
        在数据库中搜索
        
        Args:
            query: 查询字符串
            search_type: 搜索类型
            filters: 过滤器
        
        Returns:
            搜索结果
        """
        if not os.path.exists(self.db_path):
            return []
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 构建查询
        base_query = 'SELECT * FROM learning_events WHERE 1=1'
        params = []
        
        # 添加过滤器
        for key, value in filters.items():
            if isinstance(value, (int, float)):
                base_query += f' AND {key} = ?'
                params.append(value)
            elif isinstance(value, str):
                base_query += f' AND {key} LIKE ?'
                params.append(f'%{value}%')
        
        # 添加查询条件
        if search_type == 'regex':
            # SQLite 不支持正则，使用 LIKE 近似
            base_query += ' AND (context LIKE ? OR result LIKE ?)'
            params.extend([f'%{query}%', f'%{query}%'])
        else:
            base_query += ' AND (context LIKE ? OR result LIKE ?)'
            params.extend([f'%{query}%', f'%{query}%'])
        
        # 限制结果数量
        base_query += ' LIMIT 100'
        
        cursor.execute(base_query, params)
        rows = cursor.fetchall()
        
        results = [dict(row) for row in rows]
        
        # 解析 JSON 字段
        for result in results:
            for field in ['context', 'result']:
                if result.get(field):
                    try:
                        result[field] = json.loads(result[field])
                    except json.JSONDecodeError:
                        pass
        
        conn.close()
        return results
    
    def _search_in_context(
        self,
        query: str,
        search_type: str,
        filters: Dict[str, Any],
        context: List[Dict],
    ) -> List[Dict]:
        """
        在上下文中搜索
        
        Args:
            query: 查询字符串
            search_type: 搜索类型
            filters: 过滤器
            context: 上下文
        
        Returns:
            搜索结果
        """
        results = []
        
        for item in context:
            # 应用过滤器
            if not self._matches_filters(item, filters):
                continue
            
            # 执行搜索
            if self._matches_query(item, query, search_type):
                results.append(item)
        
        return results
    
    def _matches_filters(self, item: Dict, filters: Dict[str, Any]) -> bool:
        """
        检查是否匹配过滤器
        
        Args:
            item: 项目
            filters: 过滤器
        
        Returns:
            是否匹配
        """
        for key, value in filters.items():
            item_value = item.get(key)
            
            if item_value is None:
                return False
            
            if isinstance(value, (int, float)):
                if item_value != value:
                    return False
            elif isinstance(value, str):
                if value.lower() not in str(item_value).lower():
                    return False
        
        return True
    
    def _matches_query(self, item: Dict, query: str, search_type: str) -> bool:
        """
        检查是否匹配查询
        
        Args:
            item: 项目
            query: 查询字符串
            search_type: 搜索类型
        
        Returns:
            是否匹配
        """
        item_str = json.dumps(item, ensure_ascii=False).lower()
        
        if search_type == 'regex':
            try:
                return bool(re.search(query, item_str))
            except re.error:
                return False
        else:
            return query.lower() in item_str
    
    def _finalize_search(self, node: SearchNode) -> List[NestedSearchResult]:
        """
        完成搜索
        
        Args:
            node: 搜索树节点
        
        Returns:
            搜索结果列表
        """
        results = []
        
        # 收集路径
        path = self._collect_path(node)
        
        # 为每个结果创建 NestedSearchResult
        for result in node.results:
            # 计算精度分数
            precision_score = self._calculate_precision(node, result)
            
            # 计算相关性分数
            relevance_score = self._calculate_relevance(node, result)
            
            # 提取上下文
            context = self._extract_context(node, result)
            
            nested_result = NestedSearchResult(
                query_tree=node,
                total_matches=len(node.results),
                precision_score=precision_score,
                path=path,
                content=result,
                context=context,
                relevance_score=relevance_score,
            )
            
            results.append(nested_result)
        
        return results
    
    def _collect_path(self, node: SearchNode) -> List[str]:
        """
        收集搜索路径
        
        Args:
            node: 搜索树节点
        
        Returns:
            路径列表
        """
        path = []
        current = node
        
        while current.level > 0:
            path.append(f"{current.search_type}:{current.query}")
            # 向上遍历（简化实现，实际需要父节点引用）
            break
        
        return list(reversed(path))
    
    def _calculate_precision(self, node: SearchNode, result: Dict) -> float:
        """
        计算精度分数
        
        Args:
            node: 搜索树节点
            result: 搜索结果
        
        Returns:
            精度分数 0-1
        """
        score = 1.0
        
        # 深度越深，精度越高
        score *= (0.8 + 0.2 * node.level)
        
        # 结果越少，精度越高
        if node.results:
            score *= (1.0 - len(node.results) / 100.0)
        
        # 匹配过滤器数量
        if hasattr(node, 'metadata'):
            score *= 1.1  # 有额外元数据加分
        
        return min(1.0, max(0.0, score))
    
    def _calculate_relevance(self, node: SearchNode, result: Dict) -> float:
        """
        计算相关性分数
        
        Args:
            node: 搜索树节点
            result: 搜索结果
        
        Returns:
            相关性分数 0-1
        """
        # 基于性能分数
        perf_score = result.get('performance_score', 0.5)
        
        # 基于发生次数
        occurrence = result.get('occurrence_count', 1)
        occurrence_score = min(1.0, occurrence / 10.0)
        
        # 综合计算
        relevance = perf_score * 0.7 + occurrence_score * 0.3
        
        return relevance
    
    def _extract_context(self, node: SearchNode, result: Dict) -> str:
        """
        提取上下文
        
        Args:
            node: 搜索树节点
            result: 搜索结果
        
        Returns:
            上下文字符串
        """
        parts = []
        
        # 事件类型
        if 'event_type' in result:
            parts.append(f"事件类型：{result['event_type']}")
        
        # Agent ID
        if 'agent_id' in result:
            parts.append(f"Agent: {result['agent_id']}")
        
        # 性能分数
        if 'performance_score' in result:
            parts.append(f"性能：{result['performance_score']:.2f}")
        
        return ' | '.join(parts)
    
    def drill_down(
        self,
        initial_query: str,
        drill_path: List[Dict[str, Any]],
    ) -> NestedSearchResult:
        """
        钻取搜索
        
        Args:
            initial_query: 初始查询
            drill_path: 钻取路径，每层包含：
                - filter: 过滤器
                - query: 下一层查询
        
        Returns:
            搜索结果
        """
        # 构建嵌套查询
        queries = [initial_query]
        
        for step in drill_path:
            query_dict = {
                'query': step.get('query', ''),
                'filters': step.get('filter', {}),
                'type': step.get('type', 'exact'),
            }
            queries.append(query_dict)
        
        # 执行嵌套搜索
        results = self.search(queries, max_depth=len(queries))
        
        return results[0] if results else None
    
    def explain_result(self, result: NestedSearchResult) -> str:
        """
        解释搜索结果
        
        Args:
            result: 搜索结果
        
        Returns:
            解释字符串
        """
        lines = [
            "🔍 嵌套搜索结果",
            "=" * 50,
            f"搜索路径：{' → '.join(result.path)}",
            f"总匹配数：{result.total_matches}",
            f"精度分数：{result.precision_score:.2f}",
            f"相关性分数：{result.relevance_score:.2f}",
            f"上下文：{result.context}",
            "",
            "内容:",
            json.dumps(result.content, ensure_ascii=False, indent=2),
        ]
        
        return '\n'.join(lines)


# 使用示例
if __name__ == "__main__":
    engine = NestedSearchEngine()
    
    # 示例 1: 简单嵌套搜索
    print("🔍 示例 1: 简单嵌套搜索")
    queries = [
        'mirror',
        {'query': 'CEO', 'type': 'exact'},
        {'query': '', 'filters': {'performance_score': 0.8}},
    ]
    
    results = engine.search(queries, max_depth=3)
    
    for result in results[:3]:
        print(f"\n结果：{result.context}")
        print(f"精度：{result.precision_score:.2f}")
        print(f"相关性：{result.relevance_score:.2f}")
    
    # 示例 2: 钻取搜索
    print("\n\n🔍 示例 2: 钻取搜索")
    drill_path = [
        {'filter': {'event_type': 'mirror'}, 'query': ''},
        {'filter': {}, 'query': 'high performance'},
    ]
    
    result = engine.drill_down('learning', drill_path)
    
    if result:
        print(engine.explain_result(result))
