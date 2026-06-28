# Agent 层独立提取计划

> 目标：从当前项目中提取多 Agent 编排层，使其可独立运行，与自有数据源对接。

## 提取范围

| 组件 | 操作 | 说明 |
|------|------|------|
| `src/agent/` | **提取 + 7处改动** | 多 Agent 编排核心 |
| `src/notification.py` + `notification_sender/` | **直接复制** | 通知层 |
| `apps/dsa-web/` | **直接复制** | Web 前端 |
| `strategies/*.yaml` | **直接复制** | 11个交易策略 |
| `src/report_language.py` | **直接复制** | 语言工具 |
| `src/market_context.py` | **直接复制** | 市场角色/指南 |
| 传统 pipeline 分支、大盘复盘、回测、投资组合、桌面端 | **丢弃** | 不需要 |

## 目标项目结构

```
your-project/
├── agent/                    # ← 从 src/agent/ 提取
│   ├── orchestrator.py       # 不改
│   ├── runner.py             # 改：persist_usage 可选化
│   ├── protocols.py          # 不改
│   ├── llm_adapter.py        # 改：接受 LLMConfig 数据类
│   ├── executor.py           # 不改
│   ├── factory.py            # 不改
│   ├── memory.py             # 改：DB 可选化
│   ├── conversation.py       # 改：DB 可选化
│   ├── agents/               # 不改
│   ├── skills/               # 不改
│   ├── strategies/           # 不改
│   └── tools/
│       ├── registry.py       # 不改
│       ├── analysis_tools.py # 改：优先读 context
│       ├── data_tools.py     # ★ 替换 handler
│       ├── search_tools.py   # ★ 替换 handler
│       └── market_tools.py   # ★ 删除或替换
├── standalone.py             # ★ StandaloneAgentRunner 入口
├── config.py                 # ★ 精简 LLMConfig
├── report_language.py        # 复制
├── market_context.py         # 复制
├── notify/                   # ← 复制
├── web/                      # ← 复制
├── strategies/               # ← 11个 YAML
└── your_data/                # ← 你的数据层
```

## 7处改动

### 1. `llm_adapter.py` — 接受 `LLMConfig` 而非全局 `Config`

```python
@dataclass
class LLMConfig:
    model: str = ""
    api_key: str = ""
    api_base: str = ""
    temperature: float = 0.7
    fallback_models: list = field(default_factory=list)
    model_list: list = field(default_factory=list)
```

### 2. `runner.py` — `persist_usage` 改为可选注入

### 3. `memory.py` — `get_db()` 失败时降级为纯内存

### 4. `conversation.py` — `get_db()` 失败时降级为内存 dict

### 5. `analysis_tools.py` — handler 优先从 AgentContext 读预注入数据

### 6. `data_tools.py` — 替换所有 handler 为自有数据接口

### 7. `search_tools.py` — 替换所有 handler 为自有搜索接口

## 工具决策表

| 工具 | 决策 | 理由 |
|------|------|------|
| `calculate_ma`, `get_volume_analysis`, `analyze_pattern` | **保留** | 纯计算 |
| `analyze_trend` | **保留+适配** | 核心能力 |
| `get_realtime_quote`, `get_daily_history`, `get_stock_info` | **替换** | 接入你的数据 |
| `get_chip_distribution`, `get_capital_flow` | **替换或删除** | 可选 |
| `get_analysis_context`, `get_portfolio_snapshot` | **删除** | pipeline 专属 |
| `search_stock_news`, `search_comprehensive_intel` | **替换** | 接入你的搜索 |
| `get_market_indices`, `get_sector_rankings` | **替换或删除** | 非核心 |
| 全部 backtest_tools | **删除** | 非核心 |

## 最小配置

```bash
LITELLM_MODEL=anthropic/claude-sonnet-4-6
ANTHROPIC_API_KEY=sk-ant-...
AGENT_ARCH=multi
AGENT_ORCHESTRATOR_MODE=specialist
```
