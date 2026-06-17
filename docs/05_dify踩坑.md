# 创建知识库

文件类型不支持json
分段问题 chunk切的太碎 导致商品模块 四个方法接口 检索结果仅返回第一个GET
```
商品模块
├── GET
├── POST
├── PUT
├── DELETE

被切成

Chunk1 商品模块
Chunk2 GET
Chunk3 POST
Chunk4 PUT
Chunk5 DELETE


信息密集型文档，如技术手册或研究论文，上下文很重要 
例如接口文档：直接用 分段设置 父子模式
文档结构 一个模块的内容 各个###之间不要空格
详情见最终修改版 FakeStoreAPI接口文档.md

RAG效果 = 50% 文档结构 + 30% Chunk策略 + 10% 检索配置 + 10% Prompt
```

# 搭建工作流

知识索引节点 输出result变量
LLM节点 应该通过“上下文”变量 才能得到检索结果result

官方社区直接看docs
https://forum.dify.ai