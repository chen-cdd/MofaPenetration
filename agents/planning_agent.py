from memory.retrieval import MemoryRetrieval
from utils.link_analyzer import analyze_links, prioritize_links

class PlanningAgent:
    """规划代理 - 负责链接预处理、路径生成和优化"""
    
    def __init__(self, memory_retrieval):
        self.memory_retrieval = memory_retrieval
    
    def generate_plan(self, query, initial_links, max_depth):
        """
        生成搜索计划
        
        Args:
            query: 用户查询
            initial_links: 初始链接列表
            max_depth: 最大搜索深度
            
        Returns:
            search_plan: 搜索计划字典
        """
        print(f"规划代理: 为查询 '{query}' 生成搜索计划")
        
        # 预处理链接
        processed_links = self._preprocess_links(initial_links)
        
        # 生成搜索路径
        search_paths = self._generate_paths(query, processed_links, max_depth)
        
        # 优化搜索路径
        optimized_paths = self._optimize_paths(search_paths, query)
        
        return {
            "query": query,
            "max_depth": max_depth,
            "paths": optimized_paths
        }
    
    def _preprocess_links(self, links):
        """预处理链接 - 去重、验证有效性等"""
        # 去除重复链接
        unique_links = list(set(links))
        
        # 验证链接有效性
        valid_links = []
        for link in unique_links:
            # 这里可以添加链接验证逻辑
            valid_links.append(link)
            
        return valid_links
    
    def _generate_paths(self, query, links, max_depth):
        """生成初始搜索路径"""
        # 分析链接与查询的相关性
        analyzed_links = analyze_links(links, query)
        
        # 构建搜索路径
        search_paths = []
        for link in analyzed_links:
            path = {
                "start_url": link,
                "relevance_score": link["relevance_score"],
                "max_depth": max_depth,
                "exploration_strategy": "breadth_first"  # 或 depth_first
            }
            search_paths.append(path)
        
        return search_paths
    
    def _optimize_paths(self, paths, query):
        """优化搜索路径 - 基于相关性和多样性"""
        # 根据相关性排序
        sorted_paths = sorted(paths, key=lambda x: x["relevance_score"], reverse=True)
        
        # 确保路径多样性
        optimized_paths = []
        domains_included = set()
        
        for path in sorted_paths:
            domain = path["start_url"].split("/")[2] if len(path["start_url"].split("/")) > 2 else path["start_url"]
            
            # 如果已经包含了太多同一域名的路径，降低其优先级
            if domains_included.count(domain) < 2:
                optimized_paths.append(path)
                domains_included.add(domain)
        
        # 如果优化后的路径太少，添加一些原始路径
        if len(optimized_paths) < 5 and len(sorted_paths) > len(optimized_paths):
            for path in sorted_paths:
                if path not in optimized_paths:
                    optimized_paths.append(path)
                    if len(optimized_paths) >= 5:
                        break
        
        return optimized_paths
    
    def update_plan(self, execution_feedback):
        """根据执行反馈更新计划"""
        # 根据执行代理的反馈调整搜索计划
        updated_paths = []
        
        for path_feedback in execution_feedback:
            if path_feedback["status"] == "success":
                # 如果成功，可能需要深入探索
                if path_feedback["found_valuable_info"]:
                    # 添加更多相关链接到搜索路径
                    pass
            elif path_feedback["status"] == "failed":
                # 如果失败，尝试替代路径
                pass
        
        return updated_paths