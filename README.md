# OpenReview 搜索批量下载+批量总结分析
## crawl_pdf.py
输入openreview搜索的关键词search_key自动爬取搜索结果pdf存在save
_dir下
``` bash
python crawl_pdf.py search_key save_dir
```

## analysis.py
将论文传到讯飞论文分析助手上分析，分析结果保存在analysis.csv
``` bash
python analysis.py username password crawl.csv
```
讯飞分析空间上限是300M，如果满了需要手动删除(回收站也要删除)


## TODO
#### analysis
- [ ] 上传和分析分开
- [ ] 支持按期刊下载
- [ ] 讯飞分析无结果重新分析
- [ ] 自动删除讯飞空间


#### crawl_pdf
- [ ] 添加时间、期刊