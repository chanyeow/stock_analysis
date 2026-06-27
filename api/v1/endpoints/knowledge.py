# -*- coding: utf-8 -*-
"""
===================================
知识库接口
===================================

职责：
1. POST /api/v1/knowledge/crawl 触发知识库数据爬取
2. GET /api/v1/knowledge/progress 获取爬取进度
3. GET /api/v1/knowledge/list 获取知识库列表
4. GET /api/v1/knowledge/markdown/{category}/{code} 获取 Markdown 内容
5. GET /api/v1/knowledge/search 搜索知识库
"""

import logging
import threading
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from api.v1.schemas.common import ErrorResponse
from api.v1.schemas.knowledge import (
    CrawlProgressResponse,
    KnowledgeItem,
    KnowledgeListResponse,
    KnowledgeMarkdownResponse,
    SearchResponse,
)
from api.v1.schemas.capital_flow import (
    CapitalFlowItem,
    CapitalFlowResponse,
    CapitalFlowTableItem,
    CapitalFlowTableResponse,
)
from scripts.knowledge.fetcher import (
    crawl_all,
    load_capital_flow_data,
    load_capital_flow_table_data,
    load_existing_items,
    read_markdown,
    search_items,
)
from scripts.knowledge.types import CrawlProgress

logger = logging.getLogger(__name__)

router = APIRouter()

# 全局爬取状态
_crawl_progress = CrawlProgress()
_crawl_lock = threading.Lock()
_crawl_thread: Optional[threading.Thread] = None


def _update_progress(progress: CrawlProgress) -> None:
    """更新爬取进度的回调函数"""
    global _crawl_progress
    with _crawl_lock:
        _crawl_progress = CrawlProgress(
            total=progress.total,
            current=progress.current,
            status=progress.status,
            message=progress.message,
            errors=list(progress.errors),
        )


def _crawl_worker() -> None:
    """后台爬取工作线程"""
    global _crawl_progress
    try:
        with _crawl_lock:
            _crawl_progress = CrawlProgress(
                status="crawling",
                message="开始爬取知识库数据...",
            )

        crawl_all(on_progress=_update_progress)

    except Exception as e:
        logger.error(f"知识库爬取失败: {e}", exc_info=True)
        with _crawl_lock:
            _crawl_progress = CrawlProgress(
                status="error",
                message=f"爬取失败: {str(e)}",
                errors=[str(e)],
            )


@router.post(
    "/crawl",
    response_model=CrawlProgressResponse,
    responses={
        200: {"description": "爬取已启动或正在进行中"},
        409: {"description": "已有爬取任务在进行中"},
        500: {"description": "服务器错误", "model": ErrorResponse},
    },
    summary="触发知识库数据爬取",
    description="启动后台线程爬取板块和股票数据，写入 Markdown 文件。爬取过程中可通过 /progress 接口查询进度。",
)
def trigger_crawl() -> CrawlProgressResponse:
    global _crawl_thread

    with _crawl_lock:
        # 检查是否已有爬取任务在进行中
        if _crawl_thread is not None and _crawl_thread.is_alive():
            if _crawl_progress.status == "crawling":
                raise HTTPException(
                    status_code=409,
                    detail={
                        "error": "crawl_in_progress",
                        "message": "已有爬取任务在进行中，请稍后再试",
                    },
                )

        # 启动新的爬取线程
        _crawl_thread = threading.Thread(target=_crawl_worker, daemon=True)
        _crawl_thread.start()

    return CrawlProgressResponse(
        total=_crawl_progress.total,
        current=_crawl_progress.current,
        status=_crawl_progress.status,
        message=_crawl_progress.message,
        errors=list(_crawl_progress.errors),
    )


@router.get(
    "/progress",
    response_model=CrawlProgressResponse,
    summary="获取爬取进度",
    description="获取当前知识库爬取任务的进度信息。",
)
def get_progress() -> CrawlProgressResponse:
    with _crawl_lock:
        return CrawlProgressResponse(
            total=_crawl_progress.total,
            current=_crawl_progress.current,
            status=_crawl_progress.status,
            message=_crawl_progress.message,
            errors=list(_crawl_progress.errors),
        )


@router.get(
    "/list",
    response_model=KnowledgeListResponse,
    summary="获取知识库列表",
    description="获取所有已爬取的知识库条目列表。",
)
def list_items(
    category: Optional[str] = Query(None, description="类别筛选: bk/sh/sz"),
) -> KnowledgeListResponse:
    try:
        items = load_existing_items()

        # 按类别筛选
        if category:
            items = [item for item in items if item.category == category]

        return KnowledgeListResponse(
            total=len(items),
            data=[
                KnowledgeItem(
                    code=item.code,
                    name=item.name,
                    category=item.category,
                    change_pct=item.change_pct,
                )
                for item in items
            ],
        )

    except Exception as e:
        logger.error(f"获取知识库列表失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": "internal_error", "message": f"获取知识库列表失败: {str(e)}"},
        )


@router.get(
    "/markdown/{category}/{code}",
    response_model=KnowledgeMarkdownResponse,
    responses={
        200: {"description": "Markdown 内容"},
        404: {"description": "条目不存在", "model": ErrorResponse},
        500: {"description": "服务器错误", "model": ErrorResponse},
    },
    summary="获取 Markdown 内容",
    description="获取指定知识库条目的 Markdown 内容。",
)
def get_markdown(category: str, code: str) -> KnowledgeMarkdownResponse:
    # 参数校验
    valid_categories = {"bk", "sh", "sz"}
    if category not in valid_categories:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_category",
                "message": f"不支持的类别: {category}，可选: {sorted(valid_categories)}",
            },
        )

    try:
        content = read_markdown(code, category)
        if content is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "not_found",
                    "message": f"未找到条目: {category}/{code}",
                },
            )

        # 从内容中提取名称
        name = code
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("# ") and "(" in line:
                name = line[2:line.index("(")].strip()
                break

        return KnowledgeMarkdownResponse(
            code=code,
            name=name,
            category=category,
            content=content,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取 Markdown 内容失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": "internal_error", "message": f"获取 Markdown 内容失败: {str(e)}"},
        )


@router.get(
    "/search",
    response_model=SearchResponse,
    summary="搜索知识库",
    description="按代码或名称搜索知识库条目。",
)
def search(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
) -> SearchResponse:
    try:
        items = search_items(keyword)

        return SearchResponse(
            keyword=keyword,
            total=len(items),
            data=[
                KnowledgeItem(
                    code=item.code,
                    name=item.name,
                    category=item.category,
                    change_pct=item.change_pct,
                )
                for item in items
            ],
        )

    except Exception as e:
        logger.error(f"搜索知识库失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": "internal_error", "message": f"搜索知识库失败: {str(e)}"},
        )


@router.get(
    "/capital-flow/data",
    response_model=CapitalFlowResponse,
    responses={
        200: {"description": "板块资金流数据"},
        404: {"description": "无数据", "model": ErrorResponse},
        500: {"description": "服务器错误", "model": ErrorResponse},
    },
    summary="从知识库获取板块资金流数据",
    description="从 Markdown 文件中读取板块资金流数据。如果未爬取数据，返回 404 提示用户先到知识库爬取。",
)
def get_capital_flow_data_from_kb(
    category: str = Query("industry", description="类别: industry(行业) / concept(概念)"),
) -> CapitalFlowResponse:
    try:
        result = load_capital_flow_data(category=category)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "no_data",
                    "message": "未找到板块数据，请先到「知识库」页签点击刷新按钮爬取数据",
                },
            )

        items = [
            CapitalFlowItem(
                code=item["code"],
                name=item["name"],
                flow=item["flow"],
            )
            for item in result["data"]
        ]

        return CapitalFlowResponse(
            category=result["category"],
            period=result["period"],
            total=result["total"],
            data=items,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"从知识库获取资金流数据失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": "internal_error", "message": f"从知识库获取资金流数据失败: {str(e)}"},
        )


@router.get(
    "/capital-flow/table",
    response_model=CapitalFlowTableResponse,
    responses={
        200: {"description": "板块资金流表格数据"},
        404: {"description": "无数据", "model": ErrorResponse},
        500: {"description": "服务器错误", "model": ErrorResponse},
    },
    summary="从知识库获取板块资金流表格数据（含分页）",
    description="从 Markdown 文件中读取板块资金流表格数据。",
)
def get_capital_flow_table_from_kb(
    category: str = Query("industry", description="类别: industry(行业) / concept(概念)"),
    period: str = Query("today", description="周期: today(今日) / 5day(5日) / 10day(10日)"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=200, description="每页条数"),
) -> CapitalFlowTableResponse:
    try:
        result = load_capital_flow_table_data(
            category=category,
            period=period,
            page=page,
            page_size=page_size,
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "no_data",
                    "message": "未找到板块数据，请先到「知识库」页签点击刷新按钮爬取数据",
                },
            )

        items = [
            CapitalFlowTableItem(
                code=item["code"],
                name=item["name"],
                flow=item["flow"],
                price=item.get("price"),
                change_pct=item.get("change_pct"),
                company_count=item.get("company_count"),
                lead_stock_name=item.get("lead_stock_name", ""),
                lead_stock_code=item.get("lead_stock_code", ""),
                main_flow=item.get("main_flow"),
                main_ratio=item.get("main_ratio"),
                super_large_flow=item.get("super_large_flow"),
                large_flow=item.get("large_flow"),
                medium_flow=item.get("medium_flow"),
                small_flow=item.get("small_flow"),
                super_large_ratio=item.get("super_large_ratio"),
                large_ratio=item.get("large_ratio"),
                medium_ratio=item.get("medium_ratio"),
                small_ratio=item.get("small_ratio"),
            )
            for item in result["data"]
        ]

        return CapitalFlowTableResponse(
            category=result["category"],
            period=result["period"],
            total=result["total"],
            page=result["page"],
            page_size=result["page_size"],
            total_pages=result["total_pages"],
            data=items,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"从知识库获取表格数据失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": "internal_error", "message": f"从知识库获取表格数据失败: {str(e)}"},
        )
