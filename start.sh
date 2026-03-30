#!/bin/bash
# ClawHub飞书智能体启动脚本

echo "========================================"
echo "    ClawHub飞书智能体启动脚本"
echo "========================================"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: Python3 未安装"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
if [ "$OSTYPE" = "msys" ] || [ "$OSTYPE" = "win32" ]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt

# 检查环境变量
if [ ! -f ".env" ]; then
    echo "警告: .env 文件不存在"
    echo "正在创建 .env 文件..."
    cp .env.example .env
    echo "请编辑 .env 文件并配置飞书应用信息"
    read -p "按回车键继续..." 
fi

# 创建日志目录
mkdir -p logs

# 启动服务
echo "启动ClawHub飞书智能体..."
echo "服务地址: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo "按 Ctrl+C 停止服务"
echo "========================================"

python main.py