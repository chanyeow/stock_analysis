import React, { useCallback, useEffect, useState } from 'react';
import { RefreshCw, ScrollText, FileText } from 'lucide-react';
import { logsApi } from '../api/logs';
import { getParsedApiError, type ParsedApiError } from '../api/error';
import { ApiErrorAlert, Button, EmptyState, ScrollArea } from '../components/common';
import type { LogFileInfo } from '../types/logs';
import { cn } from '../utils/cn';

const LogsPage: React.FC = () => {
  useEffect(() => {
    document.title = '日志 - DSA';
  }, []);

  const [files, setFiles] = useState<LogFileInfo[]>([]);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [lines, setLines] = useState<string[]>([]);
  const [isLoadingList, setIsLoadingList] = useState(false);
  const [isLoadingContent, setIsLoadingContent] = useState(false);
  const [listError, setListError] = useState<ParsedApiError | null>(null);
  const [contentError, setContentError] = useState<ParsedApiError | null>(null);

  const loadFiles = useCallback(async () => {
    setIsLoadingList(true);
    setListError(null);
    try {
      const data = await logsApi.getList();
      setFiles(data.files);
      if (data.files.length > 0 && !selectedFile) {
        setSelectedFile(data.files[0].name);
      }
    } catch (err) {
      setListError(getParsedApiError(err));
    } finally {
      setIsLoadingList(false);
    }
  }, [selectedFile]);

  const loadContent = useCallback(async (filename: string) => {
    setIsLoadingContent(true);
    setContentError(null);
    try {
      const data = await logsApi.getContent(filename);
      setLines(data.lines);
    } catch (err) {
      setContentError(getParsedApiError(err));
    } finally {
      setIsLoadingContent(false);
    }
  }, []);

  useEffect(() => {
    void loadFiles();
  }, [loadFiles]);

  useEffect(() => {
    if (selectedFile) {
      void loadContent(selectedFile);
    }
  }, [selectedFile, loadContent]);

  const handleRefresh = () => {
    if (selectedFile) {
      void loadContent(selectedFile);
    }
  };

  const formatSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const formatTime = (iso: string): string => {
    try {
      const d = new Date(iso);
      return d.toLocaleString('zh-CN');
    } catch {
      return iso;
    }
  };

  return (
    <div className="min-h-full px-4 pb-6 pt-4 md:px-6">
      <div className="mb-5 rounded-[1.5rem] border settings-border bg-card/94 px-5 py-5 shadow-soft-card-strong backdrop-blur-sm">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-xl font-semibold tracking-tight text-foreground">日志</h1>
            <p className="text-xs leading-6 text-muted-text">查看系统运行日志与调试输出。</p>
          </div>
        </div>
      </div>

      {listError ? (
        <ApiErrorAlert
          error={listError}
          actionLabel="重试"
          onAction={() => void loadFiles()}
          className="mb-4"
        />
      ) : null}

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-[280px_1fr]">
        <aside className="lg:sticky lg:top-4 lg:self-start">
          <div className="rounded-[1.5rem] border settings-border bg-card/94 shadow-soft-card-strong backdrop-blur-sm">
            <div className="px-5 py-4">
              <h2 className="text-sm font-semibold text-foreground">日志文件</h2>
              <p className="text-xs text-muted-text">共 {files.length} 个文件</p>
            </div>
            <div className="px-3 pb-3">
              {isLoadingList ? (
                <div className="space-y-2 px-2 py-4">
                  {Array.from({ length: 4 }).map((_, i) => (
                    <div key={i} className="h-10 animate-pulse rounded-xl bg-muted/40" />
                  ))}
                </div>
              ) : files.length === 0 ? (
                <div className="px-2 py-6 text-center text-sm text-muted-text">暂无日志文件</div>
              ) : (
                <div className="flex flex-col gap-1">
                  {files.map((file) => (
                    <button
                      key={file.name}
                      type="button"
                      onClick={() => setSelectedFile(file.name)}
                      className={cn(
                        'flex w-full flex-col rounded-xl px-3 py-2.5 text-left transition-all',
                        selectedFile === file.name
                          ? 'bg-[var(--nav-active-bg)] text-[hsl(var(--primary))] font-medium'
                          : 'text-secondary-text hover:bg-hover hover:text-foreground'
                      )}
                    >
                      <span className="truncate text-sm">{file.name}</span>
                      <span className="text-xs opacity-70">
                        {formatSize(file.size)} · {formatTime(file.modifiedAt)}
                      </span>
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </aside>

        <section className="flex flex-col gap-4">
          <div className="flex flex-col rounded-[1.5rem] border settings-border bg-card/94 shadow-soft-card-strong backdrop-blur-sm">
            <div className="flex items-center justify-between px-5 py-4">
              <div className="flex items-center gap-2 min-w-0">
                <FileText className="h-4 w-4 shrink-0 text-muted-text" />
                <h2 className="truncate text-sm font-semibold text-foreground">
                  {selectedFile ?? '请选择日志文件'}
                </h2>
              </div>
              <Button
                type="button"
                variant="settings-secondary"
                size="sm"
                onClick={handleRefresh}
                disabled={!selectedFile || isLoadingContent}
                isLoading={isLoadingContent}
                loadingText="刷新中..."
              >
                <RefreshCw className="h-4 w-4" />
                刷新
              </Button>
            </div>

            {contentError ? (
              <div className="px-5 pb-4">
                <ApiErrorAlert
                  error={contentError}
                  actionLabel="重试"
                  onAction={() => void loadContent(selectedFile!)}
                />
              </div>
            ) : null}

            <div className="min-h-[400px] flex-1 px-5 pb-5">
              {!selectedFile ? (
                <EmptyState
                  title="未选择日志文件"
                  description="请在左侧选择一个日志文件以查看内容。"
                  icon={<ScrollText className="h-10 w-10" />}
                />
              ) : isLoadingContent && lines.length === 0 ? (
                <div className="flex h-64 items-center justify-center">
                  <div className="h-8 w-8 animate-spin rounded-full border-2 border-cyan/20 border-t-cyan" />
                </div>
              ) : lines.length === 0 ? (
                <EmptyState
                  title="日志为空"
                  description="当前日志文件暂无内容。"
                  icon={<FileText className="h-10 w-10" />}
                />
              ) : (
                <ScrollArea
                  className="h-[calc(100vh-14rem)] rounded-2xl border border-border/40 bg-black/5 dark:bg-white/5"
                  viewportClassName="p-4"
                >
                  <div className="space-y-0.5">
                    {lines.map((line, idx) => (
                      <div
                        key={`${selectedFile}-${idx}`}
                        className="whitespace-pre-wrap break-all font-mono text-xs leading-5 text-foreground/90"
                      >
                        {line || ' '}
                      </div>
                    ))}
                  </div>
                </ScrollArea>
              )}
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default LogsPage;
