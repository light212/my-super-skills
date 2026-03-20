#!/usr/bin/env python3
"""
主动学习爬虫

自动浏览 GitHub 优秀项目，学习优点
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_collector.collector import DataCollector, LearningEvent


class ActiveLearner:
    """
    主动学习器
    
    主动检索优秀项目，学习优点
    """
    
    def __init__(self):
        """初始化主动学习器"""
        self.collector = DataCollector()
        self.learned_projects = set()
        self._load_learned()
    
    def _load_learned(self):
        """加载已学习项目"""
        learned_path = os.path.expanduser(
            '~/.openclaw/super_learning/learned_projects.json'
        )
        
        if os.path.exists(learned_path):
            with open(learned_path, 'r', encoding='utf-8') as f:
                self.learned_projects = set(json.load(f))
    
    def _save_learned(self):
        """保存已学习项目"""
        learned_path = os.path.expanduser(
            '~/.openclaw/super_learning/learned_projects.json'
        )
        
        os.makedirs(os.path.dirname(learned_path), exist_ok=True)
        
        with open(learned_path, 'w', encoding='utf-8') as f:
            json.dump(list(self.learned_projects), f, ensure_ascii=False, indent=2)
    
    def learn_from_github_repo(self, repo_url: str, analysis: dict = None) -> LearningEvent:
        """
        从 GitHub 仓库学习
        
        Args:
            repo_url: 仓库 URL
            analysis: 分析结果
        
        Returns:
            学习事件
        """
        # 提取仓库名
        repo_name = repo_url.rstrip('/').split('/')[-1]
        
        if repo_name in self.learned_projects:
            print(f"⏭️  已学习过：{repo_name}")
            return None
        
        # 分析仓库（简化实现）
        if not analysis:
            analysis = self._analyze_repo(repo_url)
        
        # 创建学习事件
        event = LearningEvent(
            event_type='github_learning',
            agent_id='active_learner',
            timestamp=datetime.now().isoformat(),
            context={
                'source': 'github',
                'repo': repo_name,
                'url': repo_url,
            },
            result=analysis,
            performance_score=analysis.get('score', 0.8),
        )
        
        # 记录学习
        self.collector.record_event(event)
        
        # 标记已学习
        self.learned_projects.add(repo_name)
        self._save_learned()
        
        print(f"✅ 已学习：{repo_name}")
        print(f"   评分：{analysis.get('score', 0):.2f}")
        print(f"   优点：{len(analysis.get('strengths', []))} 个")
        
        return event
    
    def _analyze_repo(self, repo_url: str) -> dict:
        """
        分析仓库（简化实现）
        
        Args:
            repo_url: 仓库 URL
        
        Returns:
            分析结果
        """
        # 实际应该调用 GitHub API 或爬取网页
        # 这里简化实现
        
        repo_name = repo_url.rstrip('/').split('/')[-1]
        
        # 模拟分析
        analysis = {
            'name': repo_name,
            'score': 0.85,
            'strengths': [
                '完善的文档结构',
                '清晰的代码组织',
                '自动化脚本',
                '守护进程设计',
            ],
            'features': [
                '自主学习',
                '定时任务',
                '日志记录',
                '配置管理',
            ],
            'learnable_patterns': [
                'daemon 模式',
                '配置与代码分离',
                '优雅退出处理',
            ],
        }
        
        return analysis
    
    def learn_from_local_project(self, project_path: str) -> list:
        """
        从本地项目学习
        
        Args:
            project_path: 项目路径
        
        Returns:
            学习事件列表
        """
        project_path = Path(project_path)
        
        if not project_path.exists():
            print(f"❌ 项目不存在：{project_path}")
            return []
        
        events = []
        
        # 分析项目结构
        structure = self._analyze_structure(project_path)
        
        # 创建学习事件
        event = LearningEvent(
            event_type='project_learning',
            agent_id='active_learner',
            timestamp=datetime.now().isoformat(),
            context={
                'source': 'local',
                'path': str(project_path),
                'structure': structure,
            },
            result={
                'strengths': self._identify_strengths(structure),
                'patterns': self._identify_patterns(structure),
            },
            performance_score=0.9,
        )
        
        self.collector.record_event(event)
        events.append(event)
        
        print(f"✅ 已学习本地项目：{project_path.name}")
        
        return events
    
    def _analyze_structure(self, project_path: Path) -> dict:
        """分析项目结构"""
        structure = {
            'files': [],
            'directories': [],
            'python_files': 0,
            'config_files': 0,
            'doc_files': 0,
        }
        
        for item in project_path.iterdir():
            if item.is_file():
                structure['files'].append(item.name)
                if item.suffix == '.py':
                    structure['python_files'] += 1
                elif item.suffix in ['.md', '.rst', '.txt']:
                    structure['doc_files'] += 1
                elif item.name in ['config.json', 'config.yaml', '.env.example']:
                    structure['config_files'] += 1
            elif item.is_dir() and not item.name.startswith('.'):
                structure['directories'].append(item.name)
        
        return structure
    
    def _identify_strengths(self, structure: dict) -> list:
        """识别优点"""
        strengths = []
        
        if structure['python_files'] > 5:
            strengths.append('模块化设计')
        
        if structure['doc_files'] > 2:
            strengths.append('文档完善')
        
        if structure['config_files'] > 0:
            strengths.append('配置管理良好')
        
        if 'daemon' in str(structure['files']).lower():
            strengths.append('守护进程支持')
        
        return strengths
    
    def _identify_patterns(self, structure: dict) -> list:
        """识别模式"""
        patterns = []
        
        if 'daemon' in str(structure['files']).lower():
            patterns.append('daemon 模式')
        
        if any('config' in f.lower() for f in structure['files']):
            patterns.append('配置与代码分离')
        
        if any('log' in d.lower() for d in structure['directories']):
            patterns.append('日志管理')
        
        return patterns


def main():
    """主函数"""
    learner = ActiveLearner()
    
    print("🚀 主动学习器启动")
    print("=" * 50)
    
    # 学习 GitHub 项目
    github_projects = [
        'https://github.com/affaan-m/everything-claude-code',
        'https://github.com/anthropics/anthropic-cookbook',
        'https://github.com/openai/openai-cookbook',
    ]
    
    print("\n📚 学习 GitHub 项目...")
    for url in github_projects:
        learner.learn_from_github_repo(url)
        time.sleep(1)  # 避免请求过快
    
    # 学习本地项目
    local_projects = [
        Path('/Users/tangxuguang/project/git/billion-people-world/skills/my-super-skills'),
        Path('/Users/tangxuguang/project/git/everything-claude-code'),
    ]
    
    print("\n📚 学习本地项目...")
    for path in local_projects:
        if path.exists():
            learner.learn_from_local_project(path)
    
    print("\n" + "=" * 50)
    print("✅ 主动学习完成")
    print(f"已学习项目数：{len(learner.learned_projects)}")


if __name__ == '__main__':
    main()
