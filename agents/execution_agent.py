from utils.web_scraper import scrape_webpage, extract_links
from memory.memory_store import MemoryStore

class ExecutionAgent:
    """执行代理 - 负责执行抓取任务和动态调整"""
    
    def __init__(self, memory_store):
        self.memory_store = memory_store
    
    def execute_plan(self, search_plan, max_depth):
        """
        执行搜索计划
        
        Args:
            search_plan: 由规划代理生成的搜索计划
            max_depth: 最大搜索深度
            
        Returns:
            search_results: 搜索结果列表
        """
        print(f"执行代理: 执行搜索计划，最大深度 {max_depth}")
        
        search_results = []
        execution_feedback = []
        
        # 对每个搜索路径执行抓取
        for path in search_plan["paths"]:
            start_url = path["start_url"]
            print(f"  开始抓取: {start_url}")
            
            # 执行单个路径的抓取
            path_results, path_feedback = self._execute_path(
                start_url, 
                search_plan["query"], 
                path["max_depth"]
            )
            
            search_results.extend(path_results)
            execution_feedback.append(path_feedback)
            
            # 将结果存入内存
            for result in path_results:
                self.memory_store.store(result)
        
        return search_results
    
    def _execute_path(self, start_url, query, max_depth):
        """执行单个路径的抓取任务"""
        results = []
        visited = set()
        to_visit = [(start_url, 0)]  # (url, depth)
        
        path_feedback = {
            "start_url": start_url,
            "pages_visited": 0,
            "valuable_pages": 0,
            "status": "in_progress",
            "found_valuable_info": False
        }
        
        while to_visit and to_visit[0][1] <= max_depth:
            url, depth = to_visit.pop(0)
            
            if url in visited:
                continue
                
            visited.add(url)
            path_feedback["pages_visited"] += 1
            
            try:
                # 抓取网页
                content = scrape_webpage(url)
                
                # 评估内容相关性
                relevance_score = self._evaluate_relevance(content, query)
                
                # 存储结果
                result = {
                    "url": url,
                    "depth": depth,
                    "content": content,
                    "relevance_score": relevance_score,
                    "timestamp": self._get_timestamp()
                }
                
                results.append(result)
                
                # 如果内容相关，标记为有价值
                if relevance_score > 0.6:
                    path_feedback["valuable_pages"] += 1
                    path_feedback["found_valuable_info"] = True
                
                # 如果未达到最大深度，提取链接并添加到待访问列表
                if depth < max_depth:
                    links = extract_links(content, url)
                    # 按相关性排序链接
                    sorted_links = self._sort_links_by_relevance(links, query)
                    
                    # 添加到待访问列表
                    for link in sorted_links[:5]:  # 限制每页最多追踪5个链接
                        to_visit.append((link, depth + 1))
            
            except Exception as e:
                print(f"  抓取 {url} 时出错: {str(e)}")
        
        path_feedback["status"] = "success"
        return results, path_feedback
    
    def _evaluate_relevance(self, content, query):
        """评估内容与查询的相关性"""
        # 简单实现：检查查询词在内容中的出现频率
        query_terms = query.lower().split()
        content_lower = content.lower()
        
        score = 0
        for term in query_terms:
            if term in content_lower:
                score += content_lower.count(term) / len(content_lower) * 100
        
        # 归一化分数到0-1范围
        return min(score, 1.0)
    
    def _sort_links_by_relevance(self, links, query):
        """按与查询的相关性对链接进行排序"""
        # 简单实现：检查查询词在链接URL和锚文本中的出现情况
        scored_links = []
        query_terms = query.lower().split()
        
        for link in links:
            url = link["url"].lower()
            text = link.get("text", "").lower()
            
            score = 0
            for term in query_terms:
                if term in url:
                    score += 0.5
                if term in text:
                    score += 1.0
            
            link["relevance_score"] = score
            scored_links.append(link)
        
        # 按分数降序排序
        return sorted(scored_links, key=lambda x: x["relevance_score"], reverse=True)
    
    def _get_timestamp(self):
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()