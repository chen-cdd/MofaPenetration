import sys
import json
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

def main():
    """
    用户终端 - 处理用户输入并与其他代理交互
    """
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='用户终端')
    parser.add_argument('--data', type=str, help='输入数据')
    parser.add_argument('--planning_agent_out', type=str, help='规划代理输出')
    parser.add_argument('--execution_agent_out', type=str, help='执行代理输出')
    parser.add_argument('--integration_agent_out', type=str, help='整合代理输出')
    args = parser.parse_args()

    # 处理输入数据
    if args.data:
        try:
            input_data = json.loads(args.data)
            query = input_data.get('query', '')
            depth = input_data.get('depth', 3)
            start_url = input_data.get('start_url', '')
            
            # 输出任务数据给规划代理
            task_data = {
                'query': query,
                'depth': depth,
                'start_url': start_url
            }
            print(json.dumps(task_data), file=sys.stdout)
            
            # 输出内部状态
            int_output = {
                'status': 'processing',
                'message': f'正在处理查询: {query}'
            }
            print(json.dumps(int_output), file=sys.stderr)
            
        except json.JSONDecodeError:
            print(json.dumps({'error': '无效的JSON输入'}), file=sys.stderr)
    
    # 处理规划代理输出
    if args.planning_agent_out:
        try:
            planning_data = json.loads(args.planning_agent_out)
            print(f"规划代理输出: {planning_data.get('message', '')}", file=sys.stderr)
        except json.JSONDecodeError:
            print("无法解析规划代理输出", file=sys.stderr)
    
    # 处理执行代理输出
    if args.execution_agent_out:
        try:
            execution_data = json.loads(args.execution_agent_out)
            print(f"执行代理输出: {execution_data.get('message', '')}", file=sys.stderr)
        except json.JSONDecodeError:
            print("无法解析执行代理输出", file=sys.stderr)
    
    # 处理整合代理输出
    if args.integration_agent_out:
        try:
            integration_data = json.loads(args.integration_agent_out)
            
            # 输出最终结果
            result = {
                'summary': integration_data.get('summary', ''),
                'report_path': integration_data.get('report_path', ''),
                'status': 'completed'
            }
            print(json.dumps(result), file=sys.stdout)
            
        except json.JSONDecodeError:
            print("无法解析整合代理输出", file=sys.stderr)

if __name__ == "__main__":
    main()