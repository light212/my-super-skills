# 🤖 自主学习系统 - 完全自动化

## 🚀 一键启动

```bash
# 进入目录
cd super-learning-python

# 启动守护进程（后台运行）
bash start-daemon.sh

# 或者前台运行（查看实时日志）
bash start-daemon.sh --foreground
```

## 📊 查看状态

```bash
# 查看守护进程状态
python3 daemon/autonomous_daemon.py --status

# 查看日志
tail -f ~/.openclaw/super_learning/daemon.log

# 查看最新报告
ls -lt ~/.openclaw/super_learning/reports/ | head
```

## ⚙️ 自动运行计划

| 任务 | 频率 | 说明 |
|------|------|------|
| **检查新数据** | 每 5 分钟 | 扫描数据库中的新学习事件 |
| **运行学习循环** | 每 30 分钟 | 分辨→判断→吸收→壮大→健硕→成熟 |
| **生成报告** | 每 24 小时 | 生成学习进度报告 |

## 📝 配置文件

编辑 `~/.openclaw/super_learning/daemon_config.json`:

```json
{
  "check_interval": 300,       // 检查间隔 (秒)
  "cycle_interval": 1800,      // 学习循环间隔 (秒)
  "report_interval": 86400,    // 报告间隔 (秒)
  "min_data_points": 10,       // 最小数据点
  "auto_start": true,          // 开机自启
  "log_path": "~/.openclaw/super_learning/daemon.log"
}
```

## 🔧 管理命令

```bash
# 停止守护进程
kill $(cat ~/.openclaw/super_learning/daemon.pid)

# 重启守护进程
bash start-daemon.sh stop
bash start-daemon.sh start

# 查看日志
tail -f ~/.openclaw/super_learning/daemon.log
```

## 📈 输出示例

```
[2026-03-20T09:15:00] [INFO] ==================================================
[2026-03-20T09:15:00] [INFO] 自主学习守护进程启动
[2026-03-20T09:15:00] [INFO] 配置：检查间隔=300s
[2026-03-20T09:15:00] [INFO] ==================================================
[2026-03-20T09:20:00] [INFO] 发现 15 条新数据
[2026-03-20T09:45:00] [INFO] 开始学习循环
[2026-03-20T09:45:02] [INFO] 🔍 分辨完成
[2026-03-20T09:45:02] [INFO]    有用：12
[2026-03-20T09:45:02] [INFO]    无用：3
[2026-03-20T09:45:03] [INFO] ⚖️  判断完成
[2026-03-20T09:45:03] [INFO]    保留：10
[2026-03-20T09:45:03] [INFO]    舍弃：2
[2026-03-20T09:45:04] [INFO] 📥 吸收完成
[2026-03-20T09:45:04] [INFO]    吸收模式：8
[2026-03-20T09:45:05] [INFO] 📈 壮大完成
[2026-03-20T09:45:05] [INFO]    扩展能力：8
[2026-03-20T09:45:06] [INFO] 💪 健硕完成
[2026-03-20T09:45:06] [INFO]    平均等级：2.5
[2026-03-20T09:45:07] [INFO] 🎓 成熟完成
[2026-03-20T09:45:07] [INFO]    成熟度：0.75
[2026-03-20T09:45:07] [INFO] ✅ 学习循环完成
```

## 🎯 完全自动化

**你什么都不用做！**

系统会自动：
- 🔍 分辨什么是好的/坏的
- ⚖️  判断什么有价值
- 📥 吸收有价值的知识
- 📈 壮大能力边界
- 💪 强化核心能力
- 🎓 评估成熟度
- 🔄 持续循环

**你只需要：**
1. 启动守护进程
2. 正常使用 Super-Learning
3. 定期查看报告

**就这么简单！** 🎉
