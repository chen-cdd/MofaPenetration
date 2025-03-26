import sys
import json
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from agents.integration_agent import IntegrationAgent
from memory.memory_store import MemoryStore
from utils.report_generator import generate_markdown_report, generate_html_report

def main():
    """
    整合代理包装器 - 包装整合代理以适应DORA数据流
    """
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='整合代理包装器')
    parser.add_argument('--task', type=str, help='任务数据')
    parser.add_argument('--memory_store_out', type=str, help='内存存储输出')
    args = parser.parse_args()

    # 处理任务数据
    if args.task:
        try:
            task_data = json.loads(args.task)
            search_results = task_data.get('search_results', [])
            
            # 从第一个结果中提取查询
            query = ""
            if search_results and len(search_results) > 0:
                first_result = search_results[0]
                if 'query' in first_result:
                    query = first_result['query']
            
            # 初始化内存存储
            memory_store = MemoryStore()
            
            # 将搜索结果存入内存
            for result in search_results:
                memory_store.store(result)
            
            # 初始化整合代理
            integration_agent = IntegrationAgent(memory_store)
            
            # 整合信息
            summary, detailed_report = integration_agent.integrate_information(query, search_results)
            
            # 生成报告
            markdown_path = generate_markdown_report(query, summary, detailed_report, search_results)
            html_path = generate_html_report(query, summary, detailed_report, search_results)
            
            # 输出整合结果
            output_data = {
                'summary': summary,
                'report_path': {
                    'markdown': markdown_path,
                    'html': html_path
                },
                'message': f'已整合搜索结果，生成了摘要和详细报告'
            }
            print(json.dumps(output_data), file=sys.stdout)
            
            # 输出报告状态
            status_data = {
                'status': 'integration_completed',
                'report_generated': True
            }
            print(json.dumps(status_data), file=sys.stderr)
            
        except Exception as e:
            error_data = {
                'error': str(e),
                'message': '整合代理处理失败'
            }
            print(json.dumps(error_data), file=sys.stdout)
            print(json.dumps({'status': 'error', 'error': str(e)}), file=sys.stderr)

if __name__ == "__main__":
    main()