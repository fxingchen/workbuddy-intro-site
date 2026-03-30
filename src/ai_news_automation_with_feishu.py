#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI新闻自动化完整流程（包含飞书通知）
整合AI新闻搜集、分析和飞书发送功能
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
import subprocess

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.feishu_notifier import FeishuNotifier

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ai_news_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AINewsAutomation:
    """AI新闻自动化管理器"""
    
    def __init__(self, config_path=None):
        """
        初始化自动化管理器
        
        Args:
            config_path: 配置文件路径
        """
        self.project_root = project_root
        self.config_path = config_path or "feishu_config.json"
        self.feishu_config = None
        self.notifier = None
        
        self.load_config()
        self.setup_directories()
    
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.feishu_config = json.load(f)
                logger.info(f"已加载配置文件: {self.config_path}")
            else:
                logger.warning(f"配置文件不存在，使用默认设置")
                self.feishu_config = {
                    "webhook_url": None,
                    "notify_enabled": False,
                    "notify_on_error": True
                }
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            self.feishu_config = {
                "webhook_url": None,
                "notify_enabled": False,
                "notify_on_error": True
            }
    
    def setup_directories(self):
        """设置必要的目录结构"""
        directories = [
            ".codebuddy/automations/ai",
            "logs",
            "reports"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"确保目录存在: {dir_path}")
    
    def execute_ai_news_collection(self):
        """
        执行AI新闻收集任务
        
        这里模拟执行AI新闻收集，实际应调用你的AI新闻收集逻辑
        返回生成的最新报告文件路径
        """
        logger.info("开始执行AI新闻收集任务...")
        
        try:
            # 这里应该调用你的AI新闻收集代码
            # 例如: from src.ai_news_collector import collect_ai_news
            # report_path = collect_ai_news()
            
            # 模拟生成报告文件
            today = datetime.now().strftime('%Y-%m-%d')
            report_dir = self.project_root / ".codebuddy/automations/ai"
            report_path = report_dir / f"{today}_ai_news.md"
            
            # 如果报告文件不存在，创建一个示例报告
            if not report_path.exists():
                self.create_sample_report(report_path)
            
            logger.info(f"AI新闻收集完成，报告路径: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"AI新闻收集失败: {e}")
            # 创建错误报告
            error_report = self.create_error_report(e)
            return error_report
    
    def create_sample_report(self, report_path):
        """创建示例报告文件（用于测试）"""
        today = datetime.now().strftime('%Y年%m月%d日')
        sample_content = f"""# AI新闻推送 - {today}

## 测试报告 - 自动化集成验证

### 一、自动化测试成功
**事件内容**：AI新闻自动化与飞书通知集成测试成功
**关注原因**：验证自动化流程的完整性和稳定性
**优化策略**：持续监控和改进自动化任务执行

### 二、飞书通知测试
**事件内容**：飞书Webhook通知功能集成完成
**关注原因**：实现AI新闻的实时推送
**优化策略**：优化消息格式和发送时机

### 三、系统状态
- **自动化状态**: 运行正常
- **飞书集成**: 已配置
- **报告生成**: 成功
- **发送时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---
*这是一个测试报告，实际AI新闻内容将由自动化任务生成*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        
        logger.info(f"已创建示例报告: {report_path}")
    
    def create_error_report(self, error):
        """创建错误报告"""
        error_dir = self.project_root / ".codebuddy/automations/ai/errors"
        error_dir.mkdir(exist_ok=True)
        
        error_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        error_path = error_dir / f"error_{error_time}.md"
        
        error_content = f"""# AI新闻自动化错误报告

## 错误时间
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 错误信息
```
{str(error)}
```

## 系统信息
- Python版本: {sys.version}
- 工作目录: {os.getcwd()}
- 配置文件: {self.config_path if os.path.exists(self.config_path) else '不存在'}

## 建议操作
1. 检查网络连接
2. 验证配置文件
3. 查看详细日志: ai_news_automation.log
4. 联系系统管理员
"""
        
        with open(error_path, 'w', encoding='utf-8') as f:
            f.write(error_content)
        
        logger.error(f"已创建错误报告: {error_path}")
        return str(error_path)
    
    def send_to_feishu(self, report_path):
        """发送报告到飞书"""
        if not self.feishu_config.get('notify_enabled', False):
            logger.info("飞书通知未启用，跳过发送")
            return False
        
        webhook_url = self.feishu_config.get('webhook_url')
        if not webhook_url:
            logger.error("未配置飞书Webhook URL")
            return False
        
        try:
            logger.info("开始发送报告到飞书...")
            self.notifier = FeishuNotifier(webhook_url=webhook_url)
            success = self.notifier.send_ai_news_report(report_path)
            
            if success:
                logger.info("飞书通知发送成功")
            else:
                logger.error("飞书通知发送失败")
            
            return success
            
        except Exception as e:
            logger.error(f"飞书发送过程异常: {e}")
            return False
    
    def run_full_automation(self):
        """运行完整的自动化流程"""
        logger.info("=" * 60)
        logger.info("开始AI新闻完整自动化流程")
        logger.info("=" * 60)
        
        start_time = datetime.now()
        
        try:
            # 步骤1: 执行AI新闻收集
            logger.info("步骤1: 执行AI新闻收集")
            report_path = self.execute_ai_news_collection()
            
            # 检查是否错误报告
            if "errors" in report_path:
                logger.warning("AI新闻收集失败，生成的是错误报告")
                
                # 如果配置了错误通知，发送错误报告
                if self.feishu_config.get('notify_on_error', True):
                    self.send_to_feishu(report_path)
                
                return False
            
            # 步骤2: 发送到飞书
            logger.info("步骤2: 发送到飞书")
            feishu_success = self.send_to_feishu(report_path)
            
            # 步骤3: 记录执行结果
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"自动化流程完成，总耗时: {execution_time:.2f}秒")
            
            # 创建执行摘要
            self.create_execution_summary(start_time, report_path, feishu_success)
            
            return feishu_success
            
        except Exception as e:
            logger.error(f"自动化流程执行失败: {e}")
            # 发送错误通知
            if self.feishu_config.get('notify_on_error', True):
                error_report = self.create_error_report(e)
                self.send_to_feishu(error_report)
            
            return False
    
    def create_execution_summary(self, start_time, report_path, feishu_success):
        """创建执行摘要"""
        summary_dir = self.project_root / ".codebuddy/automations/ai/summaries"
        summary_dir.mkdir(exist_ok=True)
        
        today = datetime.now().strftime('%Y-%m-%d')
        summary_path = summary_dir / f"execution_summary_{today}.json"
        
        summary = {
            "execution_date": today,
            "start_time": start_time.isoformat(),
            "end_time": datetime.now().isoformat(),
            "duration_seconds": (datetime.now() - start_time).total_seconds(),
            "report_path": report_path,
            "feishu_enabled": self.feishu_config.get('notify_enabled', False),
            "feishu_success": feishu_success,
            "webhook_configured": bool(self.feishu_config.get('webhook_url')),
            "config_file": self.config_path if os.path.exists(self.config_path) else None
        }
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"执行摘要已保存: {summary_path}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AI新闻自动化（含飞书通知）')
    parser.add_argument('--config', '-c', type=str,
                       default='feishu_config.json',
                       help='配置文件路径')
    parser.add_argument('--test', '-t', action='store_true',
                       help='测试模式，不实际发送飞书通知')
    parser.add_argument('--force', '-f', action='store_true',
                       help='强制发送，即使配置中未启用')
    
    args = parser.parse_args()
    
    # 创建自动化实例
    automation = AINewsAutomation(config_path=args.config)
    
    # 如果是测试模式，临时修改配置
    if args.test:
        logger.info("进入测试模式")
        automation.feishu_config['notify_enabled'] = False
    
    # 如果是强制模式，临时启用通知
    if args.force and automation.feishu_config.get('webhook_url'):
        logger.info("进入强制发送模式")
        automation.feishu_config['notify_enabled'] = True
    
    # 运行自动化流程
    success = automation.run_full_automation()
    
    if success:
        logger.info("🎉 AI新闻自动化流程执行成功！")
        return 0
    else:
        logger.error("❌ AI新闻自动化流程执行失败")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)