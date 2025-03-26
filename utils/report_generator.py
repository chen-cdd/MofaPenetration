import os
from datetime import datetime

def generate_markdown_report(query, summary, detailed_report, search_results):
    """
    生成Markdown格式的报告
    
    Args:
        query: 用户查询
        summary: 摘要信息
        detailed_report: 详细报告
        search_results: 搜索结果
        
    Returns:
        report_path: 报告文件路径
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"search_report_{query.replace(' ', '_')}_{timestamp}.md"
    
    report_content = [
        f"# 深度搜索报告: {query}",
        f"\n\n*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        f"\n\n## 摘要",
        f"\n\n{summary}",
        f"\n\n## 详细信息",
        f"\n\n{detailed_report}",
        f"\n\n## 搜索统计",
        f"\n\n- 查询: {query}",
        f"\n- 检索到的页面数: {len(search_results)}",
        f"\n- 高相关性页面数: {len([r for r in search_results if r.get('relevance_score', 0) > 0.7])}"
    ]
    
    # 添加域名统计
    domains = {}
    for result in search_results:
        url = result["url"]
        domain = url.split("/")[2] if len(url.split("/")) > 2 else url
        
        if domain not in domains:
            domains[domain] = 0
        domains[domain] += 1
    
    report_content.append("\n\n### 域名分布")
    for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True):
        report_content.append(f"\n- {domain}: {count} 个页面")
    
    # 写入文件
    report_path = os.path.join(os.getcwd(), filename)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("".join(report_content))
    
    return report_path

def generate_html_report(query, summary, detailed_report, search_results):
    """
    生成HTML格式的报告
    
    Args:
        query: 用户查询
        summary: 摘要信息
        detailed_report: 详细报告
        search_results: 搜索结果
        
    Returns:
        report_path: 报告文件路径
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"search_report_{query.replace(' ', '_')}_{timestamp}.html"
    
    # 转换Markdown为HTML
    import markdown
    summary_html = markdown.markdown(summary)
    detailed_report_html = markdown.markdown(detailed_report)
    
    # 生成域名统计图表数据
    domains = {}
    for result in search_results:
        url = result["url"]
        domain = url.split("/")[2] if len(url.split("/")) > 2 else url
        
        if domain not in domains:
            domains[domain] = 0
        domains[domain] += 1
    
    domain_data = ", ".join([f"['{domain}', {count}]" for domain, count in domains.items()])
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>深度搜索报告: {query}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; color: #333; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .summary {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .details {{ margin-bottom: 30px; }}
        .statistics {{ display: flex; flex-wrap: wrap; }}
        .stat-box {{ background-color: #e9ecef; padding: 15px; margin: 10px; border-radius: 5px; flex: 1; min-width: 200px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
    </style>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
        google.charts.load('current', {{'packages':['corechart']}});
        google.charts.setOnLoadCallback(drawChart);
        
        function drawChart() {{
            var data = google.visualization.arrayToDataTable([
                ['Domain', 'Pages'],
                {domain_data}
            ]);
            
            var options = {{
                title: '域名分布',
                pieHole: 0.4,
            }};
            
            var chart = new google.visualization.PieChart(document.getElementById('domain_chart'));
            chart.draw(data, options);
        }}
    </script>
</head>
<body>
    <div class="container">
        <h1>深度搜索报告: {query}</h1>
        <p><em>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
        
        <h2>摘要</h2>
        <div class="summary">
            {summary_html}
        </div>
        
        <h2>详细信息</h2>
        <div class="details">
            {detailed_report_html}
        </div>
        
        <h2>搜索统计</h2>
        <div class="statistics">
            <div class="stat-box">
                <h3>基本统计</h3>
                <p>查询: {query}</p>
                <p>检索到的页面数: {len(search_results)}</p>
                <p>高相关性页面数: {len([r for r in search_results if r.get('relevance_score', 0) > 0.7])}</p>
            </div>
            
            <div class="stat-box">
                <h3>域名分布</h3>
                <div id="domain_chart" style="width: 100%; height: 300px;"></div>
            </div>
        </div>
        
        <h2>搜索结果列表</h2>
        <table>
            <tr>
                <th>URL</th>
                <th>相关性</th>
                <th>深度</th>
            </tr>
"""
    
    # 添加搜索结果表格
    for result in sorted(search_results, key=lambda x: x.get('relevance_score', 0), reverse=True):
        html_content += f"""
            <tr>
                <td><a href="{result['url']}" target="_blank">{result['url']}</a></td>
                <td>{result.get('relevance_score', 0):.2f}</td>
                <td>{result.get('depth', 'N/A')}</td>
            </tr>"""
    
    html_content += """
        </table>
    </div>
</body>
</html>
"""
    
    # 写入文件
    report_path = os.path.join(os.getcwd(), filename)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return report_path