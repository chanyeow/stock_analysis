# -*- coding: utf-8 -*-
"""
===================================
板块资金流接口
===================================

职责：
1. GET /api/v1/capital-flow/data 获取板块资金流数据
"""

import logging

from fastapi import APIRouter, HTTPException, Query

from api.v1.schemas.capital_flow import (
    CapitalFlowItem,
    CapitalFlowResponse,
    CapitalFlowTableItem,
    CapitalFlowTableResponse,
)
from api.v1.schemas.common import ErrorResponse
from scripts.capitalflow.fetcher import fetch_capital_flow, fetch_table_data

logger = logging.getLogger(__name__)

router = APIRouter()

VALID_CATEGORIES = {"industry", "concept"}
VALID_PERIODS = {"today", "5day", "10day"}


@router.get(
    "/data",
    response_model=CapitalFlowResponse,
    responses={
        200: {"description": "板块资金流数据"},
        400: {"description": "参数不合法", "model": ErrorResponse},
        500: {"description": "服务器错误", "model": ErrorResponse},
    },
    summary="获取板块资金流数据",
    description="获取东方财富行业/概念板块资金流数据，支持今日、5日、10日三个周期。",
)
def get_capital_flow_data(
    category: str = Query("industry", description="类别: industry(行业) / concept(概念)"),
    period: str = Query("today", description="周期: today(今日) / 5day(5日) / 10day(10日)"),
    force_refresh: bool = Query(False, description="是否跳过缓存强制刷新"),
) -> CapitalFlowResponse:
    """
    获取板块资金流数据。

    数据来源于东方财富 dataapi，包含行业资金流（约 128 个板块）和概念资金流（约 400 个板块）。
    数据按资金净流入降序排列。
    """
    # 参数校验
    if category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_category",
                "message": f"不支持的类别: {category}，可选: {sorted(VALID_CATEGORIES)}",
            },
        )
    if period not in VALID_PERIODS:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "invalid_period",
                "message": f"不支持的周期: {period}，可选: {sorted(VALID_PERIODS)}",
            },
        )

    try:
        result = fetch_capital_flow(
            category=category,
            period=period,
            force_refresh=force_refresh,
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

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={"error": "bad_request", "message": str(e)},
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=503,
            detail={"error": "service_unavailable", "message": str(e)},
        )
    except Exception as e:
        logger.error(f"获取板块资金流失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": "internal_error", "message": f"获取板块资金流失败: {str(e)}"},
        )


@router.get(
    "/table",
    response_model=CapitalFlowTableResponse,
    responses={
        200: {"description": "板块资金流表格数据"},
        400: {"description": "参数不合法", "model": ErrorResponse},
        500: {"description": "服务器错误", "model": ErrorResponse},
    },
    summary="获取板块资金流表格数据（含分页）",
    description="使用东方财富表格接口获取分页数据，包含更多字段（价格、涨跌幅、领涨股等）。",
)
def get_capital_flow_table(
    category: str = Query("industry", description="类别: industry(行业) / concept(概念)"),
    period: str = Query("today", description="周期: today(今日) / 5day(5日) / 10day(10日)"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=200, description="每页条数"),
    force_refresh: bool = Query(False, description="是否跳过缓存强制刷新"),
) -> CapitalFlowTableResponse:
    if category not in VALID_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_category", "message": f"不支持的类别: {category}"},
        )
    if period not in VALID_PERIODS:
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_period", "message": f"不支持的周期: {period}"},
        )

    try:
        result = fetch_table_data(
            category=category,
            period=period,
            page=page,
            page_size=page_size,
            force_refresh=force_refresh,
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

    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": "bad_request", "message": str(e)})
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail={"error": "service_unavailable", "message": str(e)})
    except Exception as e:
        logger.error(f"获取表格数据失败: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": "internal_error", "message": f"获取表格数据失败: {str(e)}"},
        )
