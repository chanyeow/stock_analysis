import React, { useCallback, useEffect, useMemo, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { ChevronLeft, ChevronRight, RefreshCw } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { capitalFlowApi, type CapitalFlowItem, type CapitalFlowTableItem } from '../api/capitalFlow';
import { ApiErrorAlert } from '../components/common';
import { createParsedApiError, type ParsedApiError } from '../api/error';
import { cn } from '../utils/cn';

// ============================================================
// Constants
// ============================================================

const CATEGORIES = [
  { key: 'industry', label: '行业资金流' },
  { key: 'concept', label: '概念资金流' },
] as const;

const PERIODS = [
  { key: 'today', label: '今日' },
  { key: '5day', label: '5日' },
  { key: '10day', label: '10日' },
] as const;

const CHART_HEIGHT = 500;
const BAR_WIDTH = 18;       // fixed bar width in px
const BAR_GAP = 4;          // gap between bars in px
const X_LABEL_EXTRA = 80;   // extra width for first/last label padding
const PAGE_SIZE = 50;

// Symlog threshold: values below ~1亿 stay roughly linear,
// values above are compressed logarithmically.
const SYMLOG_C = 1e8;

// ============================================================
// Symlog scale
// ============================================================

/** sign(x) * log10(1 + |x| / C) */
function symlog(x: number, C: number = SYMLOG_C): number {
  if (x === 0) return 0;
  return Math.sign(x) * Math.log10(1 + Math.abs(x) / C);
}

/** sign(x) * (10^|x| - 1) * C */
function inverseSymlog(y: number, C: number = SYMLOG_C): number {
  if (y === 0) return 0;
  return Math.sign(y) * (Math.pow(10, Math.abs(y)) - 1) * C;
}

/** Generate nice symlog-space tick values spanning the data range */
function makeSymlogTicks(dataMax: number, dataMin: number, C: number = SYMLOG_C): number[] {
  const yMax = symlog(dataMax, C);
  const yMin = symlog(dataMin, C);
  const ticks: number[] = [];

  // Negative ticks
  if (yMin < 0) {
    let tick = -Math.ceil(Math.abs(yMin));
    while (tick <= 0) {
      ticks.push(tick);
      tick += 1;
    }
  }
  // Positive ticks
  if (yMax > 0) {
    for (let tick = 1; tick <= Math.ceil(yMax); tick++) {
      ticks.push(tick);
    }
  }

  // Always include 0
  if (!ticks.includes(0)) ticks.push(0);
  ticks.sort((a, b) => a - b);
  return ticks;
}

// ============================================================
// Formatting helpers
// ============================================================

function formatFlow(value: number): string {
  const abs = Math.abs(value);
  if (abs >= 1e8) {
    return `${(value / 1e8).toFixed(2)} 亿`;
  }
  if (abs >= 1e4) {
    return `${(value / 1e4).toFixed(2)} 万`;
  }
  return `${value.toFixed(0)}`;
}

function formatTooltipFlow(value: number): string {
  const abs = Math.abs(value);
  if (abs >= 1e8) {
    return `${(value / 1e8).toFixed(2)} 亿元`;
  }
  if (abs >= 1e4) {
    return `${(value / 1e4).toFixed(2)} 万元`;
  }
  return `${value.toFixed(0)} 元`;
}

// ============================================================
// Custom Tooltip
// ============================================================

interface ChartDatum {
  name: string;
  code: string;
  flow: number;       // original value for tooltip
  displayFlow: number; // symlog-transformed value for bar length
}

const CustomTooltip: React.FC<{
  active?: boolean;
  payload?: Array<{ payload: ChartDatum }>;
}> = ({ active, payload }) => {
  if (!active || !payload || payload.length === 0) return null;
  const item = payload[0].payload;
  const isInflow = item.flow >= 0;
  return (
    <div className="rounded-lg border border-border bg-popover px-3 py-2 text-sm shadow-lg">
      <div className="font-medium text-foreground">{item.name}</div>
      <div className="text-muted-foreground text-xs">{item.code}</div>
      <div className={cn('mt-1 font-mono text-xs', isInflow ? 'text-red-400' : 'text-green-400')}>
        {isInflow ? '+' : ''}{formatTooltipFlow(item.flow)}
      </div>
    </div>
  );
};

// ============================================================
// Custom X-axis tick (angled for space)
// ============================================================

interface XTickProps {
  x?: number | string;
  y?: number | string;
  payload?: { value: string };
}

const CustomXTick: React.FC<XTickProps> = ({ x, y, payload }) => {
  if (x === undefined || y === undefined || !payload) return null;
  const maxChars = 4;
  const text = payload.value;
  const displayText = text.length > maxChars ? text.slice(0, maxChars) + '…' : text;
  const nx = typeof x === 'string' ? parseFloat(x) : x;
  const ny = typeof y === 'string' ? parseFloat(y) : y;
  return (
    <text
      x={nx}
      y={ny}
      dy={10}
      textAnchor="end"
      transform={`rotate(-55, ${nx}, ${ny})`}
      fill="currentColor"
      className="text-[10px] fill-muted-foreground"
    >
      {displayText}
    </text>
  );
};

// ============================================================
// Page Component
// ============================================================

const CapitalFlowPage: React.FC = () => {
  const navigate = useNavigate();
  const [category, setCategory] = useState<'industry' | 'concept'>('industry');
  const [period, setPeriod] = useState<string>('today');
  const [data, setData] = useState<CapitalFlowItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<ParsedApiError | null>(null);
  const [refreshing, setRefreshing] = useState(false);

  // Table state (server-driven pagination)
  const [tableData, setTableData] = useState<CapitalFlowTableItem[]>([]);
  const [tablePage, setTablePage] = useState(1);
  const [tableTotal, setTableTotal] = useState(0);
  const [tableTotalPages, setTableTotalPages] = useState(1);
  const [tableLoading, setTableLoading] = useState(false);

  const fetchData = useCallback(
    async (cat: string, per: string, force: boolean = false) => {
      setError(null);
      if (force) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }
      try {
        const result = await capitalFlowApi.getData(
          cat as 'industry' | 'concept',
          per,
          force,
        );
        setData(result.data);
      } catch (err: unknown) {
        // 检查是否是 404 无数据错误
        const is404 = err instanceof Error && err.message.includes('404');
        const parsed = createParsedApiError({
          title: is404 ? '暂无数据' : '获取板块资金流失败',
          message: is404
            ? '未找到板块数据，请先到「知识库」页签点击刷新按钮爬取数据'
            : err instanceof Error ? err.message : '获取数据失败，请稍后重试',
          category: is404 ? 'unknown' : 'upstream_network',
        });
        setError(parsed);
      } finally {
        setLoading(false);
        setRefreshing(false);
      }
    },
    [],
  );

  const fetchTable = useCallback(
    async (cat: string, per: string, pg: number, force: boolean = false) => {
      setTableLoading(true);
      try {
        const result = await capitalFlowApi.getTable(
          cat as 'industry' | 'concept',
          per,
          pg,
          PAGE_SIZE,
          force,
        );
        setTableData(result.data);
        setTableTotal(result.total);
        setTableTotalPages(result.totalPages);
        setTablePage(result.page);
      } catch {
        // table error is non-blocking; just keep previous data
      } finally {
        setTableLoading(false);
      }
    },
    [],
  );

  // Auto-fetch on mount and when category/period changes
  useEffect(() => {
    void fetchData(category, period, false);
    void fetchTable(category, period, 1, false);
  }, [category, period, fetchData, fetchTable]);

  const handleRefresh = () => {
    void fetchData(category, period, true);
    void fetchTable(category, period, 1, true);
  };

  const handleTablePage = (pg: number) => {
    void fetchTable(category, period, pg, false);
  };

  // Sort descending + apply symlog transform for display
  const chartData: ChartDatum[] = useMemo(() => {
    const sorted = [...data].sort((a, b) => b.flow - a.flow);
    return sorted.map((item) => ({
      name: item.name,
      code: item.code,
      flow: item.flow,
      displayFlow: symlog(item.flow, SYMLOG_C),
    }));
  }, [data]);

  // Compute symlog ticks based on actual data range
  const symlogTicks = useMemo(() => {
    if (chartData.length === 0) return [];
    const flows = chartData.map((d) => d.flow);
    const dataMax = Math.max(...flows);
    const dataMin = Math.min(...flows);
    return makeSymlogTicks(dataMax, dataMin, SYMLOG_C);
  }, [chartData]);

  // Tick formatter: show original value labels at symlog positions
  const tickFormatter = (v: number) => formatFlow(inverseSymlog(v, SYMLOG_C));

  // Y-axis domain: ensure it covers the data range symmetrically
  const yDomain = useMemo(() => {
    if (symlogTicks.length === 0) return [0, 0] as [number, number];
    return [symlogTicks[0], symlogTicks[symlogTicks.length - 1]] as [number, number];
  }, [symlogTicks]);


  return (
    <div className="flex h-full flex-col gap-4 p-4 lg:p-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-xl font-semibold text-foreground">资金流</h1>
        {/* 刷新按钮已隐藏，数据从知识库读取 */}
        {false && (
          <button
            type="button"
            onClick={handleRefresh}
            disabled={refreshing}
            className="btn-ghost inline-flex items-center gap-2 rounded-lg px-3 py-2 text-sm transition-colors hover:bg-hover disabled:opacity-50"
            title="刷新数据"
          >
            <RefreshCw className={cn('h-4 w-4', refreshing && 'animate-spin')} />
            刷新
          </button>
        )}
      </div>

      {/* Category tabs */}
      <div className="flex gap-1 rounded-lg bg-muted p-1 w-fit">
        {CATEGORIES.map(({ key, label }) => (
          <button
            key={key}
            type="button"
            onClick={() => setCategory(key)}
            className={cn(
              'rounded-md px-4 py-2 text-sm font-medium transition-colors',
              category === key
                ? 'bg-background text-foreground shadow-sm'
                : 'text-muted-foreground hover:text-foreground',
            )}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Period selector */}
      <div className="flex items-center gap-2">
        <span className="text-sm text-muted-foreground">周期：</span>
        <div className="flex gap-1 rounded-lg bg-muted p-1">
          {PERIODS.map(({ key, label }) => (
            <button
              key={key}
              type="button"
              onClick={() => setPeriod(key)}
              className={cn(
                'rounded-md px-3 py-1.5 text-sm transition-colors',
                period === key
                  ? 'bg-background text-foreground shadow-sm'
                  : 'text-muted-foreground hover:text-foreground',
              )}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      {loading ? (
        <div className="flex flex-1 items-center justify-center">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-cyan/20 border-t-cyan" />
        </div>
      ) : error ? (
        <div className="flex-1">
          <ApiErrorAlert error={error} />
          {error.title === '暂无数据' ? (
            <button
              type="button"
              onClick={() => navigate('/knowledge')}
              className="btn-primary mt-4"
            >
              前往知识库爬取数据
            </button>
          ) : (
            <button
              type="button"
              onClick={handleRefresh}
              className="btn-primary mt-4"
            >
              重试
            </button>
          )}
        </div>
      ) : data.length === 0 ? (
        <div className="flex flex-1 items-center justify-center text-muted-foreground">
          暂无数据
        </div>
      ) : (
        <div
          className="flex-1 overflow-x-auto rounded-lg border border-border bg-card p-2"
          style={{ scrollbarWidth: 'thin' }}
        >
          <div
            style={{
              width: Math.max(600, chartData.length * (BAR_WIDTH + BAR_GAP) + X_LABEL_EXTRA),
              height: CHART_HEIGHT,
            }}
          >
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={chartData}
                margin={{ top: 8, right: 20, left: 60, bottom: 60 }}
                barCategoryGap={BAR_GAP}
              >
                <XAxis
                  dataKey="name"
                  type="category"
                  tick={(props: XTickProps) => <CustomXTick {...props} />}
                  axisLine={{ stroke: 'hsl(var(--border))' }}
                  tickLine={false}
                  interval={0}
                  height={60}
                />
                <YAxis
                  dataKey="displayFlow"
                  type="number"
                  domain={yDomain}
                  ticks={symlogTicks}
                  tickFormatter={tickFormatter}
                  tick={{ fontSize: 11, fill: 'hsl(var(--muted-foreground))' }}
                  axisLine={{ stroke: 'hsl(var(--border))' }}
                  tickLine={false}
                  width={60}
                />
                <Tooltip content={<CustomTooltip />} cursor={{ fill: 'hsl(var(--muted)/0.3)' }} />
                <Bar
                  dataKey="displayFlow"
                  radius={[2, 2, 0, 0]}
                  maxBarSize={BAR_WIDTH}
                  fillOpacity={0.85}
                >
                  {chartData.map((entry: ChartDatum) => (
                    <Cell
                      key={entry.code}
                      fill={entry.flow >= 0 ? '#ef4444' : '#22c55e'}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Table */}
      {!loading && !error && data.length > 0 && (
        <div className="flex flex-col gap-2">
          <div
            className="overflow-x-auto rounded-lg border border-border"
            style={{ scrollbarWidth: 'thin' }}
          >
            <table className="w-max min-w-full text-xs whitespace-nowrap">
              <thead className="border-b border-border bg-muted/50">
                <tr>
                  <th className="sticky left-0 z-10 bg-muted/50 px-2 py-2 text-center w-8">#</th>
                  <th className="px-2 py-2 text-left min-w-20">板块名称</th>
                  <th className="px-2 py-2 text-right w-12">家数</th>
                  <th className="px-2 py-2 text-right w-16">最新价</th>
                  <th className="px-2 py-2 text-right w-16">涨跌幅</th>
                  <th className="px-2 py-2 text-right w-28">净流入</th>
                  <th className="px-2 py-2 text-right w-28">主力净流入</th>
                  <th className="px-2 py-2 text-right w-14">主力%</th>
                  <th className="px-2 py-2 text-right w-28">超大单</th>
                  <th className="px-2 py-2 text-right w-14">超大%</th>
                  <th className="px-2 py-2 text-right w-28">大单</th>
                  <th className="px-2 py-2 text-right w-14">大单%</th>
                  <th className="px-2 py-2 text-right w-28">中单</th>
                  <th className="px-2 py-2 text-right w-14">中单%</th>
                  <th className="px-2 py-2 text-right w-28">小单</th>
                  <th className="px-2 py-2 text-right w-14">小单%</th>
                  <th className="px-2 py-2 text-left min-w-24">领涨股</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {tableLoading ? (
                  <tr>
                    <td colSpan={17} className="px-3 py-8 text-center text-muted-foreground">
                      加载中...
                    </td>
                  </tr>
                ) : tableData.length === 0 ? (
                  <tr>
                    <td colSpan={17} className="px-3 py-8 text-center text-muted-foreground">
                      暂无数据
                    </td>
                  </tr>
                ) : (
                  tableData.map((item, i) => {
                    const rowNum = (tablePage - 1) * PAGE_SIZE + i + 1;
                    const isInflow = item.flow >= 0;
                    const fmtFlow = (v: number | null) => {
                      if (v == null) return '-';
                      const prefix = v >= 0 ? '+' : '';
                      return prefix + formatTooltipFlow(v);
                    };
                    const fmtFlowColor = (v: number | null) =>
                      cn('px-2 py-1.5 text-right font-mono', v != null && v >= 0 ? 'text-red-400' : 'text-green-400');
                    const fmtRatio = (v: number | null) => {
                      if (v == null) return '-';
                      return `${(v >= 0 ? '+' : '')}${v.toFixed(2)}%`;
                    };
                    const fmtRatioColor = (v: number | null) =>
                      cn('px-2 py-1.5 text-right font-mono', v != null && v >= 0 ? 'text-red-400' : 'text-green-400');

                    return (
                      <tr key={item.code} className="transition-colors hover:bg-muted/30">
                        <td className="sticky left-0 z-10 bg-card px-2 py-1.5 text-center text-muted-foreground group-hover:bg-muted/30">
                          {rowNum}
                        </td>
                        <td className="px-2 py-1.5 font-medium">{item.name}</td>
                        <td className="px-2 py-1.5 text-right text-muted-foreground">
                          {item.companyCount ?? '-'}
                        </td>
                        <td className="px-2 py-1.5 text-right font-mono">
                          {item.price != null ? item.price.toFixed(2) : '-'}
                        </td>
                        <td className={cn(
                          'px-2 py-1.5 text-right font-mono',
                          item.changePct != null && item.changePct >= 0 ? 'text-red-400' : 'text-green-400',
                        )}>
                          {item.changePct != null ? `${item.changePct >= 0 ? '+' : ''}${item.changePct.toFixed(2)}%` : '-'}
                        </td>
                        <td className={cn('px-2 py-1.5 text-right font-mono', isInflow ? 'text-red-400' : 'text-green-400')}>
                          {isInflow ? '+' : ''}{formatTooltipFlow(item.flow)}
                        </td>
                        <td className={fmtFlowColor(item.mainFlow)}>{fmtFlow(item.mainFlow)}</td>
                        <td className={fmtRatioColor(item.mainRatio)}>{fmtRatio(item.mainRatio)}</td>
                        <td className={fmtFlowColor(item.superLargeFlow)}>{fmtFlow(item.superLargeFlow)}</td>
                        <td className={fmtRatioColor(item.superLargeRatio)}>{fmtRatio(item.superLargeRatio)}</td>
                        <td className={fmtFlowColor(item.largeFlow)}>{fmtFlow(item.largeFlow)}</td>
                        <td className={fmtRatioColor(item.largeRatio)}>{fmtRatio(item.largeRatio)}</td>
                        <td className={fmtFlowColor(item.mediumFlow)}>{fmtFlow(item.mediumFlow)}</td>
                        <td className={fmtRatioColor(item.mediumRatio)}>{fmtRatio(item.mediumRatio)}</td>
                        <td className={fmtFlowColor(item.smallFlow)}>{fmtFlow(item.smallFlow)}</td>
                        <td className={fmtRatioColor(item.smallRatio)}>{fmtRatio(item.smallRatio)}</td>
                        <td className="px-2 py-1.5">
                          {item.leadStockName ? (
                            <span>
                              {item.leadStockName}
                              {item.leadStockCode ? (
                                <span className="ml-1 font-mono text-muted-foreground">{item.leadStockCode}</span>
                              ) : null}
                            </span>
                          ) : '-'}
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {tableTotalPages > 1 && (
            <div className="flex items-center justify-between text-sm">
              <span className="text-xs text-muted-foreground">
                共 {tableTotal} 条，第 {tablePage}/{tableTotalPages} 页
              </span>
              <div className="flex items-center gap-1">
                <button
                  type="button"
                  onClick={() => handleTablePage(1)}
                  disabled={tablePage <= 1 || tableLoading}
                  className="rounded-md px-2 py-1 text-xs text-muted-foreground hover:bg-muted disabled:opacity-30"
                >
                  首页
                </button>
                <button
                  type="button"
                  onClick={() => handleTablePage(tablePage - 1)}
                  disabled={tablePage <= 1 || tableLoading}
                  className="rounded-md px-1.5 py-1 text-muted-foreground hover:bg-muted disabled:opacity-30"
                >
                  <ChevronLeft className="h-4 w-4" />
                </button>
                {Array.from({ length: Math.min(tableTotalPages, 7) }, (_, i) => {
                  let pageNum: number;
                  if (tableTotalPages <= 7) {
                    pageNum = i + 1;
                  } else if (tablePage <= 4) {
                    pageNum = i + 1;
                  } else if (tablePage >= tableTotalPages - 3) {
                    pageNum = tableTotalPages - 6 + i;
                  } else {
                    pageNum = tablePage - 3 + i;
                  }
                  return (
                    <button
                      key={pageNum}
                      type="button"
                      onClick={() => handleTablePage(pageNum)}
                      disabled={tableLoading}
                      className={cn(
                        'rounded-md px-2 py-1 text-xs',
                        pageNum === tablePage
                          ? 'bg-primary text-primary-foreground'
                          : 'text-muted-foreground hover:bg-muted',
                      )}
                    >
                      {pageNum}
                    </button>
                  );
                })}
                <button
                  type="button"
                  onClick={() => handleTablePage(tablePage + 1)}
                  disabled={tablePage >= tableTotalPages || tableLoading}
                  className="rounded-md px-1.5 py-1 text-muted-foreground hover:bg-muted disabled:opacity-30"
                >
                  <ChevronRight className="h-4 w-4" />
                </button>
                <button
                  type="button"
                  onClick={() => handleTablePage(tableTotalPages)}
                  disabled={tablePage >= tableTotalPages || tableLoading}
                  className="rounded-md px-2 py-1 text-xs text-muted-foreground hover:bg-muted disabled:opacity-30"
                >
                  末页
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Legend */}
      {!loading && !error && data.length > 0 && (
        <div className="flex items-center gap-4 text-xs text-muted-foreground">
          <span className="flex items-center gap-1">
            <span className="inline-block h-2.5 w-2.5 rounded-sm bg-red-500" /> 净流入
          </span>
          <span className="flex items-center gap-1">
            <span className="inline-block h-2.5 w-2.5 rounded-sm bg-green-500" /> 净流出
          </span>
        </div>
      )}
    </div>
  );
};

export default CapitalFlowPage;
