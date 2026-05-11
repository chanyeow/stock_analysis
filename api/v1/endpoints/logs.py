# -*- coding: utf-8 -*-
"""
===================================
日志文件 endpoint
===================================

职责：
1. 列出 logs/ 目录下的 .log 文件
2. 安全地读取指定日志文件尾部内容（防路径遍历）
"""

from __future__ import annotations

import logging
import os
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from fastapi import APIRouter, HTTPException, Query

from api.v1.schemas.logs import LogContentResponse, LogFileInfo, LogListResponse

logger = logging.getLogger(__name__)

router = APIRouter()

LOG_DIR = (os.getenv("LOG_DIR") or "./logs").strip() or "./logs"
MAX_TAIL_LINES = 5000
DEFAULT_TAIL_LINES = 500


def _resolve_log_path(filename: str) -> Path:
    safe_name = os.path.basename(filename)
    if not safe_name or not safe_name.endswith(".log"):
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_filename", "message": "Invalid log filename"},
        )
    log_dir = Path(LOG_DIR).expanduser().resolve()
    target = (log_dir / safe_name).resolve()
    try:
        target.relative_to(log_dir)
    except ValueError:
        raise HTTPException(
            status_code=403,
            detail={"error": "access_denied", "message": "Access denied"},
        )
    if not target.exists():
        raise HTTPException(
            status_code=404,
            detail={"error": "not_found", "message": "Log file not found"},
        )
    if not target.is_file():
        raise HTTPException(
            status_code=400,
            detail={"error": "not_a_file", "message": "Not a file"},
        )
    return target


@router.get(
    "",
    response_model=LogListResponse,
    summary="List log files",
    description="List all .log files in the configured logs directory.",
)
def list_logs() -> LogListResponse:
    log_dir = Path(LOG_DIR).expanduser().resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    files: List[LogFileInfo] = []
    for f in sorted(log_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if f.is_file() and f.suffix == ".log":
            stat = f.stat()
            files.append(
                LogFileInfo(
                    name=f.name,
                    size=stat.st_size,
                    modified_at=datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc),
                )
            )
    return LogListResponse(files=files)


@router.get(
    "/{filename}",
    response_model=LogContentResponse,
    summary="Get log content",
    description="Read the tail of a specific log file.",
)
def get_log_content(
    filename: str,
    tail: int = Query(DEFAULT_TAIL_LINES, ge=1, le=MAX_TAIL_LINES),
) -> LogContentResponse:
    target = _resolve_log_path(filename)
    lines = _read_tail_lines(target, tail)
    return LogContentResponse(
        name=target.name,
        lines=lines,
        read_lines=len(lines),
    )


def _read_tail_lines(path: Path, n: int) -> List[str]:
    with path.open("r", encoding="utf-8", errors="replace") as f:
        return list(deque(f, maxlen=n))
