#!/usr/bin/env bash
# CI 后端门禁脚本
# 功能：在 CI 流水线中执行后端代码质量检查，可按阶段单独运行
# 阶段：syntax（Python 语法检查）-> flake8（静态分析）-> deterministic（确定性测试）-> offline-tests（离线 pytest）
# 用法：./scripts/ci_gate.sh [all|syntax|flake8|deterministic|offline-tests]

set -euo pipefail

syntax_check() {
  echo "==> backend-gate: Python syntax check"
  python -m py_compile main.py src/config.py src/auth.py src/analyzer.py src/notification.py
  python -m py_compile src/storage.py src/scheduler.py src/search_service.py
  python -m py_compile src/market_analyzer.py src/stock_analyzer.py
  python -m py_compile data_provider/*.py
}

flake8_checks() {
  echo "==> backend-gate: flake8 critical checks"
  flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
}

deterministic_checks() {
  echo "==> backend-gate: local deterministic checks"
  ./scripts/test.sh code
  ./scripts/test.sh yfinance
}

offline_test_suite() {
  echo "==> backend-gate: offline test suite"
  python -m pytest -m "not network"
}

run_all() {
  syntax_check
  flake8_checks
  deterministic_checks
  offline_test_suite
  echo "==> backend-gate: all checks passed"
}

phase="${1:-all}"

case "$phase" in
  all)
    run_all
    ;;
  syntax)
    syntax_check
    ;;
  flake8)
    flake8_checks
    ;;
  deterministic)
    deterministic_checks
    ;;
  offline-tests)
    offline_test_suite
    ;;
  *)
    echo "Usage: $0 [all|syntax|flake8|deterministic|offline-tests]" >&2
    exit 2
    ;;
esac
