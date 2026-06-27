import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { ChevronLeft, RefreshCw, Search, X } from 'lucide-react';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { knowledgeApi, type KnowledgeItem, type CrawlProgressResponse } from '../api/knowledge';
import { ApiErrorAlert } from '../components/common';
import { createParsedApiError, type ParsedApiError } from '../api/error';
import { cn } from '../utils/cn';

// ============================================================
// Types
// ============================================================

interface FlowItem {
  label: string;
  flow: number | null;
  ratio?: number | null;
}

interface StructuredData {
  code: string;
  name: string;
  category: string;
  price: number | null;
  change_pct: number | null;
  company_count: number | null;
  lead_stock_name: string;
  lead_stock_code: string;
  today: FlowItem[];
  '5day': FlowItem[];
  '10day': FlowItem[];
  cumulative: FlowItem[];
  cum_start_date: string;
  cum_updated_at: number | null;
  updated_at: number | null;
}

// ============================================================
// Constants
// ============================================================

const CATEGORIES = [
  { key: 'all', label: '全部' },
  { key: 'bk', label: '板块' },
  { key: 'sh', label: '沪市' },
  { key: 'sz', label: '深市' },
] as const;

const POLL_INTERVAL = 2000; // 2 seconds

const PERIOD_TABS = [
  { key: 'today', label: '今日' },
  { key: '5day', label: '5日' },
  { key: '10day', label: '10日' },
] as const;

// ============================================================
// Helpers
// ============================================================

/** Extract structured data JSON from markdown content */
function extractStructuredData(markdown: string): StructuredData | null {
  const match = markdown.match(/<!-- structured-data\n([\s\S]*?)\nstructured-data -->/);
  if (match) {
    try {
      return JSON.parse(match[1]) as StructuredData;
    } catch {
      return null;
    }
  }
  return null;
}

/** Format flow value to human readable string */
function formatFlow(value: number | null): string {
  if (value === null || value === undefined) return '-';
  const abs = Math.abs(value);
  if (abs >= 1e8) {
    return `${(value / 1e8).toFixed(2)} 亿`;
  }
  if (abs >= 1e4) {
    return `${(value / 1e4).toFixed(2)} 万`;
  }
  return `${value.toFixed(2)}`;
}

/** Format ratio value to percentage string */
function formatRatio(value: number | null | undefined): string {
  if (value === null || value === undefined) return '-';
  // ratio is stored as decimal (e.g., 0.0233 = 2.33%)
  return `${(value * 100).toFixed(2)}%`;
}

// ============================================================
// Sub-components
// ============================================================

const FlowTable: React.FC<{ data: FlowItem[]; showRatio?: boolean }> = ({ data, showRatio = true }) => {
  return (
    <div className="overflow-hidden rounded-lg border border-border">
      <table className="w-full text-sm">
        <thead>
          <tr className="bg-muted/50">
            <th className="px-4 py-2 text-left font-medium text-foreground">类型</th>
            <th className="px-4 py-2 text-right font-medium text-foreground">净流入</th>
            {showRatio && (
              <th className="px-4 py-2 text-right font-medium text-foreground">占比</th>
            )}
          </tr>
        </thead>
        <tbody>
          {data.map((item) => (
            <tr key={item.label} className="border-t border-border hover:bg-muted/30">
              <td className="px-4 py-2 font-medium text-foreground">{item.label}</td>
              <td className={cn(
                'px-4 py-2 text-right font-mono',
                item.flow !== null
                  ? item.flow >= 0 ? 'text-danger' : 'text-success'
                  : 'text-muted-text'
              )}>
                {formatFlow(item.flow)}
              </td>
              {showRatio && (
                <td className={cn(
                  'px-4 py-2 text-right font-mono',
                  item.ratio !== null && item.ratio !== undefined
                    ? item.ratio >= 0 ? 'text-danger' : 'text-success'
                    : 'text-muted-text'
                )}>
                  {formatRatio(item.ratio)}
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

// ============================================================
// KnowledgePage component
// ============================================================

const KnowledgePage: React.FC = () => {
  // State
  const [items, setItems] = useState<KnowledgeItem[]>([]);
  const [filteredItems, setFilteredItems] = useState<KnowledgeItem[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchKeyword, setSearchKeyword] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<ParsedApiError | null>(null);

  // Crawl state
  const [crawlProgress, setCrawlProgress] = useState<CrawlProgressResponse | null>(null);
  const pollingRef = useRef<ReturnType<typeof setInterval> | null>(null);

  // Markdown view state
  const [selectedItem, setSelectedItem] = useState<KnowledgeItem | null>(null);
  const [markdownContent, setMarkdownContent] = useState<string>('');
  const [markdownLoading, setMarkdownLoading] = useState(false);
  const [markdownError, setMarkdownError] = useState<string | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState<string>('today');

  // Parse structured data
  const structuredData = useMemo(() => extractStructuredData(markdownContent), [markdownContent]);

  // Clean markdown (remove structured data block)
  const cleanMarkdown = useMemo(() => {
    return markdownContent.replace(/<!-- structured-data[\s\S]*?structured-data -->/g, '').trim();
  }, [markdownContent]);

  // ============================================================
  // Data fetching
  // ============================================================

  const fetchItems = useCallback(async (category?: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await knowledgeApi.listItems(category === 'all' ? undefined : category);
      setItems(response.data);
      setFilteredItems(response.data);
    } catch (err) {
      setError(createParsedApiError({
        title: '获取知识库列表失败',
        message: err instanceof Error ? err.message : '获取数据失败，请稍后重试',
        category: 'unknown',
      }));
    } finally {
      setLoading(false);
    }
  }, []);

  // Initial load
  useEffect(() => {
    void fetchItems(selectedCategory);
  }, [fetchItems, selectedCategory]);

  // ============================================================
  // Search
  // ============================================================

  useEffect(() => {
    if (!searchKeyword.trim()) {
      setFilteredItems(items);
      return;
    }

    const keyword = searchKeyword.toLowerCase();
    const filtered = items.filter(
      (item) =>
        item.code.toLowerCase().includes(keyword) ||
        item.name.toLowerCase().includes(keyword),
    );
    setFilteredItems(filtered);
  }, [searchKeyword, items]);

  // ============================================================
  // Crawl handling
  // ============================================================

  const startPolling = useCallback(() => {
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
    }

    pollingRef.current = setInterval(async () => {
      try {
        const progress = await knowledgeApi.getProgress();
        setCrawlProgress(progress);

        if (progress.status === 'done' || progress.status === 'error') {
          // Stop polling
          if (pollingRef.current) {
            clearInterval(pollingRef.current);
            pollingRef.current = null;
          }
          setRefreshing(false);

          // Reload items on success
          if (progress.status === 'done') {
            void fetchItems(selectedCategory);
          }
        }
      } catch {
        // Ignore polling errors
      }
    }, POLL_INTERVAL);
  }, [fetchItems, selectedCategory]);

  const stopPolling = useCallback(() => {
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
      pollingRef.current = null;
    }
  }, []);

  // Cleanup polling on unmount
  useEffect(() => {
    return () => {
      stopPolling();
    };
  }, [stopPolling]);

  const handleRefresh = useCallback(async () => {
    setRefreshing(true);
    setError(null);

    // 立即显示爬取中的状态
    setCrawlProgress({
      total: 0,
      current: 0,
      status: 'crawling',
      message: '正在启动爬取任务...',
      errors: [],
    });

    try {
      const progress = await knowledgeApi.triggerCrawl();
      setCrawlProgress(progress);

      if (progress.status === 'crawling') {
        // Start polling for progress
        startPolling();
      } else if (progress.status === 'done') {
        // Already done
        setRefreshing(false);
        void fetchItems(selectedCategory);
      } else {
        // Error or idle
        setRefreshing(false);
      }
    } catch (err: unknown) {
      // 检查是否是 409 (已有爬取任务在进行中)
      const isConflict = err instanceof Error && err.message.includes('409');
      if (isConflict) {
        // 已有爬取任务，开始轮询进度
        setCrawlProgress({
          total: 0,
          current: 0,
          status: 'crawling',
          message: '已有爬取任务在进行中，正在获取进度...',
          errors: [],
        });
        startPolling();
      } else {
        setError(createParsedApiError({
          title: '启动爬取失败',
          message: err instanceof Error ? err.message : '启动爬取任务失败，请稍后重试',
          category: 'unknown',
        }));
        setRefreshing(false);
      }
    }
  }, [fetchItems, selectedCategory, startPolling]);

  // ============================================================
  // Markdown viewing
  // ============================================================

  const handleItemClick = useCallback(async (item: KnowledgeItem) => {
    setSelectedItem(item);
    setMarkdownLoading(true);
    setMarkdownError(null);

    try {
      const response = await knowledgeApi.getMarkdown(item.category, item.code);
      setMarkdownContent(response.content);
    } catch (err) {
      setMarkdownError(err instanceof Error ? err.message : '加载失败');
    } finally {
      setMarkdownLoading(false);
    }
  }, []);

  const handleBackToList = useCallback(() => {
    setSelectedItem(null);
    setMarkdownContent('');
    setMarkdownError(null);
  }, []);

  // ============================================================
  // Category change
  // ============================================================

  const handleCategoryChange = useCallback((category: string) => {
    setSelectedCategory(category);
    setSearchKeyword('');
  }, []);

  // ============================================================
  // Render helpers
  // ============================================================

  const renderProgressBar = () => {
    if (!crawlProgress || crawlProgress.status === 'idle') return null;

    const percent = crawlProgress.total > 0
      ? Math.round((crawlProgress.current / crawlProgress.total) * 100)
      : 0;

    return (
      <div className="mb-4 rounded-lg border border-border bg-card p-4">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-foreground">
            {crawlProgress.status === 'crawling' ? '正在爬取...' :
             crawlProgress.status === 'done' ? '爬取完成' :
             crawlProgress.status === 'error' ? '爬取失败' : ''}
          </span>
          <span className="text-sm text-muted-text">
            {crawlProgress.total > 0 ? `${crawlProgress.current} / ${crawlProgress.total}` : '初始化中...'}
          </span>
        </div>
        <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
          <div
            className={cn(
              'h-full rounded-full transition-all duration-300',
              crawlProgress.status === 'error' ? 'bg-danger' : 'bg-primary',
            )}
            style={{ width: `${percent}%` }}
          />
        </div>
        {crawlProgress.message && (
          <p className="mt-2 text-xs text-muted-text">{crawlProgress.message}</p>
        )}
        {crawlProgress.errors.length > 0 && (
          <div className="mt-2">
            {crawlProgress.errors.map((err, idx) => (
              <p key={idx} className="text-xs text-danger">{err}</p>
            ))}
          </div>
        )}
      </div>
    );
  };

  const renderSearchBar = () => (
    <div className="relative mb-4">
      <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-text" />
      <input
        type="text"
        value={searchKeyword}
        onChange={(e) => setSearchKeyword(e.target.value)}
        placeholder="搜索代码或名称..."
        className="w-full rounded-lg border border-border bg-card py-2 pl-10 pr-10 text-sm text-foreground placeholder:text-muted-text focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
      />
      {searchKeyword && (
        <button
          type="button"
          onClick={() => setSearchKeyword('')}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-text hover:text-foreground"
        >
          <X className="h-4 w-4" />
        </button>
      )}
    </div>
  );

  const renderCategoryTabs = () => (
    <div className="mb-4 flex flex-wrap gap-2">
      {CATEGORIES.map(({ key, label }) => (
        <button
          key={key}
          type="button"
          onClick={() => handleCategoryChange(key)}
          className={cn(
            'rounded-lg px-3 py-1.5 text-sm transition-colors',
            selectedCategory === key
              ? 'bg-primary text-primary-foreground'
              : 'bg-card text-secondary-text hover:bg-hover hover:text-foreground',
          )}
        >
          {label}
        </button>
      ))}
    </div>
  );

  const renderItemsList = () => {
    if (loading) {
      return (
        <div className="flex flex-col items-center justify-center h-64">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary/20 border-t-primary" />
          <p className="mt-4 text-sm text-muted-text">加载中...</p>
        </div>
      );
    }

    if (filteredItems.length === 0) {
      return (
        <div className="flex flex-col items-center justify-center h-64 text-muted-text">
          <p className="text-sm">
            {searchKeyword ? '未找到匹配的条目' : '暂无数据，请先点击刷新按钮爬取数据'}
          </p>
        </div>
      );
    }

    return (
      <div className="flex flex-wrap gap-2">
        {filteredItems.map((item) => (
          <button
            key={`${item.category}-${item.code}`}
            type="button"
            onClick={() => void handleItemClick(item)}
            className="inline-flex items-center gap-1.5 rounded-lg border border-border bg-card px-3 py-2 text-sm transition-colors hover:border-primary hover:bg-hover"
          >
            <span className="font-medium text-foreground">{item.name}</span>
            <span className="text-muted-text">{item.code}</span>
            {item.changePct !== null && item.changePct !== undefined && (
              <span
                className={cn(
                  'text-xs',
                  item.changePct >= 0 ? 'text-danger' : 'text-success',
                )}
              >
                {item.changePct >= 0 ? '+' : ''}{item.changePct.toFixed(2)}%
              </span>
            )}
          </button>
        ))}
      </div>
    );
  };

  const renderMarkdownView = () => {
    if (!selectedItem) return null;

    return (
      <div className="flex flex-col h-full">
        {/* Header with back button */}
        <div className="mb-4 flex items-center gap-3">
          <button
            type="button"
            onClick={handleBackToList}
            className="inline-flex items-center gap-1 rounded-lg px-3 py-2 text-sm text-secondary-text transition-colors hover:bg-hover hover:text-foreground"
          >
            <ChevronLeft className="h-4 w-4" />
            返回
          </button>
          <div>
            <h2 className="text-base font-semibold text-foreground">{selectedItem.name}</h2>
            <p className="text-xs text-muted-text">{selectedItem.code}</p>
          </div>
        </div>

        {/* Structured data view (with custom tables) */}
        {structuredData && (
          <div className="mb-4 flex-1 overflow-y-auto">
            {/* Basic info card */}
            <div className="mb-4 rounded-lg border border-border bg-card p-4">
              <div className="flex items-center gap-4 flex-wrap">
                <div>
                  <span className="text-sm text-muted-text">板块指数</span>
                  <p className="text-lg font-semibold text-foreground">{structuredData.price?.toFixed(2) ?? '-'}</p>
                </div>
                {structuredData.change_pct !== null && (
                  <div>
                    <span className="text-sm text-muted-text">涨跌幅</span>
                    <p className={cn(
                      'text-lg font-semibold',
                      structuredData.change_pct >= 0 ? 'text-danger' : 'text-success',
                    )}>
                      {structuredData.change_pct >= 0 ? '+' : ''}{structuredData.change_pct.toFixed(2)}%
                    </p>
                  </div>
                )}
                {structuredData.company_count !== null && (
                  <div>
                    <span className="text-sm text-muted-text">成分公司</span>
                    <p className="text-lg font-semibold text-foreground">{structuredData.company_count}</p>
                  </div>
                )}
                {structuredData.lead_stock_name && (
                  <div>
                    <span className="text-sm text-muted-text">领涨股</span>
                    <p className="text-sm font-medium text-foreground">{structuredData.lead_stock_name} ({structuredData.lead_stock_code})</p>
                  </div>
                )}
              </div>
            </div>

            {/* Update time */}
            {structuredData.updated_at && (
              <div className="mb-4 text-xs text-muted-text">
                数据更新时间: {new Date(structuredData.updated_at * 1000).toLocaleString('zh-CN')}
              </div>
            )}

            {/* Period tabs */}
            <div className="mb-3 flex gap-2">
              {PERIOD_TABS.map(({ key, label }) => (
                <button
                  key={key}
                  type="button"
                  onClick={() => setSelectedPeriod(key)}
                  className={cn(
                    'rounded-lg px-3 py-1.5 text-sm transition-colors',
                    selectedPeriod === key
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-card text-secondary-text hover:bg-hover hover:text-foreground',
                  )}
                >
                  {label}
                </button>
              ))}
            </div>

            {/* Flow table */}
            <FlowTable data={structuredData[selectedPeriod as keyof StructuredData] as FlowItem[]} />

            {/* Cumulative flow table */}
            {structuredData.cumulative && structuredData.cumulative.length > 0 && (
              <div className="mt-4">
                <div className="mb-2 flex items-center gap-2">
                  <h3 className="text-sm font-semibold text-foreground">
                    历史资金流（{structuredData.cum_start_date}起）
                  </h3>
                  {structuredData.cum_updated_at && (
                    <span className="text-xs text-muted-text">
                      最后更新: {new Date(structuredData.cum_updated_at * 1000).toLocaleString('zh-CN')}
                    </span>
                  )}
                </div>
                <FlowTable data={structuredData.cumulative} showRatio={false} />
              </div>
            )}
          </div>
        )}

        {/* Markdown content (as fallback) */}
        {!structuredData && (
          <>
            {markdownLoading ? (
              <div className="flex flex-col items-center justify-center h-64">
                <div className="h-8 w-8 animate-spin rounded-full border-2 border-primary/20 border-t-primary" />
                <p className="mt-4 text-sm text-muted-text">加载中...</p>
              </div>
            ) : markdownError ? (
              <div className="flex flex-col items-center justify-center h-64">
                <p className="text-sm text-danger">{markdownError}</p>
              </div>
            ) : (
              <div
                className="flex-1 overflow-y-auto rounded-lg border border-border bg-card p-4
                  prose prose-invert prose-sm max-w-none
                  prose-headings:text-foreground prose-headings:font-semibold prose-headings:mt-4 prose-headings:mb-2
                  prose-h1:text-xl
                  prose-h2:text-lg
                  prose-h3:text-base
                  prose-p:leading-relaxed prose-p:mb-3 prose-p:last:mb-0
                  prose-strong:text-foreground prose-strong:font-semibold
                  prose-ul:my-2 prose-ol:my-2 prose-li:my-1
                  prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:before:content-none prose-code:after:content-none
                  prose-pre:border
                  prose-table:border-collapse
                  prose-th:border prose-th:border-border prose-th:px-3 prose-th:py-2
                  prose-td:border prose-td:border-border prose-td:px-3 prose-td:py-2
                  prose-hr:my-4
                  prose-a:no-underline hover:prose-a:underline
                  prose-blockquote:text-secondary-text
                  whitespace-pre-line break-words
                "
              >
                <Markdown remarkPlugins={[remarkGfm]}>
                  {cleanMarkdown}
                </Markdown>
              </div>
            )}
          </>
        )}
      </div>
    );
  };

  // ============================================================
  // Main render
  // ============================================================

  return (
    <div className="flex flex-col h-full p-4">
      {/* Page header */}
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-foreground">知识库</h1>
          <p className="text-sm text-muted-text">
            板块和股票信息 · 共 {filteredItems.length} 条
          </p>
        </div>
        <button
          type="button"
          onClick={() => void handleRefresh()}
          disabled={refreshing}
          className="btn-ghost inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-hover disabled:opacity-50"
          title="刷新数据"
        >
          <RefreshCw className={cn('h-4 w-4', refreshing && 'animate-spin')} />
          刷新
        </button>
      </div>

      {/* Error alert */}
      {error && (
        <div className="mb-4">
          <ApiErrorAlert error={error} />
        </div>
      )}

      {/* Progress bar */}
      {renderProgressBar()}

      {/* Main content */}
      {selectedItem ? (
        renderMarkdownView()
      ) : (
        <>
          {/* Search bar */}
          {renderSearchBar()}

          {/* Category tabs */}
          {renderCategoryTabs()}

          {/* Items list */}
          {renderItemsList()}
        </>
      )}
    </div>
  );
};

export default KnowledgePage;
