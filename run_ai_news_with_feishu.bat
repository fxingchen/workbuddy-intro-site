@echo off
echo ========================================
echo AI新闻自动化（含飞书通知）启动脚本
echo ========================================
echo.

REM 设置Python路径（根据你的环境调整）
set PYTHON_PATH=python

REM 检查配置文件是否存在
if not exist "feishu_config.json" (
    echo ⚠️  警告: 未找到配置文件 feishu_config.json
    echo.
    echo 请执行以下步骤:
    echo 1. 复制配置文件模板: copy feishu_config_template.json feishu_config.json
    echo 2. 编辑 feishu_config.json，填入你的飞书Webhook地址
    echo 3. 重新运行此脚本
    echo.
    pause
    exit /b 1
)

REM 运行AI新闻自动化
echo 正在启动AI新闻自动化流程...
echo.

%PYTHON_PATH% src\ai_news_automation_with_feishu.py

echo.
echo ========================================
echo 自动化流程执行完成
echo 查看详细日志: ai_news_automation.log
echo ========================================
echo.

REM 等待用户查看结果
pause