"""
消息处理器插件

提供消息预处理、过滤和增强功能。
"""

from typing import Dict, Any, Optional
import re
from datetime import datetime

from ..core.plugin import BasePlugin


class MessageProcessorPlugin(BasePlugin):
    """消息处理器插件
    
    对输入消息进行预处理，包括：
    - 敏感信息过滤
    - 格式标准化
    - 意图识别
    - 情绪分析
    """
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """初始化插件
        
        Args:
            config: 插件配置
        """
        super().initialize(config)
        
        # 加载配置
        self.sensitive_patterns = config.get("sensitive_patterns", [])
        self.enable_intent_detection = config.get("enable_intent_detection", True)
        self.enable_sentiment_analysis = config.get("enable_sentiment_analysis", False)
        self.max_length = config.get("max_length", 1000)
        
        # 编译敏感词正则
        self.sensitive_regexes = [
            re.compile(pattern, re.IGNORECASE)
            for pattern in self.sensitive_patterns
        ]
        
        # 意图关键词
        self.intent_keywords = {
            "greeting": ["你好", "您好", "hello", "hi", "嗨", "早上好", "下午好", "晚上好"],
            "farewell": ["再见", "拜拜", "goodbye", "bye", "下次聊"],
            "thanks": ["谢谢", "感谢", "thank you", "thanks"],
            "help": ["帮助", "怎么", "如何", "怎样", "help", "如何使用"],
            "question": ["什么", "为什么", "怎么", "如何", "?", "？", "吗"],
            "command": ["/", "命令", "执行", "运行"],
        }
        
        self.log("info", "消息处理器插件初始化完成")
        
    async def handle_message(self, context: Any, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """处理消息
        
        Args:
            context: 对话上下文
            message: 消息数据
            
        Returns:
            处理后的消息或None
        """
        try:
            processed_message = message.copy()
            
            # 1. 提取原始内容
            content = str(message.get("content", "")).strip()
            if not content:
                return None
                
            # 2. 长度限制
            if len(content) > self.max_length:
                content = content[:self.max_length] + "..."
                processed_message["content"] = content
                self.log("warning", f"消息过长，已截断到{self.max_length}字符")
                
            # 3. 敏感信息过滤
            filtered_content, filtered_count = self._filter_sensitive_content(content)
            if filtered_count > 0:
                processed_message["content"] = filtered_content
                processed_message["filtered"] = True
                processed_message["filtered_count"] = filtered_count
                self.log("info", f"过滤了{filtered_count}处敏感内容")
                
            # 4. 意图识别
            if self.enable_intent_detection:
                intent = self._detect_intent(content)
                if intent:
                    processed_message["intent"] = intent
                    processed_message["intent_confidence"] = self._calculate_intent_confidence(content, intent)
                    
            # 5. 情绪分析（简化版）
            if self.enable_sentiment_analysis:
                sentiment = self._analyze_sentiment(content)
                if sentiment:
                    processed_message["sentiment"] = sentiment
                    
            # 6. 消息增强
            enhanced_data = self._enhance_message(context, processed_message)
            if enhanced_data:
                processed_message.update(enhanced_data)
                
            # 7. 添加处理元数据
            processed_message["processed_by"] = self.name
            processed_message["processed_at"] = datetime.now().isoformat()
            processed_message["original_length"] = len(str(message.get("content", "")))
            processed_message["processed_length"] = len(processed_message["content"])
            
            self.log("info", f"消息处理完成，意图: {processed_message.get('intent', 'unknown')}")
            
            # 插件不生成响应，只处理消息
            return None
            
        except Exception as e:
            self.log("error", f"消息处理失败: {e}")
            return None
            
    def _filter_sensitive_content(self, content: str) -> tuple[str, int]:
        """过滤敏感内容
        
        Args:
            content: 原始内容
            
        Returns:
            过滤后的内容和过滤数量
        """
        if not self.sensitive_regexes:
            return content, 0
            
        filtered_count = 0
        filtered_content = content
        
        for pattern in self.sensitive_regexes:
            matches = pattern.findall(filtered_content)
            if matches:
                # 用*替换敏感内容
                filtered_content = pattern.sub("*", filtered_content)
                filtered_count += len(matches)
                
        return filtered_content, filtered_count
        
    def _detect_intent(self, content: str) -> Optional[str]:
        """检测意图
        
        Args:
            content: 消息内容
            
        Returns:
            检测到的意图
        """
        content_lower = content.lower()
        
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    return intent
                    
        return None
        
    def _calculate_intent_confidence(self, content: str, intent: str) -> float:
        """计算意图置信度
        
        Args:
            content: 消息内容
            intent: 检测到的意图
            
        Returns:
            置信度（0-1）
        """
        content_lower = content.lower()
        keywords = self.intent_keywords.get(intent, [])
        
        if not keywords:
            return 0.5
            
        # 计算关键词匹配程度
        matched_keywords = []
        for keyword in keywords:
            if keyword.lower() in content_lower:
                matched_keywords.append(keyword)
                
        # 简化置信度计算
        confidence = len(matched_keywords) / len(keywords) if keywords else 0
        return min(confidence, 1.0)
        
    def _analyze_sentiment(self, content: str) -> Optional[str]:
        """分析情绪（简化版）
        
        Args:
            content: 消息内容
            
        Returns:
            情绪分类
        """
        # 情绪关键词（简化版）
        positive_words = ["好", "棒", "优秀", "完美", "喜欢", "爱", "开心", "高兴", "谢谢", "感谢"]
        negative_words = ["差", "坏", "糟糕", "讨厌", "烦", "生气", "愤怒", "不满", "失望"]
        
        content_lower = content.lower()
        
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
            
    def _enhance_message(self, context: Any, message: Dict[str, Any]) -> Dict[str, Any]:
        """增强消息数据
        
        Args:
            context: 对话上下文
            message: 消息数据
            
        Returns:
            增强的数据
        """
        enhanced = {}
        
        # 添加上下文信息
        if hasattr(context, 'session'):
            enhanced["session_id"] = context.session.session_id
            enhanced["channel"] = context.session.channel
            
        # 添加消息类型信息
        msg_type = message.get("type", "unknown")
        if msg_type == "text":
            content = message.get("content", "")
            if len(content) < 50:
                enhanced["message_style"] = "short"
            elif len(content) < 200:
                enhanced["message_style"] = "medium"
            else:
                enhanced["message_style"] = "long"
                
        # 检测是否包含链接
        content = message.get("content", "")
        url_pattern = re.compile(r'https?://[^\s]+')
        urls = url_pattern.findall(content)
        if urls:
            enhanced["contains_urls"] = True
            enhanced["url_count"] = len(urls)
            
        # 检测是否包含数字
        number_pattern = re.compile(r'\b\d+\b')
        numbers = number_pattern.findall(content)
        if numbers:
            enhanced["contains_numbers"] = True
            enhanced["number_count"] = len(numbers)
            
        return enhanced
        
    async def shutdown(self) -> None:
        """关闭插件"""
        super().shutdown()
        self.log("info", "消息处理器插件已关闭")
        
    def get_plugin_info(self) -> Dict[str, Any]:
        """获取插件信息
        
        Returns:
            插件信息
        """
        return {
            "name": self.name,
            "description": "消息预处理和增强插件",
            "version": "1.0.0",
            "config": {
                "sensitive_patterns_count": len(self.sensitive_patterns),
                "enable_intent_detection": self.enable_intent_detection,
                "enable_sentiment_analysis": self.enable_sentiment_analysis,
                "max_length": self.max_length,
            },
            "intent_keywords": {k: len(v) for k, v in self.intent_keywords.items()},
        }