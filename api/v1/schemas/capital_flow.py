# -*- coding: utf-8 -*-
"""
===================================
板块资金流相关模型
===================================

职责：
1. 定义板块资金流条目模型
2. 定义板块资金流响应模型
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class CapitalFlowItem(BaseModel):
    """板块资金流条目（图表用）"""

    code: str = Field(..., description="板块代码，如 BK1036")
    name: str = Field(..., description="板块名称，如 半导体")
    flow: float = Field(..., description="资金净流入（元），正值表示净流入，负值表示净流出")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "BK1036",
                "name": "半导体",
                "flow": 5243314176.0,
            }
        }


class CapitalFlowResponse(BaseModel):
    """板块资金流响应（图表用）"""

    category: str = Field(..., description="类别: industry(行业) / concept(概念)")
    period: str = Field(..., description="周期: today(今日) / 5day(5日) / 10day(10日)")
    total: int = Field(..., description="板块总数")
    data: List[CapitalFlowItem] = Field(default_factory=list, description="资金流数据列表，按净流入降序排列")

    class Config:
        json_schema_extra = {
            "example": {
                "category": "industry",
                "period": "today",
                "total": 128,
                "data": [
                    {"code": "BK1036", "name": "半导体", "flow": 5243314176.0},
                    {"code": "BK0727", "name": "医疗服务", "flow": 3210997232.0},
                ],
            }
        }


class CapitalFlowTableItem(BaseModel):
    """板块资金流表格条目（含更多字段）"""

    code: str = Field(..., description="板块代码")
    name: str = Field(..., description="板块名称")
    flow: float = Field(..., description="资金净流入（元）")
    price: Optional[float] = Field(None, description="板块指数")
    change_pct: Optional[float] = Field(None, description="涨跌幅")
    company_count: Optional[int] = Field(None, description="公司家数")
    lead_stock_name: str = Field("", description="领涨股名称")
    lead_stock_code: str = Field("", description="领涨股代码")
    main_flow: Optional[float] = Field(None, description="主力净流入（=超大单+大单）")
    main_ratio: Optional[float] = Field(None, description="主力净流入占比")
    super_large_flow: Optional[float] = Field(None, description="超大单净流入")
    large_flow: Optional[float] = Field(None, description="大单净流入")
    medium_flow: Optional[float] = Field(None, description="中单净流入")
    small_flow: Optional[float] = Field(None, description="小单净流入")
    super_large_ratio: Optional[float] = Field(None, description="超大单占比")
    large_ratio: Optional[float] = Field(None, description="大单占比")
    medium_ratio: Optional[float] = Field(None, description="中单占比")
    small_ratio: Optional[float] = Field(None, description="小单占比")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "BK1036",
                "name": "半导体",
                "flow": 5243314176.0,
                "price": 3485.92,
                "change_pct": 0.66,
                "company_count": 209,
                "lead_stock_name": "海光信息",
                "lead_stock_code": "688041",
                "main_flow": 1234567890.0,
                "super_large_flow": 987654321.0,
                "large_flow": 246801357.0,
                "medium_flow": -111111111.0,
                "small_flow": -222222222.0,
                "super_large_ratio": 0.03,
                "large_ratio": 0.05,
                "medium_ratio": -0.02,
                "small_ratio": -0.06,
            }
        }


class CapitalFlowTableResponse(BaseModel):
    """板块资金流表格响应（分页）"""

    category: str = Field(..., description="类别")
    period: str = Field(..., description="周期")
    total: int = Field(..., description="总条数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页条数")
    total_pages: int = Field(..., description="总页数")
    data: List[CapitalFlowTableItem] = Field(default_factory=list, description="当前页数据")
