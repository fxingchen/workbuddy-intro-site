#!/bin/bash

echo "========================================"
echo "AI新闻自动化（含飞书通知）启动脚本"
echo "========================================"
echo ""

# 设置Python路径（根据你的环境调整）
PYTHON_PATH=python3

# 检查配置文件是否存在
if [ ! -f "feishu_config.json" ]; then
    echo "⚠️  警告: 未找到配置文件 feishu_config.json"
    echo ""
    echo "请执行以下步骤:"
    echo "1. 复制配置文件模板: cp feishu_config_template.json feishu_config.json"
    echo "2. 编辑 feishu_config.json，填入你的飞书Webhook地址"
    echo "3. 重新运行此脚本"
    echo ""
    read -p "按回车键继续..." 
    exit 1
fi

# 检查Python环境
if ! command -v $PYTHON_PATH &> /dev/null; then
    echo "❌ 错误: 未找到Python，请先安装Python3"
    exit 1
fi

# 运行AI新闻自动化
echo "正在启动AI新闻自动化流程..."
echo ""

$PYTHON_PATH src/ai_news_automation_with_feishu.py

EXIT_CODE=$?

echo ""
echo "========================================"
echo "自动化流程执行完成"
echo "退出代码: $EXIT_CODE"
echo "查看详细日志: ai_news_automation.log"
echo "========================================"
echo ""

# 根据退出代码显示结果
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ 自动化流程执行成功！"
else
    echo "❌ 自动化流程执行失败"
fi

echo ""
read -p "按回车键退出..." </dev/tty