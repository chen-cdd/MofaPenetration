import sys
import json
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from memory.memory_store import MemoryStore
from memory.retrieval import MemoryRetrieval

def main():
    """
    内存检索包装器 - 包装内存检索以适应DORA数据流
    """
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='内存检索包装器')
    parser.add_argument('--query_data', type=str, help='查询数据')
    parser.add_argument('--memory_store_out', type=str, help='内存存储输出')
    args = parser.parse_args()

    # 处理查询数据
    if args.query_data:
        try:
            query_data = json.loads(args.query_data)
            query = query_data.get('query', '')
            
            # 初始化内存存储和检索
            memory_store = MemoryStore()
            memory_retrieval = MemoryRetrieval(memory_store)
            
            # 如果有内存存储输出，处理它
            if args.memory_store_out:
                try:
                    memory_data = json.loads(args.memory_store_out)
                    # 这里可以添加处理内存数据的逻辑
                except json.JSONDecodeError:
                    print("无法解析内存存储输出", file=sys.stderr)
            
            # 检索相关上下文
            context = memory_retrieval.retrieve_context(query)
            
            # 输出检索结果
            output_data = {
                'context': context,
                'message': f'已检索与查询 "{query}" 相关的上下文，找到 {len(context)} 个相关项'
            }
            print(json.dumps(output_data), file=sys.stdout)
            
        except Exception as e:
            error_data = {
                'error': str(e),
                'message': '内存检索处理失败'
            }
            print(json.dumps(error_data), file=sys.stdout)

if __name__ == "__main__":
    main()