#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书Webhook通知发送器
用于将AI新闻报告自动发送到飞书
支持智能类型识别、富交互卡片、AI摘要生成
"""

import json
import requests
import os
from datetime import datetime
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional, Tuple
import re

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 定义报告类型常量
REPORT_TYPE_AI_NEWS = "ai_news"
REPORT_TYPE_GAME_DEV = "game_dev"
REPORT_TYPE_NOVEL = "novel"
REPORT_TYPE_GENERIC = "generic"

class FeishuNotifier:
    """飞书Webhook通知发送器"""
    
    def __init__(self, webhook_url: Optional[str] = None, config_path: Optional[str] = None):
        """
        初始化飞书通知器
        
        Args:
            webhook_url: 飞书Webhook URL
            config_path: 配置文件路径
        """
        self.webhook_url: Optional[str] = webhook_url
        self.config_path: str = config_path or "feishu_config.json"
        
        if not webhook_url:
            self.load_config()
    
    def detect_report_type(self, content: str, title: str) -> str:
        """
        智能识别报告类型
        
        Args:
            content: 报告内容
            title: 报告标题
            
        Returns:
            报告类型常量
        """
        title_lower = title.lower()
        content_lower = content.lower()
        
        # 根据标题关键词判断
        if any(keyword in title_lower for keyword in ['ai新闻', 'ai资讯', 'ai动态', '人工智能']):
            return REPORT_TYPE_AI_NEWS
        elif any(keyword in title_lower for keyword in ['游戏开发', '游戏工具', 'gamedev']):
            return REPORT_TYPE_GAME_DEV
        elif any(keyword in title_lower for keyword in ['小说', 'novel', '创作']):
            return REPORT_TYPE_NOVEL
        
        # 根据内容关键词判断
        elif '具身智能' in content or 'AI coding' in content:
            return REPORT_TYPE_AI_NEWS
        elif '纹理生成' in content or '着色器' in content:
            return REPORT_TYPE_GAME_DEV
        elif '大纲规划' in content or '素材管理' in content:
            return REPORT_TYPE_NOVEL
        
        return REPORT_TYPE_GENERIC
    
    def generate_ai_summary(self, content: str, report_type: str) -> Tuple[str, List[str]]:
        """
        使用AI生成智能摘要
        
        Args:
            content: 完整报告内容
            report_type: 报告类型
            
        Returns:
            摘要文本和关键要点列表
        """
        try:
            # 提取前2000个字符作为上下文（避免过长）
            context = content[:2000]
            
            # 根据报告类型生成不同的摘要提示
            if report_type == REPORT_TYPE_AI_NEWS:
                prompt = f"""请为以下AI新闻报告生成一个简洁的摘要（不超过200字）和3-5个关键要点：

{context}

请按以下格式返回：
摘要：[摘要内容]
要点：
• [要点1]
• [要点2]
• [要点3]"""
            elif report_type == REPORT_TYPE_GAME_DEV:
                prompt = f"""请为以下游戏开发工具报告生成一个简洁的摘要（不超过200字）和3-5个核心工具推荐：

{context}

请按以下格式返回：
摘要：[摘要内容]
核心工具：
• [工具1]
• [工具2]
• [工具3]"""
            elif report_type == REPORT_TYPE_NOVEL:
                prompt = f"""请为以下小说创作报告生成一个简洁的摘要（不超过200字）和3-5个创作建议：

{context}

请按以下格式返回：
摘要：[摘要内容]
建议：
• [建议1]
• [建议2]
• [建议3]"""
            else:
                prompt = f"""请为以下报告生成一个简洁的摘要（不超过200字）和3-5个关键要点：

{context}

请按以下格式返回：
摘要：[摘要内容]
要点：
• [要点1]
• [要点2]
• [要点3]"""
            
            # 这里可以集成您的AI调用逻辑
            # 为了简化，暂时使用规则提取作为后备方案
            logger.info(f"生成AI摘要中，报告类型: {report_type}")
            
            # 后备方案：使用规则提取关键信息
            return self._extract_key_info_fallback(content, report_type)
            
        except Exception as e:
            logger.error(f"AI摘要生成失败: {e}")
            # 失败后使用后备方案
            return self._extract_key_info_fallback(content, report_type)
    
    def _extract_key_info_fallback(self, content: str, report_type: str) -> Tuple[str, List[str]]:
        """
        后备方案：使用规则提取关键信息
        """
        lines = content.split('\n')
        summary = ""
        key_points = []
        
        # 提取第一段的摘要
        for line in lines[5:15]:  # 跳过标题和前几行
            if line.strip() and not line.startswith('#') and not line.startswith('---'):
                summary = line.strip()[:150] + "..." if len(line.strip()) > 150 else line.strip()
                break
        
        if not summary:
            summary = "报告摘要需要查看完整内容"
        
        # 提取要点
        for line in lines:
            if line.startswith('- **') and len(key_points) < 5:
                clean_line = line.replace('- **', '').replace('**', '').strip()
                if len(clean_line) > 100:
                    clean_line = clean_line[:97] + "..."
                key_points.append(clean_line)
        
        if not key_points:
            key_points = ["请查看完整报告获取详细信息"]
        
        return summary, key_points
    
    def load_config(self):
        """从配置文件加载飞书配置"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.webhook_url = config.get('webhook_url')
                    logger.info(f"已从配置文件加载飞书Webhook配置")
            else:
                logger.warning(f"配置文件不存在: {self.config_path}")
                logger.info("请创建配置文件或直接提供webhook_url参数")
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
    
    def create_ai_news_message(self, report_path: str, use_interactive_card: bool = True) -> Dict[str, Any]:
        """
        从AI新闻报告创建飞书消息（支持富交互卡片）
        
        Args:
            report_path: AI新闻报告文件路径
            use_interactive_card: 是否使用交互式卡片格式
            
        Returns:
            飞书消息格式的字典
        """
        try:
            # 读取报告文件
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 识别报告类型
            lines = content.split('\n')
            title = lines[0].replace('# ', '').strip() if lines[0].startswith('#') else "AI新闻推送"
            report_type = self.detect_report_type(content, title)
            
            # 生成AI摘要和关键要点
            summary, key_points = self.generate_ai_summary(content, report_type)
            
            # 根据配置选择消息格式
            if use_interactive_card:
                return self.create_interactive_card(report_path, title, report_type, summary, key_points)
            else:
                return self.create_rich_text_message(report_path, title, report_type, summary, key_points)
            
        except Exception as e:
            logger.error(f"创建消息失败: {e}", exc_info=True)
            return self.create_simple_message(f"❌ 创建消息失败: {str(e)[:100]}...")
    
    def create_rich_text_message(self, report_path: str, title: str, report_type: str, summary: str, key_points: List[str]) -> Dict[str, Any]:
        """
        创建富文本消息（post格式）
        """
        today = datetime.now().strftime('%Y年%m月%d日')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 根据报告类型设置不同的图标和颜色
        type_icons = {
            REPORT_TYPE_AI_NEWS: "📊",
            REPORT_TYPE_GAME_DEV: "🎮",
            REPORT_TYPE_NOVEL: "📚",
            REPORT_TYPE_GENERIC: "📋"
        }
        
        type_names = {
            REPORT_TYPE_AI_NEWS: "AI新闻推送",
            REPORT_TYPE_GAME_DEV: "游戏开发报告",
            REPORT_TYPE_NOVEL: "小说创作报告",
            REPORT_TYPE_GENERIC: "自动化报告"
        }
        
        icon = type_icons.get(report_type, "📊")
        type_name = type_names.get(report_type, "自动化报告")
        
        # 构建消息内容
        message_content = []
        
        # 标题和类型
        message_content.append([
            {"tag": "text", "text": f"{icon} {type_name} - {today}\n\n"}
        ])
        
        # 主标题
        message_content.append([
            {"tag": "text", "text": f"🌟 {title}\n\n"}
        ])
        
        # AI生成的摘要
        if summary:
            message_content.append([
                {"tag": "text", "text": "📝 智能摘要:\n"},
                {"tag": "text", "text": f"{summary}\n\n"}
            ])
        
        # 关键要点
        if key_points:
            message_content.append([
                {"tag": "text", "text": "🔍 核心要点:\n"}
            ])
            
            for i, point in enumerate(key_points[:5], 1):  # 最多5个
                # 添加序号和要点
                message_content.append([
                    {"tag": "text", "text": f"{i}. {point}\n"}
                ])
            
            message_content.append([
                {"tag": "text", "text": "\n"}
            ])
        
        # 分隔线
        message_content.append([
            {"tag": "text", "text": "━━━━━━━━━━━━━━━━━━━━\n\n"}
        ])
        
        # 行动指引（根据报告类型定制）
        if report_type == REPORT_TYPE_AI_NEWS:
            actions = "• 查看完整报告了解详细信息\n• 根据核心发现调整工作策略\n• 关注重点AI技术发展趋势\n"
        elif report_type == REPORT_TYPE_GAME_DEV:
            actions = "• 查看完整报告了解工具详情\n• 试用推荐的开发工具\n• 关注新兴的游戏开发技术\n"
        elif report_type == REPORT_TYPE_NOVEL:
            actions = "• 查看完整报告获取创作建议\n• 根据市场分析调整创作方向\n• 关注热门小说类型趋势\n"
        else:
            actions = "• 查看完整报告了解详细信息\n• 根据报告内容采取行动\n• 定期查看自动化报告\n"
        
        message_content.append([
            {"tag": "text", "text": "💡 建议行动:\n"},
            {"tag": "text", "text": actions},
            {"tag": "text", "text": "\n"}
        ])
        
        # 文件信息
        message_content.append([
            {"tag": "text", "text": f"📁 完整报告: {report_path}\n"},
            {"tag": "text", "text": f"⏰ 发送时间: {current_time}\n"},
            {"tag": "text", "text": f"🤖 报告类型: {type_name}"}
        ])
        
        return {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": f"{icon} {title}",
                        "content": message_content
                    }
                }
            }
        }
    
    def create_interactive_card(self, report_path: str, title: str, report_type: str, summary: str, key_points: List[str]) -> Dict[str, Any]:
        """
        创建交互式卡片消息（card格式）
        
        特点：
        - 更美观的视觉设计
        - 支持按钮和交互
        - 更好的移动端体验
        """
        today = datetime.now().strftime('%Y年%m月%d日')
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 根据报告类型设置不同的图标和颜色
        type_config = {
            REPORT_TYPE_AI_NEWS: {
                "icon": "📊",
                "color": "blue",
                "name": "AI新闻推送",
                "header_color": "blue"
            },
            REPORT_TYPE_GAME_DEV: {
                "icon": "🎮",
                "color": "orange",
                "name": "游戏开发报告",
                "header_color": "orange"
            },
            REPORT_TYPE_NOVEL: {
                "icon": "📚",
                "color": "purple",
                "name": "小说创作报告",
                "header_color": "purple"
            },
            REPORT_TYPE_GENERIC: {
                "icon": "📋",
                "color": "grey",
                "name": "自动化报告",
                "header_color": "grey"
            }
        }
        
        config = type_config.get(report_type, type_config[REPORT_TYPE_GENERIC])
        
        # 构建卡片内容
        elements = [
            {
                "tag": "div",
                "text": {
                    "tag": "plain_text",
                    "content": f"{config['icon']} {config['name']} - {today}"
                },
                "style": {
                    "font_size": "large",
                    "font_weight": "bold",
                    "color": config['header_color']
                }
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "text": {
                    "tag": "plain_text",
                    "content": title
                },
                "style": {
                    "font_size": "large",
                    "font_weight": "bold",
                    "margin_bottom": "medium"
                }
            }
        ]
        
        # 添加摘要（如果有）
        if summary:
            elements.extend([
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "📝 智能摘要"
                    },
                    "style": {
                        "font_weight": "bold",
                        "margin_top": "medium",
                        "margin_bottom": "small"
                    }
                },
                {
                    "tag": "markdown",
                    "content": summary
                }
            ])
        
        # 添加要点（如果有）
        if key_points:
            elements.extend([
                {
                    "tag": "div",
                    "text": {
                        "tag": "plain_text",
                        "content": "🔍 核心要点"
                    },
                    "style": {
                        "font_weight": "bold",
                        "margin_top": "medium",
                        "margin_bottom": "small"
                    }
                },
                {
                    "tag": "markdown",
                    "content": "\n".join([f"• {point}" for point in key_points[:5]])
                }
            ])
        
        # 添加统计信息
        elements.extend([
            {"tag": "hr"},
            {
                "tag": "div",
                "text": {
                    "tag": "plain_text",
                    "content": f"📊 统计信息\n📁 文件: {Path(report_path).name}\n⏰ 时间: {current_time}"
                },
                "style": {
                    "font_size": "small",
                    "color": "grey"
                }
            }
        ])
        
        # 添加操作按钮
        elements.extend([
            {"tag": "hr"},
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "📂 查看完整报告"
                        },
                        "type": "primary",
                        "value": {
                            "action": "view_report",
                            "path": report_path
                        }
                    },
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "💾 保存到收藏"
                        },
                        "type": "default",
                        "value": {
                            "action": "save_report",
                            "path": report_path
                        }
                    }
                ]
            }
        ])
        
        return {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True
                },
                "elements": elements
            }
        }
    
    def create_simple_message(self, text):
        """创建简单的文本消息"""
        return {
            "msg_type": "text",
            "content": {
                "text": text
            }
        }
    
    def send_message(self, message):
        """
        发送消息到飞书
        
        Args:
            message: 飞书消息格式的字典
            
        Returns:
            bool: 是否发送成功
        """
        if not self.webhook_url:
            logger.error("未配置飞书Webhook URL")
            return False
        
        try:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            response = requests.post(
                self.webhook_url,
                headers=headers,
                data=json.dumps(message),
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0:
                    logger.info("飞书消息发送成功")
                    return True
                else:
                    logger.error(f"飞书返回错误: {result.get('msg')}")
                    return False
            else:
                logger.error(f"HTTP请求失败: {response.status_code}")
                return False
                
        except requests.exceptions.Timeout:
            logger.error("飞书API请求超时")
            return False
        except requests.exceptions.ConnectionError:
            logger.error("网络连接失败")
            return False
        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            return False
    
    def send_ai_news_report(self, report_path: str, use_interactive_card: bool = True) -> bool:
        """
        发送AI新闻报告到飞书（支持智能摘要和交互式卡片）
        
        Args:
            report_path: AI新闻报告文件路径
            use_interactive_card: 是否使用交互式卡片格式
            
        Returns:
            bool: 是否发送成功
        """
        logger.info(f"开始发送AI新闻报告: {report_path}")
        
        if not os.path.exists(report_path):
            logger.error(f"报告文件不存在: {report_path}")
            return False
        
        # 创建消息并发送
        message = self.create_ai_news_message(report_path, use_interactive_card=use_interactive_card)
        return self.send_message(message)
    
    def test_message_formats(self, report_path: str):
        """
        测试不同的消息格式
        
        Args:
            report_path: 测试用的报告文件路径
        """
        logger.info("测试飞书消息格式...")
        
        if not os.path.exists(report_path):
            logger.error(f"测试文件不存在: {report_path}")
            return
        
        # 测试1：普通文本消息
        logger.info("测试1: 普通文本消息")
        simple_msg = self.create_simple_message("这是一个简单的文本消息测试")
        logger.info(f"简单消息: {json.dumps(simple_msg, ensure_ascii=False, indent=2)}")
        
        # 测试2：富文本消息
        logger.info("测试2: 富文本消息")
        with open(report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        title = "测试报告"
        report_type = self.detect_report_type(content, title)
        summary, key_points = self.generate_ai_summary(content, report_type)
        
        rich_msg = self.create_rich_text_message(report_path, title, report_type, summary, key_points)
        logger.info(f"富文本消息: {json.dumps(rich_msg, ensure_ascii=False, indent=2)[:500]}...")
        
        # 测试3：交互式卡片
        logger.info("测试3: 交互式卡片消息")
        card_msg = self.create_interactive_card(report_path, title, report_type, summary, key_points)
        logger.info(f"卡片消息: {json.dumps(card_msg, ensure_ascii=False, indent=2)[:500]}...")
        
        logger.info("测试完成！")


def main():
    """
    主函数：发送AI新闻报告到飞书
    
    使用示例:
        # 基础使用（发送最新的AI新闻报告）
        python src/feishu_notifier.py
        
        # 指定报告文件
        python src/feishu_notifier.py --report "游戏开发工具网站收集_2026年3月月度报告.md"
        
        # 使用交互式卡片格式
        python src/feishu_notifier.py --interactive
        
        # 使用富文本格式（非卡片）
        python src/feishu_notifier.py --rich-text
        
        # 指定Webhook和配置文件
        python src/feishu_notifier.py --webhook "YOUR_WEBHOOK_URL" --config "custom_config.json"
        
        # 测试消息格式（不发送）
        python src/feishu_notifier.py --test-formats "报告文件.md"
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description='发送AI新闻报告到飞书（支持智能摘要和交互式卡片）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
功能特性:
  • 智能识别报告类型（AI新闻、游戏开发、小说创作等）
  • AI生成智能摘要和关键要点
  • 支持交互式卡片格式（按钮、富文本）
  • 详细的错误处理和日志记录
  • 支持多种消息格式测试
        """
    )
    
    # 主要参数
    parser.add_argument('--report', '-r', type=str, 
                       default=None,
                       help='AI新闻报告文件路径（默认自动查找最新报告）')
    parser.add_argument('--webhook', '-w', type=str,
                       help='飞书Webhook URL（可选，也可通过配置文件设置）')
    parser.add_argument('--config', '-c', type=str,
                       default='feishu_config.json',
                       help='配置文件路径（默认: feishu_config.json）')
    
    # 格式选择
    format_group = parser.add_mutually_exclusive_group()
    format_group.add_argument('--interactive', '-i', action='store_true',
                             help='使用交互式卡片格式（默认，推荐）')
    format_group.add_argument('--rich-text', '-t', action='store_true',
                             help='使用富文本格式（非卡片）')
    format_group.add_argument('--simple', '-s', action='store_true',
                             help='使用简单文本格式')
    
    # 测试和调试
    parser.add_argument('--test-formats', type=str, metavar='REPORT_PATH',
                       help='测试不同的消息格式（不发送，仅显示）')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='显示详细日志信息')
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # 创建通知器
    notifier = FeishuNotifier(webhook_url=args.webhook, config_path=args.config)
    
    # 测试模式
    if args.test_formats:
        logger.info("进入测试模式，不发送实际消息")
        notifier.test_message_formats(args.test_formats)
        return
    
    # 确定报告文件路径
    if args.report:
        report_path = args.report
    else:
        # 自动查找最新的报告文件
        possible_dirs = [
            Path(".codebuddy/automations/ai"),
            Path("."),
            Path("./reports")
        ]
        
        report_path = None
        for search_dir in possible_dirs:
            if search_dir.exists():
                report_files = list(search_dir.glob("*.md"))
                if report_files:
                    # 按修改时间排序，取最新的
                    report_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                    report_path = str(report_files[0])
                    logger.info(f"自动找到最新报告: {report_path}")
                    break
        
        if not report_path:
            logger.error("未找到任何报告文件")
            logger.info("提示: 可以使用 --report 参数指定报告文件路径")
            return
    
    # 验证报告文件
    if not os.path.exists(report_path):
        logger.error(f"报告文件不存在: {report_path}")
        return
    
    # 确定消息格式
    use_interactive = True  # 默认使用交互式卡片
    if args.simple:
        use_interactive = False
    elif args.rich_text:
        use_interactive = False
    
    # 发送报告
    logger.info(f"开始发送报告: {report_path}")
    logger.info(f"使用格式: {'交互式卡片' if use_interactive else '富文本' if args.rich_text else '简单文本'}")
    
    if notifier.send_ai_news_report(report_path, use_interactive_card=use_interactive):
        logger.info("✅ 报告发送成功！")
    else:
        logger.error("❌ 报告发送失败")


if __name__ == "__main__":
    main()