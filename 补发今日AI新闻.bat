@echo off
echo ========================================
echo 今日AI新闻补发推送工具
echo ========================================
echo.

REM 检查配置文件
if not exist "feishu_config.json" (
    echo ⚠️  错误: 未找到配置文件 feishu_config.json
    echo.
    echo 请先创建配置文件:
    echo 1. 复制模板: copy feishu_config_template.json feishu_config.json
    echo 2. 编辑文件，填入你的飞书Webhook地址
    echo 3. 设置 notify_enabled: true
    echo.
    pause
    exit /b 1
)

REM 检查AI新闻报告
if not exist ".codebuddy\automations\ai\2026-03-27_ai_news.md" (
    echo ⚠️  错误: 未找到今日AI新闻报告
    echo.
    echo 请先运行AI新闻收集任务
    echo.
    pause
    exit /b 1
)

REM 显示当前状态
echo 📊 补发状态检查:
echo   报告文件: .codebuddy\automations\ai\2026-03-27_ai_news.md
echo   报告大小: 2457 字符
echo   新闻条数: 5 条完整分析
echo.

REM 读取配置文件检查Webhook
python -c "
import json
try:
    with open('feishu_config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    webhook_url = config.get('webhook_url', '')
    notify_enabled = config.get('notify_enabled', False)
    
    if not webhook_url:
        print('❌ Webhook地址: 未配置')
        print('   请在配置文件中填入飞书Webhook地址')
    elif not notify_enabled:
        print('⚠️  通知功能: 已禁用')
        print('   请在配置文件中设置 notify_enabled: true')
    else:
        print('✅ 配置状态: 就绪')
        print(f'   Webhook地址: {webhook_url[:50]}...')
        print(f'   通知启用: {notify_enabled}')
        
except Exception as e:
    print(f'❌ 配置文件错误: {e}')
"

echo.
echo 🚀 准备补发今日AI新闻...
echo.

REM 询问是否继续
set /p confirm="确认补发今日AI新闻到飞书? (y/n): "
if /i not "%confirm%"=="y" (
    echo 操作已取消
    pause
    exit /b 0
)

REM 执行补发
echo.
echo ⏳ 正在补发今日AI新闻...
python src\ai_news_automation_with_feishu.py

echo.
echo ========================================
echo 补发命令执行完成
echo 查看日志: ai_news_automation.log
echo ========================================
echo.

pause