@echo off
REM ClawHub飞书智能体启动脚本（Windows）

echo ========================================
echo     ClawHub飞书智能体启动脚本
echo ========================================

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: Python 未安装
    pause
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo 安装依赖...
pip install -r requirements.txt

REM 检查环境变量
if not exist ".env" (
    echo 警告: .env 文件不存在
    echo 正在创建 .env 文件...
    copy .env.example .env
    echo 请编辑 .env 文件并配置飞书应用信息
    pause
)

REM 创建日志目录
if not exist "logs" mkdir logs

REM 启动服务
echo 启动ClawHub飞书智能体...
echo 服务地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo 按 Ctrl+C 停止服务
echo ========================================

python main.py