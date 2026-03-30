#!/bin/bash
# WorkBuddy网站部署脚本（Linux/Mac）
# 用于快速部署到GitHub Pages

echo "========================================"
echo "WorkBuddy 网站部署助手"
echo "========================================"
echo ""

# 检查是否已配置Git远程仓库
if ! git remote -v | grep -q "origin"; then
    echo "[错误] 未配置Git远程仓库"
    echo ""
    echo "请先执行以下步骤："
    echo "1. 访问 https://github.com/new"
    echo "2. 创建一个新仓库（例如：workbuddy-intro）"
    echo "3. 运行此脚本并输入仓库地址"
    echo ""
    read -p "请输入你的GitHub仓库地址（例如：https://github.com/username/workbuddy-intro.git）: " REPO_URL
    git remote add origin "$REPO_URL"
else
    echo "[信息] Git远程仓库已配置"
    git remote -v
fi

echo ""
echo "[1/3] 正在添加文件..."
git add .

echo ""
echo "[2/3] 正在提交更改..."
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "更新WorkBuddy网站 - $TIMESTAMP"

echo ""
echo "[3/3] 正在推送到GitHub..."
git push -u origin main

if [ $? -ne 0 ]; then
    echo ""
    echo "[错误] 推送失败！可能需要配置Git凭据"
    echo ""
    echo "请尝试："
    echo "git config --global user.name '你的名字'"
    echo "git config --global user.email '你的邮箱'"
    echo ""
else
    echo ""
    echo "========================================"
    echo "✓ 部署成功！"
    echo "========================================"
    echo ""
    echo "下一步："
    echo "1. 访问你的GitHub仓库"
    echo "2. 进入 Settings > Pages"
    echo "3. Source选择：Deploy from a branch"
    echo "4. Branch选择：main, 目录选择：/(root)"
    echo "5. 点击Save"
    echo ""
    echo "等待1-2分钟，网站将上线！"
    echo ""
fi

read -p "按Enter键退出..."
