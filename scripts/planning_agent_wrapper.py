import sys
import json
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from agents.planning_agent import PlanningAgent
from memory.retrieval import MemoryRetrieval
from memory.memory_store import MemoryStore
from utils.web_scraper import get_initial_links

def main():
    """
    规划代理包装器 - 包装规划代理以适应DORA数据流
    """
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='规划代理包装器')
    parser.add_argument('--task', type=str, help='任务数据')
    parser.add_argument('--memory_retrieval_out', type=str, help='内存检索输出')
    args = parser.parse_args()

    # 处理任务数据
    if args.task:
        try:
            task_data = json.loads(args.task)
            query = task_data.get('query', '')
            depth = task_data.get('depth', 3)
            start_url = task_data.get('start_url', '')
            
            # 初始化内存存储和检索
            memory_store = MemoryStore()
            memory_retrieval = MemoryRetrieval(memory_store)
            
            # 初始化规划代理
            planning_agent = PlanningAgent(memory_retrieval)
            
            # 获取初始链接
            if start_url:
                initial_links = [start_url]
            else:
                initial_links = get_initial_links(query)
            
            # 生成搜索计划
            search_plan = planning_agent.generate_plan(query, initial_links, depth)
            
            # 输出搜索计划
            output_data = {
                'search_plan': search_plan,
                'message': f'已为查询 "{query}" 生成搜索计划，包含 {len(search_plan["paths"])} 个路径'
            }
            print(json.dumps(output_data), file=sys.stdout)
            
            # 输出内部状态
            int_output = {
                'status': 'planning_completed',
                'paths_count': len(search_plan["paths"])
            }
            print(json.dumps(int_output), file=sys.stderr)
            
        except Exception as e:
            error_data = {
                'error': str(e),
                'message': '规划代理处理失败'
            }
            print(json.dumps(error_data), file=sys.stdout)
            print(json.dumps({'status': 'error', 'error': str(e)}), file=sys.stderr)

if __name__ == "__main__":
    main()