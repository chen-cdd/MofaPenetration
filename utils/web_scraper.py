import requests
from bs4 import BeautifulSoup
import time
import random

def get_initial_links(query, num_results=5):
    """
    使用搜索引擎获取初始链接
    
    Args:
        query: 搜索查询
        num_results: 返回结果数量
        
    Returns:
        links: 初始链接列表
    """
    print(f"获取初始链接: {query}")
    
    # 注意：实际应用中应使用搜索引擎API或遵循其robots.txt规则
    # 这里仅作为示例，实际使用时请替换为合适的实现
    
    # 使用中国境内网站作为初始链接
    mock_links = [
        f"https://www.baidu.com/s?wd={query}",
        f"https://www.zhihu.com/search?type=content&q={query}",
        f"https://s.weibo.com/weibo?q={query}",
        f"https://www.douban.com/search?q={query}",
        f"https://cn.bing.com/search?q={query}",
        f"https://www.sogou.com/web?query={query}",
        f"https://search.bilibili.com/all?keyword={query}",
        f"https://so.csdn.net/so/search?q={query}",
        f"https://www.cnki.net/kns/brief/default_result.aspx?txt_1_value1={query}",
        f"https://www.ximalaya.com/search/{query}"
    ]
    
    return mock_links[:num_results]

def scrape_webpage(url, timeout=10, max_retries=3):
    """
    抓取网页内容
    
    Args:
        url: 网页URL
        timeout: 请求超时时间（秒）
        max_retries: 最大重试次数
        
    Returns:
        content: 网页内容
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }
    
    retries = 0
    while retries < max_retries:
        try:
            # 模拟真实用户行为，添加随机延迟
            time.sleep(random.uniform(1, 3))
            
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()  # 如果响应状态码不是200，抛出异常
            
            return response.text
        except requests.exceptions.RequestException as e:
            retries += 1
            print(f"抓取 {url} 失败 (尝试 {retries}/{max_retries}): {str(e)}")
            
            if retries >= max_retries:
                # 如果达到最大重试次数，返回空内容
                return f"<html><body><p>抓取失败: {str(e)}</p></body></html>"
            
            # 指数退避策略
            time.sleep(2 ** retries)
    
    return "<html><body><p>抓取失败</p></body></html>"

def extract_links(html_content, base_url):
    """
    从HTML内容中提取链接
    
    Args:
        html_content: HTML内容
        base_url: 基础URL，用于解析相对链接
        
    Returns:
        links: 链接列表，每个链接是一个字典，包含URL和锚文本
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        text = a_tag.get_text().strip()
        
        # 处理相对链接
        if href.startswith('/'):
            # 提取域名
            from urllib.parse import urlparse
            parsed_base = urlparse(base_url)
            base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"
            href = base_domain + href
        elif not href.startswith(('http://', 'https://')):
            # 其他相对链接
            if base_url.endswith('/'):
                href = base_url + href
            else:
                href = base_url + '/' + href
        
        # 过滤掉锚点链接和JavaScript链接
        if href.startswith(('http://', 'https://')) and not href.startswith('javascript:'):
            links.append({
                "url": href,
                "text": text if text else href
            })
    
    return links