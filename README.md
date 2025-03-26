# MofaPenetration - 深度搜索工具

MofaPenetration 是一个基于 MOFA 框架的深度搜索工具，旨在解决当前 AI 搜索的一个痛点：缺乏像人类一样逐步深入挖掘信息的能力。该工具通过模拟人类点开链接、层层深入的行为，并结合用户可控的深度限制，为用户提供更细致、更全面的搜索体验。

## 功能特点

- **深度搜索**：模拟人类浏览行为，层层深入探索相关内容
- **智能规划**：根据查询内容智能规划搜索路径
- **动态调整**：根据搜索过程中的发现动态调整搜索策略
- **结构化输出**：将搜索结果整合为结构化的摘要和详细报告
- **可控深度**：用户可以设置搜索深度限制，平衡搜索广度和深度

## 系统架构

MofaPenetration 由以下几个主要组件构成：

1. **用户输入处理**：处理用户查询和参数设置
2. **初始链接检索**：获取搜索的起始点
3. **规划代理**：负责链接预处理、路径生成和优化
4. **执行代理**：负责执行抓取任务和动态调整
5. **记忆模块**：存储和检索抓取的内容
6. **整合信息代理**：负责结构化存储、生成摘要和详细报告

## 使用方法

```bash
python app.py --query "你的搜索查询" --depth 3 --start_url "https://example.com"