#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书配置快速设置脚本
用于快速创建和验证飞书配置文件
"""

import json
import os
import sys
from pathlib import Path

def create_feishu_config():
    """创建飞书配置文件"""
    
    print("=" * 60)
    print("飞书配置快速设置工具")
    print("=" * 60)
    
    # 检查模板文件
    template_path = "feishu_config_template.json"
    config_path = "feishu_config.json"
    
    if not os.path.exists(template_path):
        print(f"❌ 错误: 未找到模板文件 {template_path}")
        return False
    
    # 读取模板
    with open(template_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # 获取用户输入
    print("\n📝 请输入飞书配置信息")
    print("-" * 40)
    
    webhook_url = input("飞书Webhook URL (格式: https://open.feishu.cn/open-apis/bot/v2/hook/...):\n> ").strip()
    
    if not webhook_url:
        print("⚠️  警告: 未输入Webhook URL，将创建空配置")
        config['webhook_url'] = ""
        config['notify_enabled'] = False
    else:
        config['webhook_url'] = webhook_url
        config['notify_enabled'] = True
    
    # 询问其他配置
    print("\n📋 可选配置 (按Enter使用默认值):")
    
    notify_time = input(f"发送时间 [默认: {config.get('notify_time', '09:05')}]: ").strip()
    if notify_time:
        config['notify_time'] = notify_time
    
    max_retries = input(f"最大重试次数 [默认: {config.get('max_retries', 3)}]: ").strip()
    if max_retries:
        config['max_retries'] = int(max_retries)
    
    timeout = input(f"超时时间(秒) [默认: {config.get('timeout_seconds', 10)}]: ").strip()
    if timeout:
        config['timeout_seconds'] = int(timeout)
    
    project_name = input(f"项目名称 [默认: {config.get('project_name', 'AI新闻自动化')}]: ").strip()
    if project_name:
        config['project_name'] = project_name
    
    # 保存配置文件
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ 配置文件已创建: {config_path}")
    
    # 显示配置摘要
    print("\n📊 配置摘要:")
    print("-" * 40)
    print(f"Webhook URL: {'已配置' if config['webhook_url'] else '未配置'}")
    print(f"通知启用: {'是' if config['notify_enabled'] else '否'}")
    print(f"发送时间: {config.get('notify_time', '09:05')}")
    print(f"错误通知: {'启用' if config.get('notify_on_error', True) else '禁用'}")
    print(f"最大重试: {config.get('max_retries', 3)}次")
    print(f"超时时间: {config.get('timeout_seconds', 10)}秒")
    
    return True


def validate_config():
    """验证配置文件"""
    
    config_path = "feishu_config.json"
    
    if not os.path.exists(config_path):
        print(f"❌ 配置文件不存在: {config_path}")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("\n🔍 配置文件验证:")
        print("-" * 40)
        
        # 检查必需字段
        required_fields = ['webhook_url', 'notify_enabled']
        missing_fields = []
        
        for field in required_fields:
            if field not in config:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ 缺少必需字段: {', '.join(missing_fields)}")
            return False
        
        # 检查URL格式
        webhook_url = config['webhook_url']
        if webhook_url and not webhook_url.startswith('https://open.feishu.cn/'):
            print("⚠️  警告: Webhook URL格式可能不正确")
            print(f"   当前URL: {webhook_url[:50]}...")
        elif not webhook_url:
            print("⚠️  警告: Webhook URL为空，通知功能将禁用")
        
        print("✅ 配置文件格式正确")
        print(f"✅ Webhook URL: {'已配置' if webhook_url else '未配置'}")
        print(f"✅ 通知功能: {'启用' if config['notify_enabled'] else '禁用'}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 验证过程错误: {e}")
        return False


def test_feishu_connection():
    """测试飞书连接"""
    
    try:
        import requests
    except ImportError:
        print("❌ 需要requests库，请安装: pip install requests")
        return False
    
    config_path = "feishu_config.json"
    
    if not os.path.exists(config_path):
        print(f"❌ 配置文件不存在: {config_path}")
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    webhook_url = config.get('webhook_url')
    if not webhook_url:
        print("❌ 未配置Webhook URL")
        return False
    
    print("\n📡 测试飞书连接...")
    print(f"URL: {webhook_url[:50]}...")
    
    try:
        test_message = {
            "msg_type": "text",
            "content": {
                "text": "🔧 AI新闻自动化连接测试\n\n这是一条测试消息，用于验证飞书Webhook配置是否正确。\n\n发送时间: 测试中..."
            }
        }
        
        import requests
        response = requests.post(
            webhook_url,
            json=test_message,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('code') == 0:
                print("✅ 飞书连接测试成功！")
                print("   消息已发送到飞书群组")
                return True
            else:
                print(f"❌ 飞书返回错误: {result.get('msg', '未知错误')}")
                return False
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(f"   响应内容: {response.text[:200]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 连接超时，请检查网络")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请检查URL和网络")
        return False
    except Exception as e:
        print(f"❌ 测试过程错误: {e}")
        return False


def main():
    """主函数"""
    
    print("=" * 60)
    print("AI新闻自动化 - 飞书配置工具")
    print("=" * 60)
    
    # 检查Python版本
    if sys.version_info < (3, 6):
        print("❌ 需要Python 3.6或更高版本")
        return 1
    
    # 显示菜单
    print("\n请选择操作:")
    print("1. 创建飞书配置文件")
    print("2. 验证现有配置文件")
    print("3. 测试飞书连接")
    print("4. 执行完整设置流程")
    print("0. 退出")
    
    choice = input("\n请输入选项 (0-4): ").strip()
    
    if choice == "1":
        if create_feishu_config():
            print("\n🎉 配置创建完成！")
        else:
            print("\n❌ 配置创建失败")
            
    elif choice == "2":
        validate_config()
        
    elif choice == "3":
        test_feishu_connection()
        
    elif choice == "4":
        print("\n🚀 开始完整设置流程...")
        print("-" * 40)
        
        # 步骤1: 创建配置
        if not os.path.exists("feishu_config.json"):
            print("步骤1: 创建配置文件")
            if not create_feishu_config():
                print("❌ 配置创建失败，停止设置")
                return 1
        
        # 步骤2: 验证配置
        print("\n步骤2: 验证配置文件")
        if not validate_config():
            print("❌ 配置验证失败，停止设置")
            return 1
        
        # 步骤3: 测试连接
        print("\n步骤3: 测试飞书连接")
        config = json.load(open("feishu_config.json", 'r', encoding='utf-8'))
        if config.get('webhook_url'):
            if test_feishu_connection():
                print("\n🎉 完整设置成功！")
                print("\n下一步:")
                print("1. 运行自动化: run_ai_news_with_feishu.bat (Windows)")
                print("2. 或: ./run_ai_news_with_feishu.sh (Linux/macOS)")
                print("3. 查看文档: AUTOMATION_SETUP_COMPLETE.md")
            else:
                print("⚠️  连接测试失败，但配置文件已创建")
                print("   你可以稍后手动测试连接")
        else:
            print("⚠️  未配置Webhook URL，跳过连接测试")
            print("   配置文件已创建，请填入URL后重新测试")
        
    elif choice == "0":
        print("退出设置工具")
        return 0
        
    else:
        print("❌ 无效选项")
        return 1
    
    print("\n" + "=" * 60)
    print("设置工具运行完成")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(0)