# go-stock AI智能选股功能实现分析

## 一、系统架构概览

"AI智能选股"不是单一功能，而是一个多层系统，包含两个子系统：

- **子系统A：传统指标选股** — 调用东方财富i选股 / 同花顺i问财API，基于自然语言条件筛选股票
- **子系统B：AI驱动的股票分析与推荐** — 基于LLM + Tool-calling Agent，自主获取数据并给出结构化推荐

数据流如下：

```
用户查询 (自然语言)
    |
    v
前端 (SelectStock.vue / market.vue / agent-chat.vue / FloatingAiAssistant.vue)
    |
    v
Wails绑定 (app.go / app_common.go)
    |
    +---> 传统选股: SearchStock() -> 东方财富i选股API -> 结果表格
    +---> AI总结选股: SummaryStockNews() -> OpenAI兼容LLM
    |       |-- 组装: System Prompt + 宏观数据 + 新闻 + 日历事件
    |       |-- LLM调用工具: CreateAiRecommendStocks -> 保存到数据库
    +---> 个股分析: NewChatStream() -> OpenAI兼容LLM
    |       |-- 组装: System Prompt + K线 + 股价 + 财报 + 新闻
    |       |-- LLM按需调用工具
    +---> Agent对话: ChatWithAgent() -> Agent (React 或 PlanExecute模式)
            |-- 根据问题关键词动态选择工具组
            |-- 70+可用工具 (股票数据、筛选、新闻、宏观等)
            |-- MCP服务器工具动态加载
            |-- 技能系统注入领域特定提示词
            |
            v
        LLM响应 -> EventsEmit到前端 -> Markdown渲染
```

---

## 二、投喂给Agent的数据（信息输入）

根据 `backend/data/openai_stream.go` 的 `NewChatStream` 方法（第296-602行），系统会**并发**获取以下数据注入到对话上下文中：

| 数据类型 | 来源方法 | 说明 |
|---|---|---|
| **系统提示词** | `Settings.Prompt` / `PromptTemplateApi` | 可配置，默认为"20年投资大师"角色设定 |
| **当前时间** | 运行时注入 | 作为assistant消息注入 |
| **提问模板** | `Settings.QuestionTemplate` | 支持 `{{stockName}}`、`{{stockCode}}`、`{{costPrice}}` 等占位符 |
| **投资者互动问答** | `NewMarketNewsApi().InteractiveAnswer()` | 公司-投资者互动数据 |
| **宏观经济数据** | `NewMarketNewsApi()` | GDP、CPI、PPI、PMI，通过goroutine并发获取 |
| **财经日历事件** | `NewMarketNewsApi().ClsCalendar()` | 近期重大事件/会议 |
| **K线数据** | `NewStockDataApi().GetKLineData()` | 默认60天的日K线OHLCV数据（天数可通过KDays配置） |
| **实时股价** | `SearchStockPriceInfo()` | 爬取实时价格信息 |
| **财务报表** | `GetFinancialReportsByXUEQIU()` | 通过chromedp无头浏览器抓取雪球财务表 |
| **市场新闻(24h)** | `GetNews24HoursList()` | 80-200条近期市场新闻 |
| **个股资讯** | `SearchStockInfo()` | 个股相关的电报/快讯新闻 |
| **热门选股策略** | `HotStrategy()` | 当前热门策略（仅在SummaryStockNews路径中） |

**AI总结选股路径**（`SummaryStockNews`）则聚焦于：
- 宏观数据（GDP、CPI、PPI、PMI）
- 财经日历事件
- 默认提问：`"请根据当前时间，总结和分析股票市场新闻中的投资机会"`
- 当启用工具时，追加指令：`"最后必须调用CreateAiRecommendStocks工具函数保存ai股票推荐记录。"`

---

## 三、System Prompt（角色设定）

### 默认系统提示词

定义在 `backend/agent/agent_api.go:133`：

```
你现在扮演一位拥有20年实战经验的顶级股票投资大师，精通价值投资、趋势交易、量化分析等多种策略。
你擅长结合宏观经济、行业周期和企业基本面进行全方位、精准的多维分析，
尤其对A股、港股、美股市场有深刻理解，
始终秉持"风险控制第一"的原则，善于用通俗易懂的方式传授投资智慧。
```

### PlanExecute模式的分阶段提示词

定义在 `backend/agent/agent.go`：

- **Planner**（第491行）：`"你是股票分析规划师。将用户目标拆解为3-4步执行计划。"`
- **Executor**（第958行）：`"按计划执行当前步骤，调用工具获取数据，给出简洁精准的分析结果。"`
- **Replanner**（第982行）：`"审核执行进度并决定下一步。"` — 必须调用`plan`工具（剩余步骤）或`respond`工具（全部完成）

### AI选股路径追加指令

```
最后必须调用CreateAiRecommendStocks工具函数保存ai股票推荐记录。
```

强制LLM输出结构化推荐结果到数据库。

---

## 四、工具集（Tool Definitions）

项目定义了70+工具函数，位于 `backend/data/tools.go`（2564行）。LLM可自主决定调用哪些工具。

### 4.1 筛选类工具

| 工具名 | 功能说明 |
|---|---|
| `SearchStockByIndicators` | 自然语言选股，调用东方财富i选股API（如"MACD金叉;PE<30;净利润增长率>50%"） |
| `SelectAStock` | 调用同花顺i问财API，支持指标、财务、行业概念筛选 |
| `SelectSector` | 行业/概念板块筛选（i问财） |
| `FilterStocks` | 技术指标筛选：MACD金叉、KDJ金叉、均线多头排列、量价配合、连续涨跌天数 |
| `HotStrategyTable` | 获取当前热门选股策略 |

### 4.2 行情与K线工具

| 工具名 | 功能说明 |
|---|---|
| `GetStockKLine` | 获取股票K线数据 |
| `GetEastMoneyKLine` | 东方财富K线数据 |
| `GetEastMoneyKLineWithMA` | 带均线的K线数据 |

### 4.3 财务与估值工具

| 工具名 | 功能说明 |
|---|---|
| `GetStockFinancialInfo` | 股票财务信息 |
| `GetStockLatestFinance` | 最新财务数据 |
| `GetStockQtrMainFinance` | 季度主要财务指标 |
| `GetStockValuationPercentile` | 估值百分位（PE历史分位数） |
| `GetIndustryValuation` | 行业平均估值（PE、PEG） |

### 4.4 资金流向工具

| 工具名 | 功能说明 |
|---|---|
| `GetStockHistoryMoneyData` | 历史资金流向数据 |
| `GetStockMoneyData` | 实时资金流向 |
| `GetIndustryMoneyRank` | 行业资金流向排名 |
| `GetMutualTop10Deal` | 北向/南向资金前十交易 |
| `GetStockRZRQInfo` | 融资融券信息 |
| `GetStockMarginTrading` | 保证金交易数据 |

### 4.5 机构与研报工具

| 工具名 | 功能说明 |
|---|---|
| `GetStockOrgPredict` | 机构预测 |
| `GetStockPredictSummary` | 预测汇总 |
| `GetSecuritiesCompanyOpinion` | 券商/机构观点 |
| `GetStockResearchReport` | 分析师研报 |

### 4.6 市场热点工具

| 工具名 | 功能说明 |
|---|---|
| `GetStockBillboard` | 龙虎榜数据 |
| `GetLongTigerList` | 龙虎榜详细 |
| `GetUplimitLadder` | 涨停阶梯 |
| `GetUplimitHotPlates` | 涨停热门板块 |
| `GetUplimitHotStocks` | 涨停热门个股 |
| `GetStockConceptInfo` | 股票概念/板块归属 |

### 4.7 股东数据工具

| 工具名 | 功能说明 |
|---|---|
| `GetStockHolderNum` | 股东人数 |
| `GetStockHolderTrend` | 股东人数变动趋势 |

### 4.8 AI输出工具

| 工具名 | 功能说明 |
|---|---|
| `CreateAiRecommendStocks` | 保存单条AI推荐记录到数据库 |
| `BatchCreateAiRecommendStocks` | 批量保存AI推荐记录 |
| `AiRecommendStocks` | 查询历史AI推荐记录 |
| `SetTradingPrice` | 设置买入/止盈/止损价格 |

### 4.9 i问财系列工具

| 工具名 | 功能说明 |
|---|---|
| `QueryIwencai` | 通用i问财查询 |
| `SelectAStock` | A股智能筛选 |
| `SelectSector` | 板块筛选 |
| `QueryMacro` | 宏观数据查询 |
| `QueryZhishu` | 指数数据查询 |
| `QueryEvent` | 事件查询 |
| `SearchNews` | 新闻搜索 |
| `SearchInvestor` | 投资者搜索 |
| `SearchReport` | 研报搜索 |
| `QueryInsResearch` | 机构调研查询 |

### 4.10 工具分组与动态筛选

定义在 `backend/agent/tools/tool_groups.go`，工具被分为以下组：

| 组名 | 说明 |
|---|---|
| `base` | 基础工具 |
| `stock_analysis` | 个股分析 |
| `market` | 市场行情 |
| `screening` | 选股筛选 |
| `money_flow` | 资金流向 |
| `news_research` | 新闻研报 |
| `ai_analysis` | AI分析 |
| `operations` | 操作类 |

`ClassifyQuestion()` 函数根据用户问题中的关键词匹配，动态决定激活哪些工具组，减少不必要的工具暴露。

---

## 五、Agent模式

定义在 `backend/agent/agent.go:31`：

```go
const (
    AgentModeReact       AgentMode = "react"
    AgentModePlanExecute AgentMode = "plan_execute"
)
```

### 5.1 模式自动选择逻辑

`classifyComplexity` 函数（第42行）根据问题特征自动选择：

| 条件 | 选择模式 |
|---|---|
| 包含"今天"、"当前"、"查询"、"多少"，且<30字符 | React（快速） |
| 包含"全面分析"、"综合分析"、"投资建议"、"对比分析"、"行业分析"、"投资组合"、"风险评估" | PlanExecute（规划） |
| 匹配4+个工具组 | PlanExecute |
| 问题超过80字符 | PlanExecute |

### 5.2 React模式

使用 `github.com/cloudwego/eino/flow/agent/react`，标准的Reason+Act循环。最大步数 = 工具数量 + 15。

### 5.3 PlanExecute模式

使用 `github.com/cloudwego/eino/adk/prebuilt/planexecute`，三阶段执行：

1. **Planner** — 将用户目标拆解为3-4步执行计划
2. **Executor** — 按计划逐步执行，调用工具获取数据
3. **Replanner** — 审核执行进度，决定下一步（继续计划或给出最终响应）

### 5.4 降级机制

如果PlanExecute执行失败（如编码问题），自动降级到React模式（第316行）。

### 5.5 前端选择器

`frontend/src/components/agent-chat.vue:118`：

```javascript
const agentModeOptions = [
  { label: '自动', value: 'auto' },
  { label: '快速(React)', value: 'react' },
  { label: '规划(PlanExecute)', value: 'plan_execute' },
]
```

---

## 六、AI推荐数据模型

定义在 `backend/models/models.go:1022-1129`。

`AiRecommendStocks` 模型存储每条AI推荐记录：

| 字段 | 说明 |
|---|---|
| `ModelName` | 生成推荐的LLM模型名称 |
| `Rating` | 评级：买入/增持/中性/减持/卖出 |
| `StockCode` | 股票代码 |
| `StockName` | 股票名称 |
| `BkCode` / `BkName` | 板块代码/名称 |
| `StockPrice` | 推荐时股价 |
| `StockClosePrice` | 收盘价 |
| `StockPrePrice` | 前收盘价 |
| `RecommendReason` | AI给出的推荐理由/驱动因素 |
| `RecommendBuyPrice` | 建议买入价 |
| `RecommendBuyPriceMin` / `Max` | 建议买入价区间 |
| `RecommendStopProfitPrice` | 止盈价 |
| `RecommendStopProfitPriceMin` / `Max` | 止盈价区间 |
| `RecommendStopLossPrice` | 止损价 |
| `RiskRemarks` | 风险提示 |
| `EnableAlert` | 是否启用价格监控报警 |

### 价格监控

`app.go:1199` 的 `MonitorAiRecommendStockPrices()` 作为定时任务运行，检查 `enable_alert=true` 的推荐股票是否触及买入/止盈/止损价格，触发通知提醒。

---

## 七、MCP工具支持

定义在 `backend/agent/agent.go:386-457`。

`getMCPTools()` 函数连接用户配置的MCP服务器（存储在数据库 `models.MCPServer` 中），使用：
- `github.com/mark3labs/mcp-go/client` — Streamable HTTP传输
- `github.com/cloudwego/eino-ext/components/tool/mcp` — 工具集成

前端管理界面：`frontend/src/components/mcp-server-manager.vue`

### 技能系统（Skill System）

定义在 `backend/data/skill_api.go`。

技能可配置：触发关键词、系统提示词、示例、关联的MCP服务器ID。`agent.go:281` 的 `buildSkillPrompt()` 函数根据用户问题匹配技能，注入对应的领域特定提示词。

---

## 八、情感分析

定义在 `backend/data/stock_sentiment_analysis.go`。

基于规则的情感分析器，使用中文金融词库：
- **正面词**：涨、涨停、牛市、利好 等
- **负面词**：跌、跌停、熊市、利空 等

采用基于词频的加权评分机制，用于分析新闻内容的情感倾向。

---

## 九、关键文件路径索引

| 组件 | 文件路径 |
|---|---|
| 主应用绑定 | `app.go` |
| Agent对话绑定 | `app_common.go` (第172行) |
| Agent核心（React/PlanExecute） | `backend/agent/agent.go` |
| Agent API（对话编排） | `backend/agent/agent_api.go` |
| AI流式处理 + 数据组装 | `backend/data/openai_stream.go` |
| OpenAI配置 | `backend/data/openai_api.go` |
| 工具定义（70+工具） | `backend/data/tools.go` |
| 工具分组/筛选 | `backend/agent/tools/tool_groups.go` |
| 数据工具包装器 | `backend/agent/tools/data_tools_wrapper.go` |
| 选股工具 | `backend/agent/tools/choice_stock_by_indicators_tool.go` |
| i问财API | `backend/data/iwencai_api.go` |
| 东方财富选股 | `backend/data/search_stock_api.go` |
| AI推荐CRUD | `backend/data/ai_recommend_stocks_api.go` |
| AI推荐数据模型 | `backend/models/models.go` (第1022行) |
| 情感分析 | `backend/data/stock_sentiment_analysis.go` |
| MCP服务器API | `backend/data/mcp_server_api.go` |
| 技能系统 | `backend/data/skill_api.go` |
| 提示词模板 | `backend/data/prompt_template_api.go` |
| 设置/配置 | `backend/data/settings_api.go` |
| 前端：选股页面 | `frontend/src/components/SelectStock.vue` |
| 前端：AI推荐列表 | `frontend/src/components/aiRecommendStocksList.vue` |
| 前端：Agent对话 | `frontend/src/components/agent-chat.vue` |
| 前端：浮动AI助手 | `frontend/src/components/FloatingAiAssistant.vue` |
| 前端：市场行情(AI总结) | `frontend/src/components/market.vue` |
| 前端：MCP服务器管理 | `frontend/src/components/mcp-server-manager.vue` |
| 定时任务系统 | `backend/agent/cron_task_api.go` |
| 对话记忆 | `backend/agent/chat_memory.go` |
| 网页爬虫(财报) | `backend/data/openai_crawler.go` |

---

## 十、总结：选股策略的本质

这个项目的选股策略**不是硬编码的量化规则**，而是：

1. **角色扮演**：让LLM扮演拥有20年经验的投资大师
2. **工具赋能**：提供70+金融数据查询工具，覆盖K线、财务、资金流、研报、龙虎榜、宏观等维度
3. **数据投喂**：并发获取多维数据注入上下文（K线、财报、新闻、宏观、日历等）
4. **自主推理**：LLM自主决定调用哪些工具、分析哪些维度
5. **结构化输出**：通过`CreateAiRecommendStocks`工具强制要求LLM给出评级、买入价、止盈止损价、理由
6. **双模式运行**：简单问题用React快速响应，复杂分析用PlanExecute分步规划执行

本质上是一个 **ReAct/PlanExecute Agent + 金融MCP工具集** 的架构。策略的"智能"来自LLM的推理能力 + 丰富的工具集，而非预设的量化策略规则。
