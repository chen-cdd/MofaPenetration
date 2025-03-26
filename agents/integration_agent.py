from memory.memory_store import MemoryStore

class IntegrationAgent:
    """整合信息Agent - 负责结构化存储、生成摘要和详细报告"""
    
    def __init__(self, memory_store):
        self.memory_store = memory_store
    
    def integrate_information(self, query, search_results):
        """
        整合搜索结果信息
        
        Args:
            query: 用户查询
            search_results: 搜索结果列表
            
        Returns:
            summary: 摘要信息
            detailed_report: 详细报告
        """
        print(f"整合代理: 为查询 '{query}' 整合信息")
        
        # 结构化存储信息
        structured_data = self._structure_data(search_results)
        
        # 生成摘要
        summary = self._generate_summary(query, structured_data)
        
        # 生成详细报告
        detailed_report = self._generate_detailed_report(query, structured_data)
        
        return summary, detailed_report
    
    def _structure_data(self, search_results):
        """将搜索结果结构化"""
        # 按相关性排序
        sorted_results = sorted(
            search_results, 
            key=lambda x: x["relevance_score"], 
            reverse=True
        )
        
        # 按域名分组
        domain_groups = {}
        for result in sorted_results:
            url = result["url"]
            domain = url.split("/")[2] if len(url.split("/")) > 2 else url
            
            if domain not in domain_groups:
                domain_groups[domain] = []
            
            domain_groups[domain].append(result)
        
        # 提取关键信息
        structured_data = {
            "top_results": sorted_results[:5],
            "domain_groups": domain_groups,
            "by_relevance": {
                "high": [r for r in sorted_results if r["relevance_score"] > 0.7],
                "medium": [r for r in sorted_results if 0.4 <= r["relevance_score"] <= 0.7],
                "low": [r for r in sorted_results if r["relevance_score"] < 0.4]
            }
        }
        
        return structured_data
    
    def _generate_summary(self, query, structured_data):
        """生成摘要信息"""
        top_results = structured_data["top_results"]
        high_relevance = structured_data["by_relevance"]["high"]
        
        summary_parts = [
            f"## 查询: {query}",
            f"\n共找到 {len(structured_data['domain_groups'])} 个域名的 {sum(len(group) for group in structured_data['domain_groups'].values())} 个相关页面。",
            f"\n其中 {len(high_relevance)} 个页面与查询高度相关。"
        ]
        
        # 添加主要发现
        if top_results:
            summary_parts.append("\n\n### 主要发现:")
            for i, result in enumerate(top_results[:3], 1):
                url = result["url"]
                # 提取页面标题或使用URL
                title = self._extract_title(result["content"]) or url
                summary_parts.append(f"\n{i}. **{title}**")
                summary_parts.append(f"\n   - 相关度: {result['relevance_score']:.2f}")
                summary_parts.append(f"\n   - URL: {url}")
        
        return "\n".join(summary_parts)
    
    def _generate_detailed_report(self, query, structured_data):
        """生成详细报告"""
        report_parts = [
            f"# 详细搜索报告: {query}",
            "\n\n## 搜索路径分析"
        ]
        
        # 添加域名分组信息
        report_parts.append("\n\n## 按域名分组的结果")
        for domain, results in structured_data["domain_groups"].items():
            report_parts.append(f"\n\n### {domain} ({len(results)} 个页面)")
            
            # 按深度排序
            depth_sorted = sorted(results, key=lambda x: x["depth"])
            
            for result in depth_sorted:
                title = self._extract_title(result["content"]) or result["url"]
                report_parts.append(f"\n- **{title}** (深度: {result['depth']})")
                report_parts.append(f"\n  - URL: {result['url']}")
                report_parts.append(f"\n  - 相关度: {result['relevance_score']:.2f}")
                
                # 添加内容摘要
                summary = self._extract_content_summary(result["content"], query)
                if summary:
                    report_parts.append(f"\n  - 摘要: {summary}")
        
        # 添加高相关性内容的详细信息
        high_relevance = structured_data["by_relevance"]["high"]
        if high_relevance:
            report_parts.append("\n\n## 高相关性内容详细分析")
            
            for i, result in enumerate(high_relevance, 1):
                title = self._extract_title(result["content"]) or result["url"]
                report_parts.append(f"\n\n### {i}. {title}")
                report_parts.append(f"\n- URL: {result['url']}")
                report_parts.append(f"\n- 相关度: {result['relevance_score']:.2f}")
                report_parts.append(f"\n- 深度: {result['depth']}")
                
                # 添加详细内容分析
                analysis = self._analyze_content(result["content"], query)
                report_parts.append(f"\n\n{analysis}")
        
        return "\n".join(report_parts)
    
    def _extract_title(self, html_content):
        """从HTML内容中提取标题"""
        import re
        title_match = re.search(r"<title>(.*?)</title>", html_content, re.IGNORECASE)
        if title_match:
            return title_match.group(1)
        return None
    
    def _extract_content_summary(self, content, query, max_length=150):
        """提取内容摘要"""
        # 简单实现：提取包含查询词的段落
        import re
        
        # 移除HTML标签
        text = re.sub(r"<[^>]+>", " ", content)
        text = re.sub(r"\s+", " ", text).strip()
        
        # 查找包含查询词的段落
        query_terms = query.lower().split()
        paragraphs = text.split("\n")
        
        for term in query_terms:
            for para in paragraphs:
                if term.lower() in para.lower():
                    # 提取包含查询词的句子
                    start = max(0, para.lower().find(term.lower()) - 60)
                    end = min(len(para), start + max_length)
                    return para[start:end] + "..."
        
        # 如果没有找到包含查询词的段落，返回开头
        return text[:max_length] + "..." if len(text) > max_length else text
    
    def _analyze_content(self, content, query):
        """分析内容与查询的关系"""
        # 提取主要观点和与查询相关的信息
        # 这里可以使用更复杂的NLP技术，如命名实体识别、关键词提取等
        
        # 简单实现：提取包含查询词的段落
        import re
        
        # 移除HTML标签
        text = re.sub(r"<[^>]+>", " ", content)
        text = re.sub(r"\s+", " ", text).strip()
        
        # 分析文本
        analysis_parts = ["#### 内容分析"]
        
        # 提取关键句子
        query_terms = query.lower().split()
        sentences = re.split(r'[.!?]+', text)
        
        relevant_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            for term in query_terms:
                if term.lower() in sentence.lower():
                    relevant_sentences.append(sentence)
                    break
        
        if relevant_sentences:
            analysis_parts.append("\n\n##### 关键信息")
            for i, sentence in enumerate(relevant_sentences[:5], 1):
                analysis_parts.append(f"\n{i}. {sentence}")
        
        # 添加一些基本统计
        word_count = len(text.split())
        analysis_parts.append(f"\n\n##### 统计信息")
        analysis_parts.append(f"\n- 字数: {word_count}")
        
        # 查询词出现频率
        term_freq = {}
        for term in query_terms:
            term_freq[term] = text.lower().count(term.lower())
        
        analysis_parts.append("\n- 查询词出现频率:")
        for term, freq in term_freq.items():
            analysis_parts.append(f"\n  - {term}: {freq} 次")
        
        return "\n".join(analysis_parts)