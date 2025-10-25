# 🩺 肺结节诊断多智能体系统

基于LangGraph实现的胸外科医院肺结节诊断多智能体协同系统，完整复现临床诊断路径。

## 🎯 项目概述

本项目通过多智能体协同合作，完整复现肺结节诊断的临床路径，并实现自动化、智能化升级。系统集成了CT分割模型，使用LangGraph框架构建了六类医生智能体的协作网络。

## 🏥 智能体角色

- **放射科医生**: CT影像分析和Lung-RADS分类
- **呼吸科医生**: 内科诊断和治疗方案
- **病理科医生**: 病理学分析和确诊
- **胸外科医生**: 外科手术评估
- **放射肿瘤科医生**: 放疗方案制定
- **康复科医生**: 术后康复指导

## 🛠️ 技术栈

- **核心框架**: LangGraph, LangChain
- **AI模型**: DeepSeek API, CT分割模型
- **医学工具**: pydicom, SimpleITK, nnUNet
- **数据存储**: SQLite/PostgreSQL
- **API服务**: FastAPI

## 📁 项目结构
```
lung_agent/
├── lung_agent.py          # 主程序入口
├── tools.py               # 工具函数（SerpAPI等）
├── prompts.py             # 智能体提示词
├── requirements.txt       # 依赖包列表
├── .env.example          # 环境变量模板
└── README.md
```

# 项目说明

## 🚀 快速开始

### 环境配置

1. 克隆项目
```bash
git clone https://github.com/yourusername/lung_agent.git
cd lung_agent
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑.env文件，添加您的API密钥
```

### 运行系统

```bash
python lung_agent.py
```

## 📊 功能特性

- ✅ 多智能体协同诊断
- ✅ CT影像自动分析
- ✅ Lung-RADS自动分类
- ✅ 临床路径完整复现
- ✅ 实时医学知识检索
- ✅ 结构化诊断报告生成

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

## 📄 许可证

MIT License