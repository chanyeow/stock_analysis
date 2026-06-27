# -*- coding: utf-8 -*-
"""
===================================
知识库数据结构定义
===================================

职责：
1. 定义板块信息结构体
2. 定义股票信息结构体
3. 规范化需要写入 Markdown 的数据字段
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SectorInfo:
    """
    板块信息结构体

    用于存储从东方财富获取的板块基本信息，最终渲染为 Markdown。
    """
    code: str = ""                          # 板块代码，如 BK1036
    name: str = ""                          # 板块名称，如 半导体
    price: Optional[float] = None           # 板块指数
    change_pct: Optional[float] = None      # 涨跌幅 (%)
    company_count: Optional[int] = None     # 成分公司家数
    updated_at: Optional[int] = None        # 更新时间戳 (秒级)

    # 今日资金流
    main_flow: Optional[float] = None       # 主力净流入（元）
    main_ratio: Optional[float] = None      # 主力净流入占比 (%)
    super_large_flow: Optional[float] = None  # 超大单净流入
    super_large_ratio: Optional[float] = None
    large_flow: Optional[float] = None      # 大单净流入
    large_ratio: Optional[float] = None
    medium_flow: Optional[float] = None     # 中单净流入
    medium_ratio: Optional[float] = None
    small_flow: Optional[float] = None      # 小单净流入
    small_ratio: Optional[float] = None

    # 5日资金流
    main_flow_5d: Optional[float] = None
    main_ratio_5d: Optional[float] = None
    super_large_flow_5d: Optional[float] = None
    super_large_ratio_5d: Optional[float] = None
    large_flow_5d: Optional[float] = None
    large_ratio_5d: Optional[float] = None
    medium_flow_5d: Optional[float] = None
    medium_ratio_5d: Optional[float] = None
    small_flow_5d: Optional[float] = None
    small_ratio_5d: Optional[float] = None

    # 10日资金流
    main_flow_10d: Optional[float] = None
    main_ratio_10d: Optional[float] = None
    super_large_flow_10d: Optional[float] = None
    super_large_ratio_10d: Optional[float] = None
    large_flow_10d: Optional[float] = None
    large_ratio_10d: Optional[float] = None
    medium_flow_10d: Optional[float] = None
    medium_ratio_10d: Optional[float] = None
    small_flow_10d: Optional[float] = None
    small_ratio_10d: Optional[float] = None

    # 领涨股
    lead_stock_name: str = ""               # 领涨股名称
    lead_stock_code: str = ""               # 领涨股代码

    # 板块类别
    category: str = ""                      # "industry" 或 "concept"

    # 累计资金流（从起始日至今）
    cum_main_flow: Optional[float] = None
    cum_super_large_flow: Optional[float] = None
    cum_large_flow: Optional[float] = None
    cum_medium_flow: Optional[float] = None
    cum_small_flow: Optional[float] = None
    cum_updated_at: Optional[int] = None    # 累计更新时间戳
    cum_start_date: str = ""                # 起始日期，如 "2026-06-27"

    def to_structured_data(self) -> dict:
        """将板块信息转换为结构化数据（供前端渲染表格）"""
        def _fmt_flow(flow):
            if flow is None:
                return None
            return round(flow, 2)

        def _fmt_ratio(ratio):
            if ratio is None:
                return None
            return round(ratio, 4)

        return {
            "code": self.code,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "change_pct": self.change_pct,
            "company_count": self.company_count,
            "lead_stock_name": self.lead_stock_name,
            "lead_stock_code": self.lead_stock_code,
            "today": [
                {"label": "主力", "flow": _fmt_flow(self.main_flow), "ratio": _fmt_ratio(self.main_ratio)},
                {"label": "超大单", "flow": _fmt_flow(self.super_large_flow), "ratio": _fmt_ratio(self.super_large_ratio)},
                {"label": "大单", "flow": _fmt_flow(self.large_flow), "ratio": _fmt_ratio(self.large_ratio)},
                {"label": "中单", "flow": _fmt_flow(self.medium_flow), "ratio": _fmt_ratio(self.medium_ratio)},
                {"label": "小单", "flow": _fmt_flow(self.small_flow), "ratio": _fmt_ratio(self.small_ratio)},
            ],
            "5day": [
                {"label": "主力", "flow": _fmt_flow(self.main_flow_5d), "ratio": _fmt_ratio(self.main_ratio_5d)},
                {"label": "超大单", "flow": _fmt_flow(self.super_large_flow_5d), "ratio": _fmt_ratio(self.super_large_ratio_5d)},
                {"label": "大单", "flow": _fmt_flow(self.large_flow_5d), "ratio": _fmt_ratio(self.large_ratio_5d)},
                {"label": "中单", "flow": _fmt_flow(self.medium_flow_5d), "ratio": _fmt_ratio(self.medium_ratio_5d)},
                {"label": "小单", "flow": _fmt_flow(self.small_flow_5d), "ratio": _fmt_ratio(self.small_ratio_5d)},
            ],
            "10day": [
                {"label": "主力", "flow": _fmt_flow(self.main_flow_10d), "ratio": _fmt_ratio(self.main_ratio_10d)},
                {"label": "超大单", "flow": _fmt_flow(self.super_large_flow_10d), "ratio": _fmt_ratio(self.super_large_ratio_10d)},
                {"label": "大单", "flow": _fmt_flow(self.large_flow_10d), "ratio": _fmt_ratio(self.large_ratio_10d)},
                {"label": "中单", "flow": _fmt_flow(self.medium_flow_10d), "ratio": _fmt_ratio(self.medium_ratio_10d)},
                {"label": "小单", "flow": _fmt_flow(self.small_flow_10d), "ratio": _fmt_ratio(self.small_ratio_10d)},
            ],
            "cumulative": [
                {"label": "主力", "flow": _fmt_flow(self.cum_main_flow)},
                {"label": "超大单", "flow": _fmt_flow(self.cum_super_large_flow)},
                {"label": "大单", "flow": _fmt_flow(self.cum_large_flow)},
                {"label": "中单", "flow": _fmt_flow(self.cum_medium_flow)},
                {"label": "小单", "flow": _fmt_flow(self.cum_small_flow)},
            ],
            "cum_start_date": self.cum_start_date,
            "cum_updated_at": self.cum_updated_at,
            "updated_at": self.updated_at,
        }

    def to_markdown(self) -> str:
        """将板块信息渲染为 Markdown 格式"""
        import json

        lines = []
        lines.append(f"# {self.name} ({self.code})")
        lines.append("")

        # 基本信息
        lines.append("## 基本信息")
        lines.append("")
        lines.append(f"- **板块代码**: {self.code}")
        lines.append(f"- **板块名称**: {self.name}")
        if self.category:
            cat_label = "行业板块" if self.category == "industry" else "概念板块"
            lines.append(f"- **板块类型**: {cat_label}")
        if self.price is not None:
            lines.append(f"- **板块指数**: {self.price:.2f}")
        if self.change_pct is not None:
            lines.append(f"- **涨跌幅**: {self.change_pct:+.2f}%")
        if self.company_count is not None:
            lines.append(f"- **成分公司数**: {self.company_count}")
        if self.lead_stock_name:
            lines.append(f"- **领涨股**: {self.lead_stock_name} ({self.lead_stock_code})")
        lines.append("")

        # 今日资金流
        lines.append("## 今日资金流")
        lines.append("")
        lines.append("| 类型 | 净流入(元) | 占比 |")
        lines.append("|------|-----------|------|")
        rows = [
            ("主力", self.main_flow, self.main_ratio),
            ("超大单", self.super_large_flow, self.super_large_ratio),
            ("大单", self.large_flow, self.large_ratio),
            ("中单", self.medium_flow, self.medium_ratio),
            ("小单", self.small_flow, self.small_ratio),
        ]
        for label, flow, ratio in rows:
            flow_str = format_flow(flow) if flow is not None else "-"
            ratio_str = f"{ratio:+.2f}%" if ratio is not None else "-"
            lines.append(f"| {label} | {flow_str} | {ratio_str} |")
        lines.append("")

        # 5日资金流
        lines.append("## 5日资金流")
        lines.append("")
        lines.append("| 类型 | 净流入(元) | 占比 |")
        lines.append("|------|-----------|------|")
        rows_5d = [
            ("主力", self.main_flow_5d, self.main_ratio_5d),
            ("超大单", self.super_large_flow_5d, self.super_large_ratio_5d),
            ("大单", self.large_flow_5d, self.large_ratio_5d),
            ("中单", self.medium_flow_5d, self.medium_ratio_5d),
            ("小单", self.small_flow_5d, self.small_ratio_5d),
        ]
        for label, flow, ratio in rows_5d:
            flow_str = format_flow(flow) if flow is not None else "-"
            ratio_str = f"{ratio:+.2f}%" if ratio is not None else "-"
            lines.append(f"| {label} | {flow_str} | {ratio_str} |")
        lines.append("")

        # 10日资金流
        lines.append("## 10日资金流")
        lines.append("")
        lines.append("| 类型 | 净流入(元) | 占比 |")
        lines.append("|------|-----------|------|")
        rows_10d = [
            ("主力", self.main_flow_10d, self.main_ratio_10d),
            ("超大单", self.super_large_flow_10d, self.super_large_ratio_10d),
            ("大单", self.large_flow_10d, self.large_ratio_10d),
            ("中单", self.medium_flow_10d, self.medium_ratio_10d),
            ("小单", self.small_flow_10d, self.small_ratio_10d),
        ]
        for label, flow, ratio in rows_10d:
            flow_str = format_flow(flow) if flow is not None else "-"
            ratio_str = f"{ratio:+.2f}%" if ratio is not None else "-"
            lines.append(f"| {label} | {flow_str} | {ratio_str} |")
        lines.append("")

        # 更新时间
        if self.updated_at is not None:
            from datetime import datetime, timezone, timedelta
            dt = datetime.fromtimestamp(self.updated_at, tz=timezone(timedelta(hours=8)))
            lines.append("## 更新时间")
            lines.append("")
            lines.append(f"- **数据更新时间**: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append("")

        # 累计资金流（从起始日至今）
        if self.cum_main_flow is not None:
            from datetime import datetime, timezone, timedelta
            cum_dt_str = ""
            if self.cum_updated_at:
                cum_dt = datetime.fromtimestamp(self.cum_updated_at, tz=timezone(timedelta(hours=8)))
                cum_dt_str = cum_dt.strftime('%Y-%m-%d %H:%M:%S')

            lines.append(f"## 历史资金流（{self.cum_start_date}起）")
            lines.append(f"最后更新时间：{cum_dt_str}")
            lines.append("")
            lines.append("| 类型 | 累计净流入(元) |")
            lines.append("|------|---------------|")
            cum_rows = [
                ("主力", self.cum_main_flow),
                ("超大单", self.cum_super_large_flow),
                ("大单", self.cum_large_flow),
                ("中单", self.cum_medium_flow),
                ("小单", self.cum_small_flow),
            ]
            for label, flow in cum_rows:
                flow_str = format_flow(flow) if flow is not None else "-"
                lines.append(f"| {label} | {flow_str} |")
            lines.append("")

        # 追加结构化数据（供前端渲染）
        lines.append("---")
        lines.append("")
        lines.append("<!-- structured-data")
        lines.append(json.dumps(self.to_structured_data(), ensure_ascii=False, indent=2))
        lines.append("structured-data -->")

        return "\n".join(lines)


@dataclass
class StockInfo:
    """
    股票信息结构体

    用于存储股票基本信息，最终渲染为 Markdown。
    暂时留空，待后续实现数据源。
    """
    code: str = ""                          # 股票代码，如 600519
    name: str = ""                          # 股票名称，如 贵州茅台
    market: str = ""                        # 市场: sh(沪市) / sz(深市)

    # TODO: 后续添加更多字段
    # price: Optional[float] = None
    # change_pct: Optional[float] = None
    # volume: Optional[float] = None
    # turnover: Optional[float] = None
    # market_cap: Optional[float] = None
    # pe_ratio: Optional[float] = None
    # pb_ratio: Optional[float] = None

    def to_markdown(self) -> str:
        """将股票信息渲染为 Markdown 格式"""
        lines = []
        lines.append(f"# {self.name} ({self.code})")
        lines.append("")
        lines.append("## 基本信息")
        lines.append("")
        lines.append(f"- **股票代码**: {self.code}")
        lines.append(f"- **股票名称**: {self.name}")
        if self.market:
            market_label = "沪市" if self.market == "sh" else "深市"
            lines.append(f"- **上市市场**: {market_label}")
        lines.append("")
        lines.append("> 暂无更多数据，股票数据源待实现。")
        lines.append("")
        return "\n".join(lines)


@dataclass
class KnowledgeItem:
    """
    知识库条目

    用于前端展示的摘要信息，不需要完整的资金流数据。
    """
    code: str = ""          # 代码，如 BK1036 / 600519
    name: str = ""          # 名称，如 半导体 / 贵州茅台
    category: str = ""      # 类别: bk(板块) / sh(沪市) / sz(深市)
    change_pct: Optional[float] = None  # 涨跌幅（仅板块有）


@dataclass
class CrawlProgress:
    """
    爬取进度
    """
    total: int = 0              # 总数
    current: int = 0            # 当前进度
    status: str = "idle"        # 状态: idle / crawling / done / error
    message: str = ""           # 状态消息
    errors: List[str] = field(default_factory=list)  # 错误列表


def format_flow(value: Optional[float]) -> str:
    """格式化资金流数值"""
    if value is None:
        return "-"
    abs_val = abs(value)
    if abs_val >= 1e8:
        return f"{value / 1e8:+.2f} 亿"
    if abs_val >= 1e4:
        return f"{value / 1e4:+.2f} 万"
    return f"{value:+.0f}"
