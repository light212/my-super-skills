#!/bin/bash
# 启动自主学习守护进程

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON="${PYTHON:-python3}"

echo "🚀 启动自主学习守护进程..."

# 检查依赖
if ! $PYTHON -c "import daemon" 2>/dev/null; then
    echo "⚠️  安装依赖..."
    $PYTHON -m pip install python-daemon --quiet
fi

# 创建必要目录
mkdir -p ~/.openclaw/super_learning/{logs,reports,data}

# 启动守护进程
if [ "$1" == "--foreground" ] || [ "$1" == "-f" ]; then
    echo "📍 前台运行模式"
    $PYTHON "$SCRIPT_DIR/daemon/autonomous_daemon.py" --foreground
else
    echo "📦 后台运行模式"
    $PYTHON "$SCRIPT_DIR/daemon/autonomous_daemon.py" &
    PID=$!
    echo $PID > ~/.openclaw/super_learning/daemon.pid
    echo "✅ 守护进程已启动 (PID: $PID)"
fi
