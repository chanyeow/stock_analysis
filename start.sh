#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

mkdir -p logs data

PYTHON="./.venv/bin/python"
PID_FILE="./data/.main_py.pid"

# 杀掉上次的进程
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "停止旧进程 (PID: $OLD_PID) ..."
        kill "$OLD_PID"
        sleep 2
        # 还没死就强杀
        if kill -0 "$OLD_PID" 2>/dev/null; then
            echo "强制终止 ..."
            kill -9 "$OLD_PID"
        fi
    fi
    rm -f "$PID_FILE"
fi

# 兜底：杀掉所有 python main.py --webui 进程
pkill -f "python.*main\.py.*--webui" 2>/dev/null || true
sleep 1

echo "启动服务 ..."
nohup $PYTHON main.py --webui > ./logs/start.log 2>&1 &
NEW_PID=$!
echo "$NEW_PID" > "$PID_FILE"
echo "已启动 (PID: $NEW_PID)"
echo "日志: tail -f ./logs/start.log"
echo "访问: http://192.168.2.219:9094"
