import sys
import json
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from agents.execution_agent import ExecutionAgent
from memory.memory_store import MemoryStore

def main():
    """
    执行代理包装器 - 包装执行代理以适应DORA数据流
    """
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='执行代理包装器')
    parser.add_argument('--task', type=str, help='任务数据')
    parser.add_argument('--memory_store_out', type=str, help='内存存储输出')
    args = parser.parse_args()

    # 处理任务数据
    if args.task:
        try:
            task_data = json.loads(args.task)
            search_plan = task_data.get('search_plan', {})
            
            # 初始化内存存储
            memory_store = MemoryStore()
            
            # 初始化执行代理
            execution_agent = ExecutionAgent(memory_store)
            
            # 执行搜索计划
            max_depth = search_plan.get('max_depth', 3)
            search_results = execution_agent.execute_plan(search_plan, max_depth)
            
            # 输出搜索结果
            output_data = {
                'search_results': search_results,
                'message': f'已执行搜索计划，获取了 {len(search_results)} 个结果'
            }
            print(json.dumps(output_data), file=sys.stdout)
            
            # 输出执行状态
            status_data = {
                'status': 'execution_completed',
                'results_count': len(search_results)
            }
            print(json.dumps(status_data), file=sys.stderr)
            
        except Exception as e:
            error_data = {
                'error': str(e),
                'message': '执行代理处理失败'
            }
            print(json.dumps(error_data), file=sys.stdout)
            print(json.dumps({'status': 'error', 'error': str(e)}), file=sys.stderr)

if __name__ == "__main__":
    main()