from urllib.parse import urlparse
import re

def analyze_links(links, query):
    """
    分析链接与查询的相关性
    
    Args:
        links: 链接列表
        query: 用户查询
        
    Returns:
        analyzed_links: 带有相关性分数的链接列表
    """
    query_terms = query.lower().split()
    analyzed_links = []
    
    for link in links:
        # 如果链接是字符串，转换为字典格式
        if isinstance(link, str):
            link_obj = {"url": link}
        else:
            link_obj = link
        
        url = link_obj["url"]
        text = link_obj.get("text", "")
        
        # 计算相关性分数
        relevance_score = calculate_relevance(url, text, query_terms)
        
        # 添加域名信息
        domain = extract_domain(url)
        
        analyzed_links.append({
            "url": url,
            "text": text,
            "domain": domain,
            "relevance_score": relevance_score
        })
    
    return analyzed_links

def prioritize_links(analyzed_links, max_links_per_domain=2):
    """
    优先考虑多样性和相关性高的链接
    
    Args:
        analyzed_links: 带有相关性分数的链接列表
        max_links_per_domain: 每个域名最多选择的链接数
        
    Returns:
        prioritized_links: 优先级排序后的链接列表
    """
    # 按相关性排序
    sorted_links = sorted(analyzed_links, key=lambda x: x["relevance_score"], reverse=True)
    
    # 按域名分组
    domain_groups = {}
    for link in sorted_links:
        domain = link["domain"]
        if domain not in domain_groups:
            domain_groups[domain] = []
        domain_groups[domain].append(link)
    
    # 从每个域名中选择最相关的链接
    prioritized_links = []
    for domain, links in domain_groups.items():
        prioritized_links.extend(links[:max_links_per_domain])
    
    # 再次按相关性排序
    prioritized_links = sorted(prioritized_links, key=lambda x: x["relevance_score"], reverse=True)
    
    return prioritized_links

def calculate_relevance(url, text, query_terms):
    """
    计算链接与查询的相关性分数
    
    Args:
        url: 链接URL
        text: 链接文本
        query_terms: 查询词列表
        
    Returns:
        relevance_score: 相关性分数 (0-1)
    """
    url_lower = url.lower()
    text_lower = text.lower()
    
    score = 0.0
    
    # 检查URL中的查询词
    for term in query_terms:
        if term in url_lower:
            # URL路径中的查询词比查询参数中的更重要
            path = urlparse(url).path.lower()
            if term in path:
                score += 0.3
            else:
                score += 0.1
    
    # 检查锚文本中的查询词
    for term in query_terms:
        if term in text_lower:
            score += 0.5
    
    # 检查完整查询
    full_query = " ".join(query_terms)
    if full_query in text_lower:
        score += 0.5
    
    # 归一化分数到0-1范围
    return min(score, 1.0)

def extract_domain(url):
    """
    从URL中提取域名
    
    Args:
        url: 链接URL
        
    Returns:
        domain: 域名
    """
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    # 移除www前缀
    if domain.startswith('www.'):
        domain = domain[4:]
    
    return domain

def is_relevant_url(url, query_terms):
    """
    判断URL是否与查询相关
    
    Args:
        url: 链接URL
        query_terms: 查询词列表
        
    Returns:
        is_relevant: 是否相关
    """
    # 排除常见的无关链接
    excluded_patterns = [
        r'/login', r'/signup', r'/register',
        r'/privacy', r'/terms', r'/about',
        r'/contact', r'/help', r'/faq',
        r'/cart', r'/checkout', r'/account'
    ]
    
    for pattern in excluded_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return False
    
    # 检查URL是否包含查询词
    url_lower = url.lower()
    for term in query_terms:
        if term in url_lower:
            return True
    
    # 默认情况下，认为URL可能相关
    return True