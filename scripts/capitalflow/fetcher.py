# -*- coding: utf-8 -*-
"""
===================================
板块资金流数据抓取器
===================================

数据来源：东方财富 dataapi (https://data.eastmoney.com/dataapi/bkzj/getbkzj)
覆盖：
- 行业资金流 (code=m:90+s:4) — 约 128 个申万行业板块
- 概念资金流 (code=m:90+t:3) — 约 400 个概念板块

防封禁策略（与 data_provider/efinance_fetcher.py 对齐）：
1. 每次请求前随机休眠 1.5-3.0 秒
2. 随机轮换 User-Agent
3. 使用 tenacity 实现指数退避重试
4. 熔断器机制：连续失败后自动冷却
"""

import logging
import random
import re
import time
from typing import Any, Dict, List, Optional

import requests
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)

from data_provider.realtime_types import CircuitBreaker

logger = logging.getLogger(__name__)

# ============================================================
# 配置常量
# ============================================================

BASE_URL = "https://data.eastmoney.com/dataapi/bkzj/getbkzj"
TABLE_URL = "https://push2.eastmoney.com/api/qt/clist/get"

# 类别 -> 东方财富 code 参数映射
CATEGORY_CODE = {
    "industry": "m:90+s:4",   # 行业资金流 (申万行业)
    "concept": "m:90+t:3",    # 概念资金流
}

# 周期 -> key 参数映射（东方财富的字段编号）
PERIOD_KEY = {
    "today": "f62",    # 今日
    "5day": "f164",    # 5日
    "10day": "f174",   # 10日
}

# 表格接口的 fields 参数（各周期不同）
TABLE_FIELDS: Dict[str, str] = {
    "today": "f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13",
    "5day": "f12,f14,f2,f109,f164,f165,f166,f167,f168,f169,f170,f171,f172,f173,f257,f258,f124,f1,f13",
    "10day": "f12,f14,f2,f160,f174,f175,f176,f177,f178,f179,f180,f181,f182,f183,f260,f261,f124,f1,f13",
}

# 各周期的子字段映射（用于抽取表格全部列）
# 格式: { period: { output_key: (raw_field, description) } }
PERIOD_DETAIL_FIELDS: Dict[str, Dict[str, tuple]] = {
    # 字段是交错的: 净额, 占比, 净额, 占比, ...
    # 主力净额 = 超大单净额 + 大单净额（东方财富前端计算）
    "today": {
        "main_ratio": ("f184", "今日主力净流入占比"),
        "super_large_flow": ("f66", "今日超大单净流入"),
        "super_large_ratio": ("f69", "今日超大单净流入占比"),
        "large_flow": ("f72", "今日大单净流入"),
        "large_ratio": ("f75", "今日大单净流入占比"),
        "medium_flow": ("f78", "今日中单净流入"),
        "medium_ratio": ("f81", "今日中单净流入占比"),
        "small_flow": ("f84", "今日小单净流入"),
        "small_ratio": ("f87", "今日小单净流入占比"),
        "lead_name": ("f204", "领涨股名称"),
        "lead_code": ("f205", "领涨股代码"),
    },
    "5day": {
        "main_ratio": ("f165", "5日主力净流入占比"),
        "super_large_flow": ("f166", "5日超大单净流入"),
        "super_large_ratio": ("f167", "5日超大单净流入占比"),
        "large_flow": ("f168", "5日大单净流入"),
        "large_ratio": ("f169", "5日大单净流入占比"),
        "medium_flow": ("f170", "5日中单净流入"),
        "medium_ratio": ("f171", "5日中单净流入占比"),
        "small_flow": ("f172", "5日小单净流入"),
        "small_ratio": ("f173", "5日小单净流入占比"),
        "lead_name": ("f257", "领涨股名称"),
        "lead_code": ("f258", "领涨股代码"),
    },
    "10day": {
        "main_ratio": ("f175", "10日主力净流入占比"),
        "super_large_flow": ("f176", "10日超大单净流入"),
        "super_large_ratio": ("f177", "10日超大单净流入占比"),
        "large_flow": ("f178", "10日大单净流入"),
        "large_ratio": ("f179", "10日大单净流入占比"),
        "medium_flow": ("f180", "10日中单净流入"),
        "medium_ratio": ("f181", "10日中单净流入占比"),
        "small_flow": ("f182", "10日小单净流入"),
        "small_ratio": ("f183", "10日小单净流入占比"),
        "lead_name": ("f260", "领涨股名称"),
        "lead_code": ("f261", "领涨股代码"),
    },
}

# User-Agent 池，用于随机轮换
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

# Referer 必须携带，否则可能被拒绝
REFERER = "https://data.eastmoney.com/bkzj/hy.html"

# 休眠范围（秒）
SLEEP_MIN = 1.5
SLEEP_MAX = 3.0

# 缓存 TTL（秒）
CACHE_TTL = 300  # 5 分钟

# ============================================================
# 熔断器
# ============================================================

_circuit_breaker = CircuitBreaker(
    failure_threshold=3,
    cooldown_seconds=300.0,  # 5 分钟冷却
    half_open_max_calls=1,
)

# ============================================================
# 缓存
# ============================================================

_cache: Dict[str, Dict[str, Any]] = {}


def _cache_key(category: str, period: str) -> str:
    return f"{category}:{period}"


def _get_cached(category: str, period: str) -> Optional[Dict[str, Any]]:
    key = _cache_key(category, period)
    entry = _cache.get(key)
    if entry is None:
        return None
    if time.time() - entry["ts"] > CACHE_TTL:
        del _cache[key]
        return None
    return entry["data"]


def _set_cache(category: str, period: str, data: Dict[str, Any]) -> None:
    key = _cache_key(category, period)
    _cache[key] = {"ts": time.time(), "data": data}


# ============================================================
# 防护策略
# ============================================================

def _random_sleep(min_sec: float = SLEEP_MIN, max_sec: float = SLEEP_MAX) -> None:
    """随机休眠，增加请求间隔的不可预测性"""
    sleep_time = random.uniform(min_sec, max_sec)
    logger.debug(f"随机休眠 {sleep_time:.2f} 秒...")
    time.sleep(sleep_time)


def _random_user_agent() -> str:
    """随机选择一个 User-Agent"""
    return random.choice(USER_AGENTS)


# ============================================================
# 核心抓取逻辑
# ============================================================

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=30),
    retry=retry_if_exception_type((
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.ChunkedEncodingError,
        requests.exceptions.HTTPError,
    )),
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
def _fetch_raw(category: str, period: str) -> Dict[str, Any]:
    """
    执行单次 API 请求，返回原始 JSON 响应。

    被 tenacity @retry 装饰，指数退避最多重试 3 次。
    """
    code = CATEGORY_CODE.get(category)
    if code is None:
        raise ValueError(f"不支持的类别: {category}，可选: {list(CATEGORY_CODE.keys())}")

    key = PERIOD_KEY.get(period)
    if key is None:
        raise ValueError(f"不支持的周期: {period}，可选: {list(PERIOD_KEY.keys())}")

    # 熔断检查
    source_key = f"capitalflow_{category}"
    if not _circuit_breaker.is_available(source_key):
        logger.warning(f"[熔断] 数据源 {source_key} 处于熔断状态，拒绝请求")
        raise RuntimeError(f"数据源 {source_key} 处于熔断保护状态，请稍后重试")

    # 随机休眠
    _random_sleep()

    url = BASE_URL
    params = {
        "key": key,
        "code": code,
    }
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Referer": REFERER,
        "User-Agent": _random_user_agent(),
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    logger.info(f"请求东方财富板块资金流: category={category}, period={period}")

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        resp.raise_for_status()

        data = resp.json()
        rc = data.get("rc")
        if rc != 0:
            error_msg = f"东方财富 API 返回错误: rc={rc}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        # 记录成功
        _circuit_breaker.record_success(source_key)
        return data

    except (requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
            requests.exceptions.RequestException) as e:
        _circuit_breaker.record_failure(source_key, str(e))
        raise
    except Exception as e:
        _circuit_breaker.record_failure(source_key, str(e))
        raise


def fetch_capital_flow(
    category: str = "industry",
    period: str = "today",
    force_refresh: bool = False,
) -> Dict[str, Any]:
    """
    获取板块资金流数据。

    Args:
        category: 类别 — "industry" (行业) 或 "concept" (概念)
        period: 周期 — "today" (今日), "5day" (5日), "10day" (10日)
        force_refresh: 是否跳过缓存强制刷新

    Returns:
        {
            "category": "industry",
            "period": "today",
            "total": 128,
            "data": [
                {"code": "BK1036", "name": "半导体", "flow": 5243314176},
                ...
            ]
        }

    Raises:
        ValueError: 类别或周期参数不合法
        RuntimeError: 熔断保护中或 API 错误
    """
    if category not in CATEGORY_CODE:
        raise ValueError(f"不支持的类别: {category}，可选: {list(CATEGORY_CODE.keys())}")
    if period not in PERIOD_KEY:
        raise ValueError(f"不支持的周期: {period}，可选: {list(PERIOD_KEY.keys())}")

    # 检查缓存
    if not force_refresh:
        cached = _get_cached(category, period)
        if cached is not None:
            logger.info(f"使用缓存数据: category={category}, period={period}")
            return cached

    raw = _fetch_raw(category, period)

    # 解析响应
    data_block = raw.get("data", {})
    total = data_block.get("total", 0)
    diff = data_block.get("diff", [])

    # 确定资金字段名（与请求的 key 一致）
    flow_field = PERIOD_KEY[period]

    items: List[Dict[str, Any]] = []
    for item in diff:
        code = item.get("f12", "")
        name = item.get("f14", "")
        flow = item.get(flow_field, 0)
        if name:  # 过滤掉名称为空的条目
            items.append({
                "code": code,
                "name": name,
                "flow": flow,
            })

    # 按资金流降序排列（流入最多在前）
    items.sort(key=lambda x: x["flow"], reverse=True)

    result = {
        "category": category,
        "period": period,
        "total": total,
        "data": items,
    }

    # 写入缓存
    _set_cache(category, period, result)

    return result


# ============================================================
# 表格数据抓取（带分页的原生表格接口）
# ============================================================

def _table_cache_key(category: str, period: str) -> str:
    return f"table:{category}:{period}"


def _get_table_cached(category: str, period: str) -> Optional[Dict[str, Any]]:
    key = _table_cache_key(category, period)
    entry = _cache.get(key)
    if entry is None:
        return None
    if time.time() - entry["ts"] > CACHE_TTL:
        del _cache[key]
        return None
    return entry["data"]


def _set_table_cache(category: str, period: str, data: Dict[str, Any]) -> None:
    key = _table_cache_key(category, period)
    _cache[key] = {"ts": time.time(), "data": data}


def _strip_jsonp(text: str) -> str:
    """Remove JSONP callback wrapper, e.g. jQuery...(...) -> {...}"""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return text


def _fetch_table_page(
    category: str, period: str, page: int, page_size: int,
    code: str, key: str, fields: str, source_key: str,
) -> tuple:
    """Fetch a single page of table data. Returns (diffs, total) tuple."""
    params = {
        "fid": key,
        "po": "1",
        "pz": str(page_size),
        "pn": str(page),
        "np": "1",
        "fltt": "2",
        "invt": "2",
        "ut": "8dec03ba335b81bf4ebdf7b29ec27d15",
        "fs": code,
        "fields": fields,
    }
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Referer": REFERER,
        "User-Agent": _random_user_agent(),
        "sec-ch-ua": '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    resp = requests.get(TABLE_URL, params=params, headers=headers, timeout=30)
    resp.raise_for_status()

    raw_text = resp.text
    json_text = _strip_jsonp(raw_text)
    data = __import__("json").loads(json_text)

    rc = data.get("rc")
    if rc != 0:
        raise RuntimeError(f"表格 API 返回错误: rc={rc}")

    data_block = data.get("data", {})
    diff = data_block.get("diff", [])
    total = data_block.get("total", 0)
    return diff, total


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=30),
    retry=retry_if_exception_type((
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.ChunkedEncodingError,
        requests.exceptions.HTTPError,
    )),
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
def _fetch_table_raw(category: str, period: str) -> List[Dict[str, Any]]:
    """
    调用 push2.eastmoney.com 表格接口，获取全量板块列表。
    API 单页上限约 100 条，自动翻页获取全部数据。
    返回解析后的 diff 数组。
    """
    code = CATEGORY_CODE.get(category)
    if code is None:
        raise ValueError(f"不支持的类别: {category}")

    key = PERIOD_KEY.get(period)
    if key is None:
        raise ValueError(f"不支持的周期: {period}")

    fields = TABLE_FIELDS.get(period)
    if fields is None:
        raise ValueError(f"不支持的周期字段: {period}")

    source_key = f"capitalflow_table_{category}"
    if not _circuit_breaker.is_available(source_key):
        logger.warning(f"[熔断] 表格数据源 {source_key} 处于熔断状态")
        raise RuntimeError(f"数据源 {source_key} 处于熔断保护状态，请稍后重试")

    _random_sleep()

    PAGE_SIZE = 100  # API 单页上限
    all_diffs: List[Dict[str, Any]] = []
    page = 1

    logger.info(f"请求东方财富表格数据: category={category}, period={period}")

    try:
        # 第一页
        diffs, total = _fetch_table_page(
            category, period, page, PAGE_SIZE, code, key, fields, source_key,
        )
        all_diffs.extend(diffs)
        logger.info(f"表格数据第 {page} 页: 获取 {len(diffs)} 条, 总计 {total} 条")

        # 翻页
        while len(all_diffs) < total:
            page += 1
            _random_sleep()
            diffs, _ = _fetch_table_page(
                category, period, page, PAGE_SIZE, code, key, fields, source_key,
            )
            all_diffs.extend(diffs)
            logger.info(f"表格数据第 {page} 页: 获取 {len(diffs)} 条, 累计 {len(all_diffs)}/{total}")

        _circuit_breaker.record_success(source_key)
        return all_diffs

    except (requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
            requests.exceptions.RequestException) as e:
        _circuit_breaker.record_failure(source_key, str(e))
        raise
    except Exception as e:
        _circuit_breaker.record_failure(source_key, str(e))
        raise


def fetch_table_data(
    category: str = "industry",
    period: str = "today",
    page: int = 1,
    page_size: int = 50,
    force_refresh: bool = False,
) -> Dict[str, Any]:
    """
    获取板块资金流表格数据（含更多列字段）。

    Args:
        category: 类别 — "industry" / "concept"
        period: 周期 — "today" / "5day" / "10day"
        page: 页码（从 1 开始）
        page_size: 每页条数（默认 50）
        force_refresh: 是否跳过缓存

    Returns:
        {
            "category": "industry",
            "period": "today",
            "total": 128,
            "page": 1,
            "page_size": 50,
            "data": [{"code": "BK1036", "name": "半导体", "price": 3485.92, ...}, ...]
        }
    """
    if category not in CATEGORY_CODE:
        raise ValueError(f"不支持的类别: {category}")
    if period not in PERIOD_KEY:
        raise ValueError(f"不支持的周期: {period}")

    if not force_refresh:
        cached = _get_table_cached(category, period)
        if cached is not None:
            all_items = cached
        else:
            all_items = None
    else:
        all_items = None

    if all_items is None:
        raw_items = _fetch_table_raw(category, period)
        flow_field = PERIOD_KEY[period]
        detail_map = PERIOD_DETAIL_FIELDS.get(period, {})

        # 解析为统一结构
        all_items = []
        for item in raw_items:
            name = item.get("f14", "")
            if not name:
                continue

            # 抽取子资金流字段
            detail_flows: Dict[str, Any] = {}
            for out_key, (raw_field, _desc) in detail_map.items():
                val = item.get(raw_field)
                if val is not None:
                    detail_flows[out_key] = val

            # 主力净流入 = 超大单 + 大单（东方财富的计算方式）
            super_large = detail_flows.get("super_large_flow") or 0
            large = detail_flows.get("large_flow") or 0
            main_flow = super_large + large

            all_items.append({
                "code": item.get("f12", ""),
                "name": name,
                "flow": item.get(flow_field, 0),
                "price": item.get("f2"),
                "change_pct": item.get("f3") or item.get("f109") or item.get("f160"),
                "company_count": item.get("f1"),
                "lead_stock_name": item.get("f260", "") or item.get("f257", "") or item.get("f204", ""),
                "lead_stock_code": item.get("f261", "") or item.get("f258", "") or item.get("f205", ""),
                "main_flow": main_flow,
                "main_ratio": detail_flows.get("main_ratio"),
                "super_large_flow": super_large,
                "super_large_ratio": detail_flows.get("super_large_ratio"),
                "large_flow": large,
                "large_ratio": detail_flows.get("large_ratio"),
                "medium_flow": detail_flows.get("medium_flow") or 0,
                "medium_ratio": detail_flows.get("medium_ratio"),
                "small_flow": detail_flows.get("small_flow") or 0,
                "small_ratio": detail_flows.get("small_ratio"),
            })

        # 按资金流降序
        all_items.sort(key=lambda x: x["flow"], reverse=True)
        _set_table_cache(category, period, all_items)

    total = len(all_items)
    total_pages = max(1, (total + page_size - 1) // page_size)
    safe_page = max(1, min(page, total_pages))
    start = (safe_page - 1) * page_size
    page_data = all_items[start:start + page_size]

    return {
        "category": category,
        "period": period,
        "total": total,
        "page": safe_page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": page_data,
    }
