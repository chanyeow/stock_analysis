# 项目精简方案

> 基于当前使用模式（Linux 部署 + `start_server_only.sh` + 仅 A 股 + 多 Agent 编排核心）制定。

---

## 一、当前使用画像

| 维度 | 实际情况 |
|------|---------|
| 部署方式 | Linux + `start_server_only.sh` → `python main.py --webui-only` |
| 核心功能 | 多 Agent 编排（`src/agent/`） |
| 需要的市场 | **仅 A 股** |
| 不需要的市场 | 美股（可删）、港股（代码侵入浅，建议保留） |
| 不需要的形态 | 桌面端、Bot 机器人、定时调度、投资组合跟踪 |

---

## 二、可删除模块清单

### 🔴 高优先级：明确可删（纯美股 + 废弃代码）

#### 2.1 美股数据源

| 文件 | 大小 | 原因 |
|------|------|------|
| `data_provider/us_index_mapping.py` | ~3KB | 纯美股指数映射（SPX→^GSPC 等）和 `is_us_stock_code()` |
| `data_provider/yfinance_fetcher.py` | ~30KB | Yahoo Finance，美股主力数据源。虽也支持 A 股/港股，但数据延迟大，国内源完全覆盖 |
| `data_provider/longbridge_fetcher.py` | ~20KB | 长桥 OpenAPI，**仅覆盖港股+美股**，不提供 A 股数据 |

#### 2.2 美股专用服务

| 文件 | 大小 | 原因 |
|------|------|------|
| `src/services/social_sentiment_service.py` | ~15KB | 从 Reddit/X/Polymarket 获取美股情绪数据，仅对美股代码生效 |

#### 2.3 已废弃脚本

| 路径 | 原因 |
|------|------|
| `scripts/deprecated/build-all-macos.sh` | 已标记废弃 |
| `scripts/deprecated/build-all.ps1` | 已标记废弃 |
| `scripts/deprecated/build-backend-macos.sh` | 已标记废弃 |
| `scripts/deprecated/build-backend.ps1` | 已标记废弃 |
| `scripts/deprecated/build-desktop-macos.sh` | 已标记废弃 |
| `scripts/deprecated/build-desktop.ps1` | 已标记废弃 |
| `scripts/deprecated/run-desktop.ps1` | 已标记废弃 |

#### 2.4 Discord Bot（已是死代码）

| 文件 | 原因 |
|------|------|
| `bot/platforms/discord.py` | 未在 `bot/platforms/__init__.py` 中注册，实际不可用 |

---

### 🟡 中优先级：你可能用不上（需确认）

#### 2.5 桌面端

| 路径 | 大小 | 原因 |
|------|------|------|
| `apps/dsa-desktop/` | 整个目录 | Electron 桌面端，你只用 Linux 服务器模式 + WebUI |

#### 2.6 Bot 系统

| 路径 | 原因 |
|------|------|
| `bot/` 整个目录 | 钉钉/飞书/Telegram 机器人，通过 IM 触发分析 |
| `docs/bot-command.md` | Bot 命令文档（中文） |
| `docs/bot-command_EN.md` | Bot 命令文档（英文） |
| `docs/bot/dingding-bot-config.md` | 钉钉 Bot 配置指南 |
| `docs/bot/feishu-bot-config.md` | 飞书 Bot 配置指南 |
| `docs/bot/discord-bot-config.md` | Discord Bot 配置指南 |

#### 2.7 投资组合系统

| 文件 | 原因 |
|------|------|
| `src/services/portfolio_service.py` | 持仓管理、交易记录、股息、盈亏计算 |
| `src/services/portfolio_risk_service.py` | 组合风险分析（集中度、回撤、止损距离） |
| `src/services/portfolio_import_service.py` | CSV 导入券商交易记录 |
| `src/repositories/portfolio_repo.py` | 组合数据库操作 |
| `api/api/v1/endpoints/portfolio.py` | 组合相关 API 端点 |

#### 2.8 回测系统

| 文件 | 原因 |
|------|------|
| `src/core/backtest_engine.py` | 回测引擎（纯逻辑，DB 无关） |
| `src/services/backtest_service.py` | 回测编排服务 |
| `src/repositories/backtest_repo.py` | 回测数据库操作 |
| `src/agent/tools/backtest_tools.py` | Agent 可调用的回测工具 |
| `api/api/v1/endpoints/backtest.py` | 回测 API 端点 |

---

### 🟢 低优先级：可精简但需谨慎

#### 2.9 A 股数据源冗余（5 个 → 保留 2-3 个）

| 数据源 | 文件 | 优先级 | 建议 |
|--------|------|--------|------|
| 东方财富 | `data_provider/efinance_fetcher.py` | 0 | **保留** - 主力数据源，数据全、免费 |
| AkShare | `data_provider/akshare_fetcher.py` | 1 | **保留** - 覆盖面广，免费，备选 |
| Tushare | `data_provider/tushare_fetcher.py` | -1 | 可选 - 需要 token，有积分门槛 |
| 通达信 | `data_provider/pytdx_fetcher.py` | 2 | **可删** - TCP 协议直连，维护成本高 |
| 证券宝 | `data_provider/baostock_fetcher.py` | 3 | **可删** - 更新慢，覆盖面窄 |

#### 2.10 搜索服务 Provider 精简

`src/search_service.py`（~130KB）集成了 7 个搜索提供商：

| Provider | 建议 |
|----------|------|
| Tavily | **保留** - AI 原生搜索，效果好 |
| Bocha | 可选 - 中文搜索 |
| 其余 5 个（Anspire, Brave, SerpAPI, MiniMax, SearXNG） | 按需保留 0-1 个 |

---

## 三、Docs 目录精简

### 当前状态：33+ 个文件

### ✅ 保留（核心文档 8 个）

| 文件 | 理由 |
|------|------|
| `docs/CHANGELOG.md` | 变更记录 |
| `docs/full-guide.md`（或 EN 版） | 完整配置指南 |
| `docs/DEPLOY.md`（或 EN 版） | 部署指南 |
| `docs/LLM_CONFIG_GUIDE.md`（或 EN 版） | LLM 配置指南 |
| `docs/llm-providers.md` | LLM provider 详细参考 |
| `docs/notifications.md` | 通知渠道配置 |
| `docs/分析调用堆栈.md` | 架构调用链，关键开发文档 |
| `docs/architecture/api_spec.json` | API 规范 |

### ❌ 可删除（与你无关的功能文档 14 个）

| 文件 | 原因 |
|------|------|
| `docs/bot-command.md` | 不用 Bot |
| `docs/bot-command_EN.md` | 同上 |
| `docs/bot/dingding-bot-config.md` | 不用钉钉 Bot |
| `docs/bot/feishu-bot-config.md` | 不用飞书 Bot |
| `docs/bot/discord-bot-config.md` | 不用 Discord Bot |
| `docs/desktop-package.md` | 不用桌面端 |
| `docs/deploy-webui-cloud.md` | 你是本地 Linux 部署 |
| `docs/docker/zeabur-deployment.md` | 不用 Zeabur 云平台 |
| `docs/openclaw-skill-integration.md` | openclaw 外部集成，与你无关 |
| `docs/TUSHARE_STOCK_LIST_GUIDE.md` | 如果删了 Tushare 数据源 |
| `docs/AI智能选股功能分析.md` | 内部分析文档，非用户文档 |
| `docs/image-extract-prompt.md` | 图片提取 prompt 记录，开发笔记 |
| `docs/settings-help.md` | WebUI 设置帮助基础设施 |

### ⚠️ 建议去重/合并

当前大量文档维护了中英双语版本，如果你只用中文：

| 可删除（英文版） | 保留（中文版） |
|------|------|
| `docs/README_EN.md` | 根目录 `README.md` |
| `docs/FAQ_EN.md` | `docs/FAQ.md` |
| `docs/CONTRIBUTING_EN.md` | `docs/CONTRIBUTING.md` |
| `docs/INDEX_EN.md` | `docs/INDEX.md` |
| `docs/LLM_CONFIG_GUIDE_EN.md` | `docs/LLM_CONFIG_GUIDE.md` |
| `docs/full-guide_EN.md` | `docs/full-guide.md` |
| `docs/DEPLOY_EN.md` | `docs/DEPLOY.md` |

以及繁体中文版：

| 可删除 | 原因 |
|------|------|
| `docs/README_CHT.md` | 你只用简体中文 |

### 可删除的品牌/截图资源

| 路径 | 原因 |
|------|------|
| `docs/assets/dsa_vi/` | 品牌 VI 源文件（PSD/AI/ico），运行时不需要 |
| `docs/assets/alipay.jpg`、`wechatpay.jpg`、`ko-fi.png` | 赞助收款码图片 |
| `docs/assets/serpapi_banner_en.png`、`serpapi_banner_zh.png` | 第三方服务 banner |
| `docs/bot/*.png`（~11 个截图） | Bot 配置截图 |

---

## 四、需要联动修改的代码

删除上述模块后，需要在以下文件中移除对应的 import 和引用：

### 4.1 数据源注册

| 文件 | 修改内容 |
|------|---------|
| `data_provider/__init__.py` | 移除 yfinance、longbridge、us_index_mapping 的 import 和注册 |
| `data_provider/base.py` | 移除 fallback 链中的 yfinance 和 longbridge |
| `src/config.py` | 移除 `YFINANCE_PRIORITY`、`LONGBRIDGE_*` 等美股/长桥相关配置项 |
| `.env.example` | 移除美股/长桥相关环境变量 |

### 4.2 市场上下文精简

| 文件 | 修改内容 |
|------|---------|
| `src/market_context.py` | 移除 `"us"` 和 `"hk"` 分支，仅保留 `"cn"` |
| `src/core/market_profile.py` | 移除 `"us"` 和 `"hk"` 的 market profile |
| `src/core/market_strategy.py` | 移除美股/港股的策略蓝图 |
| `src/core/trading_calendar.py` | 移除 `"us"` 和 `"hk"` 的交易日历配置 |
| `src/core/market_review.py` | 移除多市场遍历，固定为 `"cn"` |
| `src/config.py` | `MARKET_REVIEW_REGION` 固定为 `"cn"` |

### 4.3 服务层

| 文件 | 修改内容 |
|------|---------|
| `src/services/__init__.py` | 移除 SocialSentimentService 导出 |
| `src/services/stock_code_utils.py` | 移除 `is_us_stock_code()` 相关逻辑 |
| `api/api/v1/router.py` | 移除 portfolio、backtest 路由注册（如删除对应功能） |
| `main.py` | 移除 `--backtest` 相关 CLI 参数（如删除回测） |

---

## 五、保留清单（核心功能）

### 5.1 必须保留的目录/文件

```
src/agent/                  # ★ 多Agent编排核心
src/agent/agents/           # TechnicalAgent, IntelAgent, RiskAgent, DecisionAgent
src/agent/tools/            # 工具注册 + data/analysis/search/market tools
src/agent/skills/           # 技能系统（SkillAgent, SkillRouter, SkillAggregator）
src/agent/strategies/       # 旧命名兼容层（可后续统一）
strategies/                 # 11个 YAML 交易策略定义
src/stock_analyzer.py       # StockTrendAnalyzer（TechnicalAgent 依赖）
src/search_service.py       # SearchService（IntelAgent 依赖）
src/config.py               # 配置中心
src/storage.py              # 数据库层
src/notification.py         # 通知服务
src/notification_sender/    # 通知渠道实现（13个）
src/report_language.py      # 报告国际化
src/market_context.py       # 市场上下文（精简为仅 A 股）
src/formatters.py           # Markdown 格式化
src/logging_config.py       # 日志配置
src/enums.py                # 枚举
src/md2img.py               # Markdown 转图片
src/scheduler.py            # 定时调度（如果 start_server_only 不需要可删）
src/webui_frontend.py       # WebUI 前端入口
src/auth.py                 # 数据源认证
data_provider/              # 精简后的 A 股数据源（保留 efinance + akshare + tickflow）
api/                        # FastAPI 服务
apps/dsa-web/               # Web 前端
main.py                     # 入口
server.py                   # FastAPI 入口
start_server_only.sh        # 启动脚本
```

### 5.2 不确定是否需要的（请确认）

| 模块 | 文件 | 问题 |
|------|------|------|
| 飞书文档 | `src/feishu_doc.py` | 你是否用飞书文档发布报告？ |
| 大盘复盘 | `src/core/market_review.py`、`src/market_analyzer.py`、`src/core/market_profile.py`、`src/core/market_strategy.py` | 你是否需要每日大盘复盘功能？ |
| 定时调度 | `src/scheduler.py` | `start_server_only.sh` 模式下是否用到？ |
| Gemini 分析器 | `src/analyzer.py`（133KB，最大单文件） | 传统（非 Agent）分析路径，Agent 模式下是否还在用？ |
| 流水线 | `src/core/pipeline.py` | 传统分析流水线，Agent 模式下是否还在用？ |
| 资金流向 | `api/api/v1/endpoints/capital_flow.py`、`scripts/capitalflow/` | 是否需要东方财富板块资金流向？ |
| 知识库 | `api/api/v1/endpoints/knowledge.py`、`scripts/knowledge/` | 是否需要 A 股基本面/资金流知识库爬虫？ |
| 通知渠道 | `src/notification_sender/` 下有 13 个 sender | 实际用哪几个？不需要的可删 |
| 图片提取 | `src/services/image_stock_extractor.py` | 是否需要从截图提取股票代码？ |

---

## 六、建议执行顺序

| 轮次 | 内容 | 风险 | 预计删除文件数 |
|------|------|------|--------------|
| **第一轮** | 美股数据源 + 美股服务 + 废弃脚本 + Discord | 低 | ~12 |
| **第二轮** | 桌面端 + Bot 系统 + 投资组合 + 回测 | 中（需确认） | ~30+ |
| **第三轮** | 冗余 A 股数据源 + 搜索 Provider 精简 | 中（需测试） | ~5 |
| **第四轮** | Docs 精简 + 去重 | 低 | ~25 |
| **第五轮** | 代码联动清理（市场分支、import、配置项） | 中 | ~10 文件修改 |
| **第六轮** | 不确定项的最终确认和清理 | 低 | 按需 |

---

## 七、风险点

1. **yfinance 删除**：虽然主要服务于美股，但它也是 A 股的 P4 兜底数据源。删除后 A 股在国内源全部故障时无降级路径。**建议**：先确认 efinance + akshare 稳定性足够。
2. **港股连带影响**：`akshare_fetcher` 和 `tushare_fetcher` 同时支持 A 股和港股，港股逻辑嵌入在同一文件中。如果只删美股不删港股，改动面小很多。
3. **Config 文件巨大**：`src/config.py`（117KB）中散布着美股/港股/长桥/yfinance 的配置项，清理时需细心，避免误删 A 股相关配置。
4. **测试文件**：`tests/` 下有 100+ 测试文件，很多涉及美股和已删模块，需要同步清理否则 CI 会挂。
5. **Agent 工具依赖**：`src/agent/tools/market_tools.py` 中的 `get_market_indices`、`get_sector_rankings` 可能引用了美股指数，需要检查。
6. **前端 hardcode**：`apps/dsa-web/` 中可能有美股相关的 UI 文案或市场选择器，需要排查。
