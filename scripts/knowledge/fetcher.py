# -*- coding: utf-8 -*-
"""
===================================
知识库数据爬取器
===================================

职责：
1. 爬取板块数据（行业 + 概念），写入 Markdown 文件
2. 爬取股票数据（暂时留空）
3. 提供进度回调

数据来源：
- 板块数据：复用 scripts/capitalflow/fetcher.py
- 股票数据：待实现

防封禁策略：
- 复用 capitalflow 的防护策略（随机休眠、UA轮换、熔断器）
"""

import logging
import os
import time
from pathlib import Path
from typing import Callable, Dict, List, Optional

from scripts.capitalflow.fetcher import fetch_table_data
from scripts.knowledge.types import (
    CrawlProgress,
    KnowledgeItem,
    SectorInfo,
    StockInfo,
)

logger = logging.getLogger(__name__)

# res 目录路径
RES_DIR = Path(__file__).parent.parent.parent / "res"


def _get_res_dir() -> Path:
    """获取 res 目录路径"""
    return RES_DIR


def _ensure_dir(path: Path) -> None:
    """确保目录存在"""
    path.mkdir(parents=True, exist_ok=True)


def _write_markdown(filepath: Path, content: str) -> None:
    """写入 Markdown 文件"""
    _ensure_dir(filepath.parent)
    filepath.write_text(content, encoding="utf-8")


def _sector_to_info(item: Dict, category: str) -> SectorInfo:
    """将 API 返回的条目转换为 SectorInfo"""
    return SectorInfo(
        code=item.get("code", ""),
        name=item.get("name", ""),
        price=item.get("price"),
        change_pct=item.get("change_pct"),
        company_count=item.get("company_count"),
        updated_at=item.get("updated_at"),
        main_flow=item.get("main_flow"),
        main_ratio=item.get("main_ratio"),
        super_large_flow=item.get("super_large_flow"),
        super_large_ratio=item.get("super_large_ratio"),
        large_flow=item.get("large_flow"),
        large_ratio=item.get("large_ratio"),
        medium_flow=item.get("medium_flow"),
        medium_ratio=item.get("medium_ratio"),
        small_flow=item.get("small_flow"),
        small_ratio=item.get("small_ratio"),
        lead_stock_name=item.get("lead_stock_name", ""),
        lead_stock_code=item.get("lead_stock_code", ""),
        category=category,
    )


def crawl_sectors(
    on_progress: Optional[Callable[[CrawlProgress], None]] = None,
) -> List[KnowledgeItem]:
    """
    爬取板块数据并写入 Markdown 文件。

    Args:
        on_progress: 进度回调函数

    Returns:
        知识库条目列表
    """
    res_dir = _get_res_dir()
    bk_dir = res_dir / "bk"
    _ensure_dir(bk_dir)

    all_items: List[KnowledgeItem] = []
    progress = CrawlProgress(status="crawling", message="开始爬取板块数据...")

    if on_progress:
        on_progress(progress)

    # 爬取行业板块
    logger.info("开始爬取行业板块...")
    progress.message = "正在爬取行业板块..."
    if on_progress:
        on_progress(progress)

    try:
        industry_data = fetch_table_data(
            category="industry",
            period="today",
            page=1,
            page_size=200,
            force_refresh=True,
        )
        industry_items = industry_data.get("data", [])
        progress.total += len(industry_items)
        logger.info(f"获取到 {len(industry_items)} 个行业板块")
    except Exception as e:
        logger.error(f"爬取行业板块失败: {e}")
        progress.errors.append(f"行业板块爬取失败: {str(e)}")
        industry_items = []

    # 爬取概念板块
    logger.info("开始爬取概念板块...")
    progress.message = "正在爬取概念板块..."
    if on_progress:
        on_progress(progress)

    try:
        concept_data = fetch_table_data(
            category="concept",
            period="today",
            page=1,
            page_size=500,
            force_refresh=True,
        )
        concept_items = concept_data.get("data", [])
        progress.total += len(concept_items)
        logger.info(f"获取到 {len(concept_items)} 个概念板块")
    except Exception as e:
        logger.error(f"爬取概念板块失败: {e}")
        progress.errors.append(f"概念板块爬取失败: {str(e)}")
        concept_items = []

    # 处理行业板块（获取5日和10日数据）
    logger.info("开始获取行业板块5日和10日数据...")
    progress.message = "正在获取行业板块历史资金流..."
    if on_progress:
        on_progress(progress)

    # 获取5日和10日数据
    industry_5d = {}
    industry_10d = {}
    try:
        industry_5d_data = fetch_table_data(
            category="industry",
            period="5day",
            page=1,
            page_size=200,
            force_refresh=True,
        )
        for item in industry_5d_data.get("data", []):
            industry_5d[item.get("code", "")] = item
    except Exception as e:
        logger.warning(f"获取行业板块5日数据失败: {e}")

    try:
        industry_10d_data = fetch_table_data(
            category="industry",
            period="10day",
            page=1,
            page_size=200,
            force_refresh=True,
        )
        for item in industry_10d_data.get("data", []):
            industry_10d[item.get("code", "")] = item
    except Exception as e:
        logger.warning(f"获取行业板块10日数据失败: {e}")

    # 处理行业板块
    for item in industry_items:
        code = item.get("code", "")
        if not code:
            continue

        info = _sector_to_info(item, "industry")

        # 合并5日数据
        if code in industry_5d:
            d5 = industry_5d[code]
            info.main_flow_5d = d5.get("main_flow")
            info.main_ratio_5d = d5.get("main_ratio")
            info.super_large_flow_5d = d5.get("super_large_flow")
            info.super_large_ratio_5d = d5.get("super_large_ratio")
            info.large_flow_5d = d5.get("large_flow")
            info.large_ratio_5d = d5.get("large_ratio")
            info.medium_flow_5d = d5.get("medium_flow")
            info.medium_ratio_5d = d5.get("medium_ratio")
            info.small_flow_5d = d5.get("small_flow")
            info.small_ratio_5d = d5.get("small_ratio")

        # 合并10日数据
        if code in industry_10d:
            d10 = industry_10d[code]
            info.main_flow_10d = d10.get("main_flow")
            info.main_ratio_10d = d10.get("main_ratio")
            info.super_large_flow_10d = d10.get("super_large_flow")
            info.super_large_ratio_10d = d10.get("super_large_ratio")
            info.large_flow_10d = d10.get("large_flow")
            info.large_ratio_10d = d10.get("large_ratio")
            info.medium_flow_10d = d10.get("medium_flow")
            info.medium_ratio_10d = d10.get("medium_ratio")
            info.small_flow_10d = d10.get("small_flow")
            info.small_ratio_10d = d10.get("small_ratio")

        # 更新累计资金流
        if info.updated_at and info.main_flow is not None:
            cum_state = update_cumulative_flow(
                code=code,
                today_main_flow=info.main_flow or 0,
                today_super_large_flow=info.super_large_flow or 0,
                today_large_flow=info.large_flow or 0,
                today_medium_flow=info.medium_flow or 0,
                today_small_flow=info.small_flow or 0,
                current_timestamp=info.updated_at,
            )
            info.cum_main_flow = cum_state.get("cum_main_flow")
            info.cum_super_large_flow = cum_state.get("cum_super_large_flow")
            info.cum_large_flow = cum_state.get("cum_large_flow")
            info.cum_medium_flow = cum_state.get("cum_medium_flow")
            info.cum_small_flow = cum_state.get("cum_small_flow")
            info.cum_updated_at = cum_state.get("updated_at")
            info.cum_start_date = CUM_START_DATE

        # 写入 Markdown
        md_path = bk_dir / f"{code}.md"
        _write_markdown(md_path, info.to_markdown())

        all_items.append(KnowledgeItem(
            code=code,
            name=info.name,
            category="bk",
            change_pct=info.change_pct,
        ))

        progress.current += 1
        progress.message = f"已处理行业板块: {info.name} ({progress.current}/{progress.total})"
        if on_progress:
            on_progress(progress)

    # 处理概念板块（获取5日和10日数据）
    logger.info("开始获取概念板块5日和10日数据...")
    progress.message = "正在获取概念板块历史资金流..."
    if on_progress:
        on_progress(progress)

    concept_5d = {}
    concept_10d = {}
    try:
        concept_5d_data = fetch_table_data(
            category="concept",
            period="5day",
            page=1,
            page_size=500,
            force_refresh=True,
        )
        for item in concept_5d_data.get("data", []):
            concept_5d[item.get("code", "")] = item
    except Exception as e:
        logger.warning(f"获取概念板块5日数据失败: {e}")

    try:
        concept_10d_data = fetch_table_data(
            category="concept",
            period="10day",
            page=1,
            page_size=500,
            force_refresh=True,
        )
        for item in concept_10d_data.get("data", []):
            concept_10d[item.get("code", "")] = item
    except Exception as e:
        logger.warning(f"获取概念板块10日数据失败: {e}")

    # 处理概念板块
    for item in concept_items:
        code = item.get("code", "")
        if not code:
            continue

        info = _sector_to_info(item, "concept")

        # 合并5日数据
        if code in concept_5d:
            d5 = concept_5d[code]
            info.main_flow_5d = d5.get("main_flow")
            info.main_ratio_5d = d5.get("main_ratio")
            info.super_large_flow_5d = d5.get("super_large_flow")
            info.super_large_ratio_5d = d5.get("super_large_ratio")
            info.large_flow_5d = d5.get("large_flow")
            info.large_ratio_5d = d5.get("large_ratio")
            info.medium_flow_5d = d5.get("medium_flow")
            info.medium_ratio_5d = d5.get("medium_ratio")
            info.small_flow_5d = d5.get("small_flow")
            info.small_ratio_5d = d5.get("small_ratio")

        # 合并10日数据
        if code in concept_10d:
            d10 = concept_10d[code]
            info.main_flow_10d = d10.get("main_flow")
            info.main_ratio_10d = d10.get("main_ratio")
            info.super_large_flow_10d = d10.get("super_large_flow")
            info.super_large_ratio_10d = d10.get("super_large_ratio")
            info.large_flow_10d = d10.get("large_flow")
            info.large_ratio_10d = d10.get("large_ratio")
            info.medium_flow_10d = d10.get("medium_flow")
            info.medium_ratio_10d = d10.get("medium_ratio")
            info.small_flow_10d = d10.get("small_flow")
            info.small_ratio_10d = d10.get("small_ratio")

        # 更新累计资金流
        if info.updated_at and info.main_flow is not None:
            cum_state = update_cumulative_flow(
                code=code,
                today_main_flow=info.main_flow or 0,
                today_super_large_flow=info.super_large_flow or 0,
                today_large_flow=info.large_flow or 0,
                today_medium_flow=info.medium_flow or 0,
                today_small_flow=info.small_flow or 0,
                current_timestamp=info.updated_at,
            )
            info.cum_main_flow = cum_state.get("cum_main_flow")
            info.cum_super_large_flow = cum_state.get("cum_super_large_flow")
            info.cum_large_flow = cum_state.get("cum_large_flow")
            info.cum_medium_flow = cum_state.get("cum_medium_flow")
            info.cum_small_flow = cum_state.get("cum_small_flow")
            info.cum_updated_at = cum_state.get("updated_at")
            info.cum_start_date = CUM_START_DATE

        # 写入 Markdown
        md_path = bk_dir / f"{code}.md"
        _write_markdown(md_path, info.to_markdown())

        all_items.append(KnowledgeItem(
            code=code,
            name=info.name,
            category="bk",
            change_pct=info.change_pct,
        ))

        progress.current += 1
        progress.message = f"已处理概念板块: {info.name} ({progress.current}/{progress.total})"
        if on_progress:
            on_progress(progress)

    progress.status = "done"
    progress.message = f"板块数据爬取完成，共 {len(all_items)} 个板块"
    if on_progress:
        on_progress(progress)

    logger.info(f"板块数据爬取完成，共 {len(all_items)} 个板块")
    return all_items


def crawl_stocks(
    on_progress: Optional[Callable[[CrawlProgress], None]] = None,
) -> List[KnowledgeItem]:
    """
    爬取股票数据并写入 Markdown 文件。

    暂时留空，待后续实现数据源。

    Args:
        on_progress: 进度回调函数

    Returns:
        知识库条目列表
    """
    # TODO: 实现股票数据爬取
    logger.info("股票数据爬取暂未实现")
    return []


def crawl_all(
    on_progress: Optional[Callable[[CrawlProgress], None]] = None,
) -> List[KnowledgeItem]:
    """
    爬取所有知识库数据。

    Args:
        on_progress: 进度回调函数

    Returns:
        知识库条目列表
    """
    all_items: List[KnowledgeItem] = []

    # 爬取板块
    sector_items = crawl_sectors(on_progress)
    all_items.extend(sector_items)

    # 爬取股票（暂时为空）
    stock_items = crawl_stocks(on_progress)
    all_items.extend(stock_items)

    return all_items


def load_existing_items() -> List[KnowledgeItem]:
    """
    从 res 目录加载已有的知识库条目。

    Returns:
        知识库条目列表
    """
    res_dir = _get_res_dir()
    items: List[KnowledgeItem] = []

    # 扫描板块
    bk_dir = res_dir / "bk"
    if bk_dir.exists():
        for md_file in bk_dir.glob("*.md"):
            code = md_file.stem
            # 从文件中提取名称
            name = _extract_name_from_markdown(md_file)
            items.append(KnowledgeItem(
                code=code,
                name=name,
                category="bk",
            ))

    # 扫描沪市
    sh_dir = res_dir / "sh"
    if sh_dir.exists():
        for md_file in sh_dir.glob("*.md"):
            code = md_file.stem
            name = _extract_name_from_markdown(md_file)
            items.append(KnowledgeItem(
                code=code,
                name=name,
                category="sh",
            ))

    # 扫描深市
    sz_dir = res_dir / "sz"
    if sz_dir.exists():
        for md_file in sz_dir.glob("*.md"):
            code = md_file.stem
            name = _extract_name_from_markdown(md_file)
            items.append(KnowledgeItem(
                code=code,
                name=name,
                category="sz",
            ))

    return items


def _extract_name_from_markdown(filepath: Path) -> str:
    """从 Markdown 文件中提取名称"""
    try:
        content = filepath.read_text(encoding="utf-8")
        # 查找第一个 # 标题
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("# ") and "(" in line:
                # 格式: # 板块名称 (BK1036)
                return line[2:line.index("(")].strip()
            elif line.startswith("# "):
                return line[2:].strip()
    except Exception:
        pass
    return filepath.stem


def read_markdown(code: str, category: str) -> Optional[str]:
    """
    读取指定条目的 Markdown 内容。

    Args:
        code: 代码
        category: 类别 (bk/sh/sz)

    Returns:
        Markdown 内容，不存在则返回 None
    """
    res_dir = _get_res_dir()
    md_path = res_dir / category / f"{code}.md"

    if md_path.exists():
        return md_path.read_text(encoding="utf-8")
    return None


def search_items(keyword: str) -> List[KnowledgeItem]:
    """
    搜索知识库条目（按文件名搜索）。

    Args:
        keyword: 搜索关键词

    Returns:
        匹配的知识库条目列表
    """
    all_items = load_existing_items()
    keyword_lower = keyword.lower()

    return [
        item for item in all_items
        if keyword_lower in item.code.lower() or keyword_lower in item.name.lower()
    ]


def load_capital_flow_data(category: str = "industry") -> Optional[Dict]:
    """
    从 Markdown 文件加载板块资金流数据（结构化 JSON）。

    读取 res/bk/ 目录下所有板块的 Markdown 文件，提取其中的 structured-data JSON 块，
    组装成与原 capitalflow API 相同格式的数据。

    Args:
        category: "industry" (行业) 或 "concept" (概念)

    Returns:
        {
            "category": "industry",
            "period": "today",
            "total": 128,
            "data": [
                {"code": "BK1036", "name": "半导体", "flow": 5243314176.0},
                ...
            ]
        }
        如果没有任何数据则返回 None
    """
    import json
    import re

    res_dir = _get_res_dir()
    bk_dir = res_dir / "bk"

    if not bk_dir.exists():
        return None

    items = []
    pattern = re.compile(r'<!-- structured-data\n([\s\S]*?)\nstructured-data -->')

    for md_file in bk_dir.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            match = pattern.search(content)
            if match:
                data = json.loads(match.group(1))
                # 根据 category 筛选
                file_category = data.get("category", "")
                if category == "industry" and file_category != "industry":
                    continue
                if category == "concept" and file_category != "concept":
                    continue

                # 取今日主力资金流作为 flow
                today_data = data.get("today", [])
                flow = 0
                for item in today_data:
                    if item.get("label") == "主力" and item.get("flow") is not None:
                        flow = item["flow"]
                        break

                items.append({
                    "code": data.get("code", md_file.stem),
                    "name": data.get("name", ""),
                    "flow": flow,
                })
        except Exception as e:
            logger.warning(f"解析 Markdown 文件失败: {md_file.name}: {e}")

    if not items:
        return None

    # 按资金流降序排列
    items.sort(key=lambda x: x["flow"], reverse=True)

    return {
        "category": category,
        "period": "today",
        "total": len(items),
        "data": items,
    }


def load_capital_flow_table_data(
    category: str = "industry",
    period: str = "today",
    page: int = 1,
    page_size: int = 50,
) -> Optional[Dict]:
    """
    从 Markdown 文件加载板块资金流表格数据（结构化 JSON）。

    Args:
        category: "industry" (行业) 或 "concept" (概念)
        period: "today" / "5day" / "10day"
        page: 页码
        page_size: 每页条数

    Returns:
        与原 capitalflow API 相同格式的表格数据
    """
    import json
    import re

    res_dir = _get_res_dir()
    bk_dir = res_dir / "bk"

    if not bk_dir.exists():
        return None

    items = []
    pattern = re.compile(r'<!-- structured-data\n([\s\S]*?)\nstructured-data -->')

    for md_file in bk_dir.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            match = pattern.search(content)
            if match:
                data = json.loads(match.group(1))
                # 根据 category 筛选
                file_category = data.get("category", "")
                if category == "industry" and file_category != "industry":
                    continue
                if category == "concept" and file_category != "concept":
                    continue

                # 获取对应周期的数据
                period_data = data.get(period, [])
                flow = 0
                main_flow = 0
                super_large_flow = 0
                large_flow = 0
                medium_flow = 0
                small_flow = 0
                main_ratio = None
                super_large_ratio = None
                large_ratio = None
                medium_ratio = None
                small_ratio = None

                for item in period_data:
                    label = item.get("label", "")
                    item_flow = item.get("flow")
                    item_ratio = item.get("ratio")

                    if label == "主力":
                        flow = item_flow or 0
                        main_flow = item_flow or 0
                        main_ratio = item_ratio
                    elif label == "超大单":
                        super_large_flow = item_flow or 0
                        super_large_ratio = item_ratio
                    elif label == "大单":
                        large_flow = item_flow or 0
                        large_ratio = item_ratio
                    elif label == "中单":
                        medium_flow = item_flow or 0
                        medium_ratio = item_ratio
                    elif label == "小单":
                        small_flow = item_flow or 0
                        small_ratio = item_ratio

                items.append({
                    "code": data.get("code", md_file.stem),
                    "name": data.get("name", ""),
                    "flow": flow,
                    "price": data.get("price"),
                    "change_pct": data.get("change_pct"),
                    "company_count": data.get("company_count"),
                    "lead_stock_name": data.get("lead_stock_name", ""),
                    "lead_stock_code": data.get("lead_stock_code", ""),
                    "main_flow": main_flow,
                    "main_ratio": main_ratio,
                    "super_large_flow": super_large_flow,
                    "super_large_ratio": super_large_ratio,
                    "large_flow": large_flow,
                    "large_ratio": large_ratio,
                    "medium_flow": medium_flow,
                    "medium_ratio": medium_ratio,
                    "small_flow": small_flow,
                    "small_ratio": small_ratio,
                })
        except Exception as e:
            logger.warning(f"解析 Markdown 文件失败: {md_file.name}: {e}")

    if not items:
        return None

    # 按资金流降序排列
    items.sort(key=lambda x: x["flow"], reverse=True)

    total = len(items)
    total_pages = max(1, (total + page_size - 1) // page_size)
    safe_page = max(1, min(page, total_pages))
    start = (safe_page - 1) * page_size
    page_data = items[start:start + page_size]

    return {
        "category": category,
        "period": period,
        "total": total,
        "page": safe_page,
        "page_size": page_size,
        "total_pages": total_pages,
        "data": page_data,
    }


# ============================================================
# 累计资金流状态管理
# ============================================================

# 起始日期（首次爬取的日期）
CUM_START_DATE = "2026-06-27"


def _get_cumulative_path() -> Path:
    """获取累计状态文件路径"""
    return _get_res_dir().parent / "res" / "bk" / "_cumulative.json"


def load_cumulative_state() -> Dict:
    """
    加载累计资金流状态。

    返回格式:
    {
        "start_date": "2026-06-27",
        "last_updated_at": 1782459587,
        "sectors": {
            "BK0420": {
                "cum_main_flow": 123456789.0,
                "cum_super_large_flow": ...,
                "cum_large_flow": ...,
                "cum_medium_flow": ...,
                "cum_small_flow": ...,
                "updated_at": 1782459587,
            },
            ...
        }
    }
    """
    import json

    path = _get_cumulative_path()
    if not path.exists():
        return {"start_date": CUM_START_DATE, "last_updated_at": None, "sectors": {}}

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"加载累计状态失败: {e}")
        return {"start_date": CUM_START_DATE, "last_updated_at": None, "sectors": {}}


def save_cumulative_state(state: Dict) -> None:
    """保存累计资金流状态"""
    import json

    path = _get_cumulative_path()
    _ensure_dir(path.parent)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def update_cumulative_flow(
    code: str,
    today_main_flow: float,
    today_super_large_flow: float,
    today_large_flow: float,
    today_medium_flow: float,
    today_small_flow: float,
    current_timestamp: int,
) -> Dict:
    """
    更新单个板块的累计资金流。

    逻辑:
    1. 读取现有累计状态
    2. 只有当爬到的时间戳 > 上次更新时间戳时，才累加数据
    3. 如果时间戳相同或更小，跳过（防止重复计算）
    4. 保存更新后的状态

    注意: f124 是 API 返回的数据更新时间戳，代表这组数据的"新鲜度"。
    - 交易日: f124 通常在收盘后更新
    - 非交易日(周末): f124 保持上一个交易日的值
    - 所以周末多次爬取不会重复计算

    Args:
        code: 板块代码
        today_main_flow: 今日主力净流入
        today_super_large_flow: 今日超大单净流入
        today_large_flow: 今日大单净流入
        today_medium_flow: 今日中单净流入
        today_small_flow: 今日小单净流入
        current_timestamp: API 返回的数据时间戳 (f124)

    Returns:
        更新后的累计数据
    """
    from datetime import datetime, timezone, timedelta

    state = load_cumulative_state()
    sectors = state.get("sectors", {})

    sector_state = sectors.get(code, {})
    last_updated = sector_state.get("updated_at")

    # 如果是首次运行，设置起始日期
    if not state.get("start_date"):
        dt = datetime.fromtimestamp(current_timestamp, tz=timezone(timedelta(hours=8)))
        state["start_date"] = dt.strftime("%Y-%m-%d")

    # 严格检查: 只有当爬到的时间戳 > 上次更新时间戳时才计算
    # 这样可以确保:
    # 1. 周末多次爬取不会重复计算 (f124 相同)
    # 2. 只有当数据真正更新时才累加
    if last_updated and current_timestamp <= last_updated:
        logger.debug(
            f"板块 {code} 数据未更新 (当前={current_timestamp}, 上次={last_updated})，跳过累计计算"
        )
        return sector_state

    # 累加今日数据
    cum_main = (sector_state.get("cum_main_flow") or 0) + today_main_flow
    cum_super_large = (sector_state.get("cum_super_large_flow") or 0) + today_super_large_flow
    cum_large = (sector_state.get("cum_large_flow") or 0) + today_large_flow
    cum_medium = (sector_state.get("cum_medium_flow") or 0) + today_medium_flow
    cum_small = (sector_state.get("cum_small_flow") or 0) + today_small_flow

    sectors[code] = {
        "cum_main_flow": cum_main,
        "cum_super_large_flow": cum_super_large,
        "cum_large_flow": cum_large,
        "cum_medium_flow": cum_medium,
        "cum_small_flow": cum_small,
        "updated_at": current_timestamp,
    }

    state["sectors"] = sectors
    state["last_updated_at"] = current_timestamp

    save_cumulative_state(state)

    return sectors[code]


def get_cumulative_for_sector(code: str) -> Optional[Dict]:
    """获取单个板块的累计资金流数据"""
    state = load_cumulative_state()
    return state.get("sectors", {}).get(code)
