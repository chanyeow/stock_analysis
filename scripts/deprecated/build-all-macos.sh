#!/usr/bin/env bash
# macOS 全量构建脚本
# 功能：依次执行后端构建和桌面端构建，生成完整的 macOS 应用产物
# 流程：build-backend-macos.sh -> build-desktop-macos.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Daily Stock Analysis Desktop Build (macOS) ==="

bash "${SCRIPT_DIR}/build-backend-macos.sh"
bash "${SCRIPT_DIR}/build-desktop-macos.sh"

echo "All builds completed."
