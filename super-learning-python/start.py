#!/usr/bin/env python3
"""
Super-Learning Python 启动脚本

用法:
    python start.py
    
或者:
    uvicorn api.api:app --reload --host 0.0.0.0 --port 8000
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def check_dependencies():
    """检查依赖"""
    required = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "deap",
        "optuna",
        "scikit-learn",
        "numpy",
        "pandas",
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ 缺少依赖:")
        for package in missing:
            print(f"   - {package}")
        print("\n请运行：pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖已安装")
    return True


def main():
    """主函数"""
    print("🚀 Super-Learning Python 启动脚本\n")
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 启动 API 服务
    print("\n📡 启动 API 服务...")
    print("   http://localhost:8000")
    print("   API 文档：http://localhost:8000/docs\n")
    
    import uvicorn
    from api.api import app
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
