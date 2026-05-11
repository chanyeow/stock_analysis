# AData 功能对比 — 当前项目缺失项

> 对比基准：`adata` v2.9.5（专注A股量化行情数据SDK）
> 对比对象：本仓库 `stock_analysis` 当前主分支
> 生成时间：2026-05-11

---

## 结论速览

本仓库在 **A股/港股/美股日线数据、实时行情、指数行情、市场统计、板块排行、筹码分布、基本面聚合** 等核心分析链路已具备完善能力。但相比 `adata`，在 **概念/板块生态、分时/五档/分笔级行情、ETF/债券专项接口、舆情与情绪数据（北向资金、人气榜、龙虎榜详情、融资融券、解禁、扫雷）** 等方面存在明显缺口。

---

## 详细对比表

| 模块 | adata API | 当前项目是否具备 | 备注 |
|------|-----------|----------------|------|
| **股票基本信息** | | | |
| | `all_code()` — 全部A股代码 | ⚠️ 部分有 | `TushareFetcher`/`BaostockFetcher` 有 `get_stock_list()`，但无统一 `all_code` 入口，也未做多源融合（百度→东财→新浪→本地缓存） |
| | `get_stock_shares()` — 股本变更 | ❌ 没有 | 无股本变更历史查询能力 |
| | `get_industry_sw()` — 申万行业 | ❌ 没有 | 无申万一级/二级行业查询 |
| | `trade_calendar()` — 交易日历 | ❌ 没有 | 无交易日历接口（仅有 `trading_calendar.py` 内部逻辑，未暴露为数据接口） |
| | `all_index_code()` — 全部指数代码 | ❌ 没有 | 无指数代码全量列表 |
| | `index_constituent()` — 指数成分股 | ❌ 没有 | 无指数成分股查询 |
| | `all_concept_code_ths/east()` — 全部概念代码 | ❌ 没有 | 无概念代码列表 |
| | `concept_constituent_ths/east()` — 概念成分股 | ❌ 没有 | 无概念成分股查询 |
| | `get_concept_ths/east/baidu()` — 股票所属概念 | ❌ 没有 | 无股票所属概念查询 |
| | `get_plate_east()` — 股票所属板块（行业/地域/概念） | ❌ 没有 | 无板块归属查询 |
| **股票行情** | | | |
| | `get_market()` — 日/周/月/分钟K线（复权） | ✅ 有 | `DataFetcherManager.get_daily_data()` 支持日线；分钟级K线未暴露 |
| | `get_market_min()` — 当日分时行情 | ❌ 没有 | 无分时数据接口 |
| | `list_market_current()` — 多股最新实时行情 | ⚠️ 部分有 | 有单股 `get_realtime_quote()` 和批量预取 `prefetch_realtime_quotes()`，但无明确的多股实时批量返回接口（如传入 `['000001','000002']` 返回 DataFrame） |
| | `get_market_five()` — 五档买卖盘 | ❌ 没有 | 无五档行情接口 |
| | `get_market_bar()` — 分笔成交 | ❌ 没有 | 无分笔/逐笔成交接口 |
| | `get_dividend()` — 分红信息 | ⚠️ 部分有 | `AkshareFundamentalAdapter` 在基本面聚合中包含了分红数据，但没有独立的 `get_dividend()` 入口 |
| | `get_market_index()` — 指数K线 | ❌ 没有 | 有 `get_main_indices()` 获取指数实时行情，但无指数历史K线 |
| | `get_market_index_min()` — 指数当日分时 | ❌ 没有 | 无指数分时数据 |
| | `get_market_index_current()` — 指数当前最新行情 | ⚠️ 部分有 | `get_main_indices()` 返回当前点位，但字段和粒度与 adata 的指数当前行情不完全对齐 |
| | `get_market_concept_ths/east()` — 概念K线 | ❌ 没有 | 无概念指数K线 |
| | `get_market_concept_min_ths/east()` — 概念当日分时 | ❌ 没有 | 无概念分时数据 |
| | `get_market_concept_current_ths/east()` — 概念当前行情 | ❌ 没有 | 无概念当前行情 |
| | `get_capital_flow_min()` — 当日分钟级资金流向 | ❌ 没有 | 无分钟级资金流向 |
| | `get_capital_flow()` — 日度资金流向历史 | ⚠️ 部分有 | `AkshareFundamentalAdapter.get_capital_flow()` 和 `DataFetcherManager.get_capital_flow_context()` 提供个股资金流向，但缺少近2年历史日度序列 |
| | `all_capital_flow_east()` — 全市场概念资金流向排行 | ❌ 没有 | 无全市场概念资金流向排行榜 |
| **财务数据** | | | |
| | `get_core_index()` — 核心财务指标（~30+字段） | ⚠️ 部分有 | `fundamental_adapter` 在基本面聚合中零散包含 ROE、毛利率、净利率等字段，但没有独立、完整的 `~30+` 字段核心财务指标接口 |
| **基金模块** | | | |
| | `all_etf_exchange_traded_info()` — 全部场内ETF列表 | ❌ 没有 | 无ETF全量列表接口 |
| | `get_market_etf()` — ETF日/周/月K线 | ✅ 有 | `AkshareFetcher`/`EfinanceFetcher` 支持 ETF 日线获取 |
| | `get_market_etf_min()` — ETF当日分时 | ❌ 没有 | 无ETF分时数据 |
| | `get_market_etf_current()` — ETF当前最新行情 | ✅ 有 | 有 ETF 实时行情获取 |
| **债券模块** | | | |
| | `all_convert_code()` — 全部可转债代码 | ❌ 没有 | 无可转债代码列表 |
| | `list_market_current()` — 可转债最新实时行情 | ❌ 没有 | 无可转债实时行情接口 |
| **舆情模块** | | | |
| | `north_flow()` — 北向资金历史日度 | ❌ 没有 | `market_analyzer.py` 中有注释掉的 `_get_north_flow()`，标注“已废弃，接口不可用”，当前无北向资金获取能力 |
| | `north_flow_min()` — 北向资金当日分时 | ❌ 没有 | 无北向资金分时 |
| | `north_flow_current()` — 北向资金最新数据 | ❌ 没有 | 无北向资金当前数据 |
| | `pop_rank_100_east()` — 东方财富人气榜Top100 | ❌ 没有 | 无人气榜 |
| | `hot_rank_100_ths()` — 同花顺热股Top100 | ❌ 没有 | 无热股榜 |
| | `hot_concept_20_ths()` — 同花顺热门概念/行业Top20 | ❌ 没有 | 无热门概念/行业榜 |
| | `list_a_list_daily()` — 每日龙虎榜列表 | ❌ 没有 | 有 `get_dragon_tiger_flag()` 判断单股是否上榜，但无每日龙虎榜全量列表 |
| | `get_a_list_info()` — 单股龙虎榜买卖5席详情 | ❌ 没有 | 无龙虎榜买卖席位详情 |
| | `securities_margin()` — 融资融券余额 | ❌ 没有 | 无融资融券数据 |
| | `stock_lifting_last_month()` — 最近一个月解禁列表 | ❌ 没有 | 无解禁数据接口（`risk_agent` 提示词中提到“解禁”，但无实际数据获取） |
| | `mine_clearance_tdx()` — 通达信扫雷信息 | ❌ 没有 | 无扫雷/避险数据 |

---

## 优先级建议

若计划补齐缺口，建议按以下优先级推进（结合本仓库“股票智能分析”定位）：

1. **高优先级（直接影响分析质量）**
   - `get_industry_sw()` — 申万行业（行业分析基础）
   - `get_concept_*()` / `get_plate_east()` — 概念/板块归属（热点关联分析）
   - `get_core_index()` — 核心财务指标（财务分析基础）
   - `north_flow()` — 北向资金（情绪面关键指标）

2. **中优先级（增强实时性与颗粒度）**
   - `get_market_min()` — 分时行情（盘中分析）
   - `get_market_five()` — 五档盘口（流动性分析）
   - `get_capital_flow_min()` / `all_capital_flow_east()` — 分钟级/全市场资金流向
   - `list_a_list_daily()` / `get_a_list_info()` — 龙虎榜列表与详情（异动追踪）

3. **低优先级（工具性/补充性）**
   - `trade_calendar()` — 交易日历（可用现有逻辑封装）
   - `all_code()` — 统一全市场代码入口（现有 `get_stock_list` 可整合）
   - `all_etf_exchange_traded_info()` / `all_convert_code()` — ETF/可转债列表
   - `hot_rank_*()` / `pop_rank_*()` — 人气/热股榜（情绪参考）
   - `securities_margin()` / `stock_lifting_last_month()` / `mine_clearance_tdx()` — 融资融券、解禁、扫雷
