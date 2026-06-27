# -*- coding: utf-8 -*-
"""
===================================
知识库相关模型
===================================

职责：
1. 定义知识库条目模型
2. 定义知识库响应模型
3. 定义爬取进度模型
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class KnowledgeItem(BaseModel):
    """知识库条目"""

    code: str = Field(..., description="代码，如 BK1036 / 600519")
    name: str = Field(..., description="名称，如 半导体 / 贵州茅台")
    category: str = Field(..., description="类别: bk(板块) / sh(沪市) / sz(深市)")
    change_pct: Optional[float] = Field(None, description="涨跌幅（仅板块有）")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "BK1036",
                "name": "半导体",
                "category": "bk",
                "change_pct": 0.66,
            }
        }


class KnowledgeListResponse(BaseModel):
    """知识库列表响应"""

    total: int = Field(..., description="总条数")
    data: List[KnowledgeItem] = Field(default_factory=list, description="知识库条目列表")

    class Config:
        json_schema_extra = {
            "example": {
                "total": 128,
                "data": [
                    {"code": "BK1036", "name": "半导体", "category": "bk", "change_pct": 0.66},
                    {"code": "BK0727", "name": "医疗服务", "category": "bk", "change_pct": -0.32},
                ],
            }
        }


class KnowledgeMarkdownResponse(BaseModel):
    """知识库 Markdown 内容响应"""

    code: str = Field(..., description="代码")
    name: str = Field(..., description="名称")
    category: str = Field(..., description="类别")
    content: str = Field(..., description="Markdown 内容")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "BK1036",
                "name": "半导体",
                "category": "bk",
                "content": "# 半导体 (BK1036)\n\n## 基本信息\n...",
            }
        }


class CrawlProgressResponse(BaseModel):
    """爬取进度响应"""

    total: int = Field(0, description="总数")
    current: int = Field(0, description="当前进度")
    status: str = Field("idle", description="状态: idle / crawling / done / error")
    message: str = Field("", description="状态消息")
    errors: List[str] = Field(default_factory=list, description="错误列表")

    class Config:
        json_schema_extra = {
            "example": {
                "total": 528,
                "current": 128,
                "status": "crawling",
                "message": "正在处理行业板块: 半导体 (128/528)",
                "errors": [],
            }
        }


class SearchResponse(BaseModel):
    """搜索响应"""

    keyword: str = Field(..., description="搜索关键词")
    total: int = Field(..., description="匹配条数")
    data: List[KnowledgeItem] = Field(default_factory=list, description="匹配的知识库条目列表")
