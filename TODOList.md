# 需要修改的内容
## 拉取股票列表
实际情况是：

有一个手动拉取脚本：scripts/fetch_tushare_stock_list.py

从 Tushare Pro API 获取 A 股、港股、美股全量列表
需要你在 .env 里配置 TUSHARE_TOKEN，并且账号有对应积分
执行后会输出到 data/stock_list_a.csv、stock_list_hk.csv、stock_list_us.csv
不是自动定时任务：.github/workflows/ 里没有引用这个脚本，说明是手动执行的

当前仓库里只有最终产物：stocks.index.json 这个 3MB 的静态文件已经生成好了并提交了，所以 CSV 中间文件不需要留在本地

一句话：这份索引是有人手动跑 fetch_tushare_stock_list.py 从 Tushare 拉取，再跑 generate_index_from_csv.py 生成的，不是定时自动从网上更新的。如果股票列表变陈旧了，需要手动重跑这两个脚本。

改进：
1. 从东方财富拉。
优先级低


