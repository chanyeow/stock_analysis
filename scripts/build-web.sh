#!/usr/bin/env bash
# Web 前端构建脚本
# 功能：安装前端依赖、执行 lint 检查、构建前端静态资源到 static/ 目录
# 用法：./scripts/build-web.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
WEB_DIR="$PROJECT_ROOT/apps/dsa-web"
STATIC_DIR="$PROJECT_ROOT/static"

cd "$WEB_DIR"

echo "==> Installing dependencies..."
npm ci

echo "==> Running lint..."
npm run lint

echo "==> Building web frontend..."
npm run build

echo "==> Build complete. Output: $STATIC_DIR"
ls -lh "$STATIC_DIR"
