import type React from 'react';
import { useCallback, useEffect, useRef, useState } from 'react';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { BarChart3, Copy, Check, Calendar } from 'lucide-react';
import { analysisApi } from '../api/analysis';
import { getParsedApiError, type ParsedApiError } from '../api/error';
import { ApiErrorAlert, Button, InlineAlert } from '../components/common';

type MarketReviewNotice = {
  variant: 'success' | 'warning' | 'danger';
  title: string;
  message: string;
} | null;

interface ReportEntry {
  hour: string;
  filename: string;
  content: string;
}

function formatDate(d: Date): string {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}${m}${day}`;
}

function formatDateDisplay(d: string): string {
  if (d.length !== 8) return d;
  return `${d.slice(0, 4)}-${d.slice(4, 6)}-${d.slice(6, 8)}`;
}

const MarketReviewPage: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState(() => formatDate(new Date()));
  const [reports, setReports] = useState<ReportEntry[]>([]);
  const [isLoadingReports, setIsLoadingReports] = useState(false);
  const [reportLoadError, setReportLoadError] = useState<ParsedApiError | null>(null);

  // Trigger state
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [notice, setNotice] = useState<MarketReviewNotice>(null);
  const [triggerError, setTriggerError] = useState<ParsedApiError | null>(null);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  const pollTimer = useRef<number | null>(null);

  const stopPolling = useCallback(() => {
    if (pollTimer.current !== null) {
      window.clearInterval(pollTimer.current);
      pollTimer.current = null;
    }
  }, []);

  useEffect(() => () => stopPolling(), [stopPolling]);

  // Load reports for selected date
  const loadReports = useCallback(async (date: string) => {
    setIsLoadingReports(true);
    setReportLoadError(null);
    try {
      const data = await analysisApi.getMarketReviewReportsByDate(date);
      setReports(data.reports ?? []);
    } catch (err: unknown) {
      const parsed = getParsedApiError(err);
      if (parsed.status === 404) {
        setReports([]);
        setReportLoadError(null);
      } else {
        setReportLoadError(parsed);
        setReports([]);
      }
    } finally {
      setIsLoadingReports(false);
    }
  }, []);

  useEffect(() => {
    void loadReports(selectedDate);
  }, [selectedDate, loadReports]);

  // Poll task status after triggering
  const pollTaskStatus = useCallback(
    async (taskId: string) => {
      stopPolling();
      const maxAttempts = 120;
      const intervalMs = 2000;
      let attempts = 0;

      const poll = async (): Promise<boolean> => {
        if (attempts >= maxAttempts) {
          stopPolling();
          setNotice({
            variant: 'danger',
            title: '大盘复盘已超时',
            message: '任务长时间未返回最终结果，请稍后刷新查看。',
          });
          return false;
        }
        attempts += 1;

        try {
          const status = await analysisApi.getStatus(taskId);
          if (status.status === 'pending' || status.status === 'processing') {
            const progress = typeof status.progress === 'number' ? `${status.progress}%` : '进行中';
            setNotice({
              variant: 'warning',
              title: '大盘复盘进行中',
              message: `任务状态：${status.status}（${progress}）`,
            });
            return true;
          }

          if (status.status === 'completed') {
            stopPolling();
            setNotice({
              variant: 'success',
              title: '大盘复盘已完成',
              message: '报告已生成，正在刷新列表...',
            });
            setTriggerError(null);
            // Reload reports for today
            void loadReports(formatDate(new Date()));
            return false;
          }

          if (status.status === 'failed') {
            stopPolling();
            setTriggerError(
              getParsedApiError({
                response: {
                  status: 500,
                  data: {
                    error: 'market_review_failed',
                    message: status.error || '大盘复盘执行失败。',
                  },
                },
              }),
            );
            setNotice(null);
            return false;
          }

          stopPolling();
          setNotice({
            variant: 'danger',
            title: '大盘复盘状态异常',
            message: `收到未知任务状态：${status.status}`,
          });
          return false;
        } catch {
          if (attempts >= maxAttempts) {
            stopPolling();
            return false;
          }
          return true;
        }
      };

      if (await poll()) {
        pollTimer.current = window.setInterval(() => {
          void poll().then((shouldContinue) => {
            if (!shouldContinue) stopPolling();
          });
        }, intervalMs);
      }
    },
    [stopPolling, loadReports],
  );

  const handleTrigger = useCallback(async () => {
    setIsSubmitting(true);
    setNotice(null);
    setTriggerError(null);
    try {
      const result = await analysisApi.triggerMarketReview({ sendNotification: false });
      setNotice({
        variant: 'success',
        title: '大盘复盘已提交',
        message: result.message,
      });
      if (result.taskId) {
        await pollTaskStatus(result.taskId);
      }
    } catch (err: unknown) {
      setTriggerError(getParsedApiError(err));
      setNotice(null);
    } finally {
      setIsSubmitting(false);
    }
  }, [pollTaskStatus]);

  const handleCopy = useCallback((content: string, index: number) => {
    void navigator.clipboard.writeText(content).then(() => {
      setCopiedIndex(index);
      setTimeout(() => setCopiedIndex(null), 2000);
    });
  }, []);

  const handleDateChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value.replace(/-/g, '');
    if (/^\d{8}$/.test(val)) {
      setSelectedDate(val);
    }
  }, []);

  return (
    <div className="flex h-[calc(100vh-5rem)] w-full flex-col overflow-hidden sm:h-[calc(100vh-5.5rem)] lg:h-[calc(100vh-2rem)]">
      <div className="flex-1 flex flex-col min-h-0 min-w-0 max-w-full lg:max-w-6xl mx-auto w-full">
        {/* Header */}
        <header className="flex min-w-0 flex-shrink-0 items-center justify-between gap-3 px-3 py-3 md:px-4 md:py-4">
          <div className="flex items-center gap-2.5">
            <BarChart3 className="h-5 w-5 text-primary" />
            <h1 className="text-base font-semibold text-foreground">大盘复盘</h1>
          </div>
          <div className="flex items-center gap-2.5">
            <div className="relative flex items-center">
              <Calendar className="absolute left-2.5 h-4 w-4 text-secondary-text pointer-events-none" />
              <input
                type="date"
                value={`${selectedDate.slice(0, 4)}-${selectedDate.slice(4, 6)}-${selectedDate.slice(6, 8)}`}
                onChange={handleDateChange}
                className="h-10 rounded-xl border border-subtle bg-surface/60 pl-8 pr-3 text-sm text-foreground transition-colors hover:border-subtle-hover focus:border-primary focus:outline-none"
              />
            </div>
            <Button
              type="button"
              variant="primary"
              size="md"
              isLoading={isSubmitting}
              loadingText="提交中"
              onClick={() => void handleTrigger()}
              className="h-10 whitespace-nowrap"
            >
              <BarChart3 className="h-4 w-4" aria-hidden="true" />
              大盘分析
            </Button>
          </div>
        </header>

        {/* Notice / Error */}
        {notice ? (
          <div className="px-3 pb-2 md:px-4">
            <InlineAlert
              variant={notice.variant}
              title={notice.title}
              message={notice.message}
              className="rounded-xl px-3 py-2 text-xs shadow-none"
            />
          </div>
        ) : null}

        {triggerError ? (
          <div className="px-3 pb-2 md:px-4">
            <ApiErrorAlert
              error={triggerError}
              className="mb-1"
              onDismiss={() => setTriggerError(null)}
            />
          </div>
        ) : null}

        {/* Content */}
        <section className="flex-1 min-h-0 overflow-y-auto px-3 pb-4 md:px-6">
          {isLoadingReports ? (
            <div className="flex h-full flex-col items-center justify-center">
              <div className="h-10 w-10 animate-spin rounded-full border-[3px] border-primary/20 border-t-primary" />
              <p className="mt-4 text-sm text-secondary-text">加载报告中...</p>
            </div>
          ) : reportLoadError ? (
            <div className="flex h-full items-center justify-center">
              <ApiErrorAlert error={reportLoadError} />
            </div>
          ) : reports.length === 0 ? (
            <div className="flex h-full flex-col items-center justify-center">
              <div className="rounded-xl border border-dashed border-subtle px-8 py-12 text-center">
                <BarChart3 className="mx-auto h-8 w-8 text-secondary-text mb-3" />
                <p className="text-sm text-secondary-text">
                  {formatDateDisplay(selectedDate)} 暂无大盘复盘报告
                </p>
                <p className="mt-1 text-xs text-muted-text">
                  点击右上角"大盘分析"按钮生成当天报告
                </p>
              </div>
            </div>
          ) : (
            <div className="max-w-4xl space-y-6 pb-8">
              <p className="text-xs text-secondary-text">
                {formatDateDisplay(selectedDate)} 共 {reports.length} 份报告
              </p>
              {reports.map((report, index) => (
                <div
                  key={report.filename}
                  className="rounded-xl border border-subtle bg-surface/70 shadow-sm"
                >
                  <div className="flex items-center justify-between gap-2 border-b border-subtle px-4 py-2.5">
                    <p className="text-sm font-medium text-foreground">
                      {report.hour}:00 报告
                    </p>
                    <button
                      type="button"
                      className="flex h-7 items-center gap-1 rounded-md px-2.5 text-xs text-secondary-text transition-colors hover:bg-hover hover:text-foreground"
                      disabled={copiedIndex === index}
                      onClick={() => handleCopy(report.content, index)}
                    >
                      {copiedIndex === index ? (
                        <>
                          <Check className="h-3.5 w-3.5 text-success" />
                          已复制
                        </>
                      ) : (
                        <>
                          <Copy className="h-3.5 w-3.5" />
                          复制
                        </>
                      )}
                    </button>
                  </div>
                  <div
                    className="home-markdown-prose prose prose-invert prose-sm max-w-none px-4 py-4
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
                      prose-hr:my-4
                      prose-a:no-underline hover:prose-a:underline
                      prose-blockquote:text-secondary-text
                      whitespace-pre-line break-words
                    "
                  >
                    <Markdown remarkPlugins={[remarkGfm]}>
                      {report.content}
                    </Markdown>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
};

export default MarketReviewPage;
