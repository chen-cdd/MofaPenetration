import argparse
from agents.planning_agent import PlanningAgent
from agents.execution_agent import ExecutionAgent
from agents.integration_agent import IntegrationAgent
from memory.memory_store import MemoryStore
from memory.retrieval import MemoryRetrieval

def main():
    parser = argparse.ArgumentParser(description='深度搜索工具 - 模拟人类深度搜索行为')
    parser.add_argument('--query', type=str, required=True, help='搜索查询')
    parser.add_argument('--depth', type=int, default=3, help='搜索深度限制')
    parser.add_argument('--start_url', type=str, default='', help='可选的起始URL')
    args = parser.parse_args()

    # 初始化内存存储
    memory_store = MemoryStore()
    memory_retrieval = MemoryRetrieval(memory_store)
    
    # 初始化代理
    planning_agent = PlanningAgent(memory_retrieval)
    execution_agent = ExecutionAgent(memory_store)
    integration_agent = IntegrationAgent(memory_store)
    
    # 处理用户输入
    if args.start_url:
        initial_links = [args.start_url]
    else:
        # 使用搜索引擎获取初始链接
        from utils.web_scraper import get_initial_links
        initial_links = get_initial_links(args.query)
    
    # 规划搜索路径
    search_plan = planning_agent.generate_plan(args.query, initial_links, args.depth)
    
    # 执行搜索
    search_results = execution_agent.execute_plan(search_plan, args.depth)
    
    # 整合信息
    summary, detailed_report = integration_agent.integrate_information(
        args.query, search_results
    )
    
    # 输出结果
    print("\n===== 搜索摘要 =====")
    print(summary)
    
    print("\n===== 详细报告 =====")
    print(detailed_report)
    
    # 保存报告
    with open(f"search_report_{args.query.replace(' ', '_')}.md", "w", encoding="utf-8") as f:
        f.write("# 搜索报告: " + args.query + "\n\n")
        f.write("## 摘要\n\n" + summary + "\n\n")
        f.write("## 详细信息\n\n" + detailed_report)
    
    print(f"\n报告已保存至 search_report_{args.query.replace(' ', '_')}.md")

if __name__ == "__main__":
    main()