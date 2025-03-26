class MemoryStore:
    """内存存储 - 存储抓取的网页内容和搜索状态"""
    
    def __init__(self):
        self.pages = {}  # 存储网页内容
        self.visited_urls = set()  # 已访问的URL
        self.url_metadata = {}  # URL元数据
    
    def store(self, page_data):
        """
        存储页面数据
        
        Args:
            page_data: 包含页面信息的字典
        """
        url = page_data["url"]
        self.pages[url] = page_data
        self.visited_urls.add(url)
        
        # 存储元数据
        self.url_metadata[url] = {
            "depth": page_data["depth"],
            "relevance_score": page_data["relevance_score"],
            "timestamp": page_data["timestamp"]
        }
    
    def get_page(self, url):
        """获取页面内容"""
        return self.pages.get(url)
    
    def get_all_pages(self):
        """获取所有页面"""
        return list(self.pages.values())
    
    def get_pages_by_relevance(self, min_score=0.0):
        """按相关性获取页面"""
        return [
            page for page in self.pages.values() 
            if page["relevance_score"] >= min_score
        ]
    
    def get_pages_by_depth(self, depth):
        """获取特定深度的页面"""
        return [
            page for page in self.pages.values() 
            if page["depth"] == depth
        ]
    
    def is_url_visited(self, url):
        """检查URL是否已访问"""
        return url in self.visited_urls
    
    def get_domain_statistics(self):
        """获取域名统计信息"""
        domain_stats = {}
        
        for url in self.pages:
            domain = url.split("/")[2] if len(url.split("/")) > 2 else url
            
            if domain not in domain_stats:
                domain_stats[domain] = {
                    "count": 0,
                    "avg_relevance": 0,
                    "max_depth": 0
                }
            
            stats = domain_stats[domain]
            stats["count"] += 1
            stats["avg_relevance"] += self.url_metadata[url]["relevance_score"]
            stats["max_depth"] = max(stats["max_depth"], self.url_metadata[url]["depth"])
        
        # 计算平均相关性
        for domain in domain_stats:
            if domain_stats[domain]["count"] > 0:
                domain_stats[domain]["avg_relevance"] /= domain_stats[domain]["count"]
        
        return domain_stats