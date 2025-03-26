class MemoryRetrieval:
    """内存检索 - 从内存中检索相关信息"""
    
    def __init__(self, memory_store):
        self.memory_store = memory_store
    
    def retrieve_context(self, query, max_results=10):
        """
        检索与查询相关的上下文
        
        Args:
            query: 用户查询
            max_results: 最大结果数
            
        Returns:
            context: 相关上下文列表
        """
        # 获取所有页面
        all_pages = self.memory_store.get_all_pages()
        
        # 按相关性排序
        sorted_pages = sorted(
            all_pages, 
            key=lambda x: x["relevance_score"], 
            reverse=True
        )
        
        # 提取上下文
        context = []
        for page in sorted_pages[:max_results]:
            context.append({
                "url": page["url"],
                "content_summary": self._extract_summary(page["content"], query),
                "relevance_score": page["relevance_score"]
            })
        
        return context
    
    def retrieve_by_url(self, url):
        """通过URL检索页面"""
        return self.memory_store.get_page(url)
    
    def retrieve_similar_pages(self, url, max_results=5):
        """检索与给定URL相似的页面"""
        target_page = self.memory_store.get_page(url)
        if not target_page:
            return []
        
        # 获取所有页面
        all_pages = self.memory_store.get_all_pages()
        
        # 计算相似度
        similar_pages = []
        for page in all_pages:
            if page["url"] == url:
                continue
                
            # 计算URL相似度（简单实现：相同域名）
            target_domain = url.split("/")[2] if len(url.split("/")) > 2 else url
            page_domain = page["url"].split("/")[2] if len(page["url"].split("/")) > 2 else page["url"]
            
            domain_similarity = 1.0 if target_domain == page_domain else 0.0
            
            # 可以添加更复杂的相似度计算，如内容相似度
            
            similar_pages.append({
                "page": page,
                "similarity": domain_similarity
            })
        
        # 按相似度排序
        sorted_similar = sorted(
            similar_pages, 
            key=lambda x: x["similarity"], 
            reverse=True
        )
        
        return [item["page"] for item in sorted_similar[:max_results]]
    
    def _extract_summary(self, content, query, max_length=200):
        """从内容中提取摘要"""
        import re
        
        # 移除HTML标签
        text = re.sub(r"<[^>]+>", " ", content)
        text = re.sub(r"\s+", " ", text).strip()
        
        # 查找包含查询词的段落
        query_terms = query.lower().split()
        
        # 尝试找到包含查询词的部分
        for term in query_terms:
            term_pos = text.lower().find(term.lower())
            if term_pos >= 0:
                start = max(0, term_pos - 100)
                end = min(len(text), term_pos + 100)
                return text[start:end] + "..."
        
        # 如果没有找到，返回开头部分
        return text[:max_length] + "..." if len(text) > max_length else text