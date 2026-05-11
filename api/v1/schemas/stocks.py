# -*- coding: utf-8 -*-
"""
===================================
股票数据相关模型
===================================

职责：
1. 定义股票实时行情模型
2. 定义历史 K 线数据模型
"""

from typing import Optional, List

from pydantic import BaseModel, Field


class StockQuote(BaseModel):
    """股票实时行情"""
    
    stock_code: str = Field(..., description="股票代码")
    stock_name: Optional[str] = Field(None, description="股票名称")
    current_price: float = Field(..., description="当前价格")
    change: Optional[float] = Field(None, description="涨跌额")
    change_percent: Optional[float] = Field(None, description="涨跌幅 (%)")
    open: Optional[float] = Field(None, description="开盘价")
    high: Optional[float] = Field(None, description="最高价")
    low: Optional[float] = Field(None, description="最低价")
    prev_close: Optional[float] = Field(None, description="昨收价")
    volume: Optional[float] = Field(None, description="成交量（股）")
    amount: Optional[float] = Field(None, description="成交额（元）")
    update_time: Optional[str] = Field(None, description="更新时间")
    
    class Config:
        json_schema_extra = {
            "example": {
                "stock_code": "600519",
                "stock_name": "贵州茅台",
                "current_price": 1800.00,
                "change": 15.00,
                "change_percent": 0.84,
                "open": 1785.00,
                "high": 1810.00,
                "low": 1780.00,
                "prev_close": 1785.00,
                "volume": 10000000,
                "amount": 18000000000,
                "update_time": "2024-01-01T15:00:00"
            }
        }


class KLineData(BaseModel):
    """K 线数据点"""
    
    date: str = Field(..., description="日期")
    open: float = Field(..., description="开盘价")
    high: float = Field(..., description="最高价")
    low: float = Field(..., description="最低价")
    close: float = Field(..., description="收盘价")
    volume: Optional[float] = Field(None, description="成交量")
    amount: Optional[float] = Field(None, description="成交额")
    change_percent: Optional[float] = Field(None, description="涨跌幅 (%)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "date": "2024-01-01",
                "open": 1785.00,
                "high": 1810.00,
                "low": 1780.00,
                "close": 1800.00,
                "volume": 10000000,
                "amount": 18000000000,
                "change_percent": 0.84
            }
        }


class ExtractItem(BaseModel):
    """单条提取结果（代码、名称、置信度）"""

    code: Optional[str] = Field(None, description="股票代码，None 表示解析失败")
    name: Optional[str] = Field(None, description="股票名称（如有）")
    confidence: str = Field("medium", description="置信度：high/medium/low")


class ExtractFromImageResponse(BaseModel):
    """图片股票代码提取响应"""

    codes: List[str] = Field(..., description="提取的股票代码（已去重，向后兼容）")
    items: List[ExtractItem] = Field(default_factory=list, description="提取结果明细（代码+名称+置信度）")
    raw_text: Optional[str] = Field(None, description="原始 LLM 响应（调试用）")


class StockHistoryResponse(BaseModel):
    """股票历史行情响应"""

    stock_code: str = Field(..., description="股票代码")
    stock_name: Optional[str] = Field(None, description="股票名称")
    period: str = Field(..., description="K 线周期")
    data: List[KLineData] = Field(default_factory=list, description="K 线数据列表")

    class Config:
        json_schema_extra = {
            "example": {
                "stock_code": "600519",
                "stock_name": "贵州茅台",
                "period": "daily",
                "data": []
            }
        }


class IndustrySwResponse(BaseModel):
    """申万行业分类响应"""

    stock_code: str = Field(..., description="股票代码")
    industry_name: Optional[str] = Field(None, description="行业名称")
    industry_code: Optional[str] = Field(None, description="行业代码")


class ConceptItem(BaseModel):
    """概念/板块项"""

    name: str = Field(..., description="名称")
    code: Optional[str] = Field(None, description="代码")


class ConceptListResponse(BaseModel):
    """概念归属响应"""

    stock_code: str = Field(..., description="股票代码")
    source: str = Field("east", description="数据源: east/ths")
    data: List[ConceptItem] = Field(default_factory=list, description="概念列表")


class PlateItem(BaseModel):
    """板块项"""

    type: str = Field(..., description="板块类型: industry/region/concept")
    name: str = Field(..., description="名称")
    code: Optional[str] = Field(None, description="代码")


class PlateListResponse(BaseModel):
    """板块归属响应"""

    stock_code: str = Field(..., description="股票代码")
    data: List[PlateItem] = Field(default_factory=list, description="板块列表")


class CoreIndexResponse(BaseModel):
    """核心财务指标响应"""

    stock_code: str = Field(..., description="股票代码")
    report_date: Optional[str] = Field(None, description="报告期")
    eps: Optional[float] = Field(None, description="每股收益")
    bps: Optional[float] = Field(None, description="每股净资产")
    roe: Optional[float] = Field(None, description="净资产收益率(%)")
    gross_margin: Optional[float] = Field(None, description="毛利率(%)")
    net_margin: Optional[float] = Field(None, description="净利率(%)")
    debt_ratio: Optional[float] = Field(None, description="资产负债率(%)")
    revenue: Optional[float] = Field(None, description="营业总收入")
    net_profit: Optional[float] = Field(None, description="净利润")
    total_assets: Optional[float] = Field(None, description="总资产")
    total_equity: Optional[float] = Field(None, description="净资产")


class NorthFlowItem(BaseModel):
    """北向资金单条记录"""

    trade_date: Optional[str] = Field(None, description="交易日期")
    net_hgt: Optional[float] = Field(None, description="沪股通净流入")
    buy_hgt: Optional[float] = Field(None, description="沪股通买入")
    sell_hgt: Optional[float] = Field(None, description="沪股通卖出")
    net_sgt: Optional[float] = Field(None, description="深股通净流入")
    buy_sgt: Optional[float] = Field(None, description="深股通买入")
    sell_sgt: Optional[float] = Field(None, description="深股通卖出")
    net_tgt: Optional[float] = Field(None, description="北向资金合计净流入")


class NorthFlowResponse(BaseModel):
    """北向资金响应"""

    data: List[NorthFlowItem] = Field(default_factory=list, description="北向资金数据")
    count: int = Field(0, description="记录数")
