import sys
import json
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from memory.memory_store import MemoryStore

def main():
    """
    内存存储包装器 - 包装内存存储以适应DORA数据流
    """
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='内存存储包装器')
    parser.add_argument('--execution_data', type=str, help='执行数据')
    args = parser.parse_args()

    # 处理执行数据
    if args.execution_data:
        try:
            execution_data = json.loads(args.execution_data)
            search_results = execution_data.get('search_results', [])
            
            # 初始化内存存储
            memory_store = MemoryStore()
            
            # 存储搜索结果
            for result in search_results:
                memory_store.store(result)
            
            # 获取域名统计
            domain_stats = memory_store.get_domain_statistics()
            
            # 输出内存存储状态
            output_data = {
                'stored_pages': len(memory_store.pages),
                'domain_stats': domain_stats,
                'message': f'已存储 {len(memory_store.pages)} 个页面'
            }
            print(json.dumps(output_data), file=sys.stdout)
            
            # 输出存储状态
            status_data = {
                'status': 'storage_completed',
                'pages_count': len(memory_store.pages)
            }
            print(json.dumps(status_data), file=sys.stderr)
            
        except Exception as e:
            error_data = {
                'error': str(e),
                'message': '内存存储处理失败'
            }
            print(json.dumps(error_data), file=sys.stdout)
            print(json.dumps({'status': 'error', 'error': str(e)}), file=sys.stderr)

if __name__ == "__main__":
    main()