"""
智能体基类定义

定义智能体的基本接口和行为模式，为不同类型的智能体提供统一的基础。
"""

from typing import Dict, Any, Optional, List, Callable, Awaitable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from datetime import datetime

from .context import Context
from .memory import Memory


@dataclass
class AgentConfig:
    """智能体配置"""
    name: str = "ClawHub智能体"
    description: str = "基于ClawHub框架的智能体"
    skills: List[str] = field(default_factory=list)
    plugins: List[str] = field(default_factory=list)
    memory_size: int = 100
    max_context_length: int = 10
    enable_history: bool = True
    enable_learning: bool = True
    response_timeout: int = 30
    config: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """智能体基类
    
    定义智能体的基本接口，所有具体的智能体实现都应该继承此类。
    """
    
    def __init__(self, config: AgentConfig):
        """
        初始化智能体
        
        Args:
            config: 智能体配置
        """
        self.config = config
        self.name = config.name
        self.description = config.description
        self.skills = config.skills
        self.plugins = config.plugins
        self.memory = Memory(config.memory_size)
        self.created_at = datetime.now()
        self.stats = {
            "messages_processed": 0,
            "responses_sent": 0,
            "errors": 0,
            "avg_response_time": 0.0,
        }
        self._handlers: Dict[str, List[Callable]] = {}
        
    async def initialize(self) -> None:
        """初始化智能体，加载插件和技能"""
        self._setup_default_handlers()
        await self._load_plugins()
        await self._load_skills()
        
    def _setup_default_handlers(self) -> None:
        """设置默认事件处理器"""
        self.register_handler("message", self._default_message_handler)
        self.register_handler("error", self._default_error_handler)
        
    async def _load_plugins(self) -> None:
        """加载配置的插件"""
        for plugin_name in self.plugins:
            try:
                # 动态加载插件
                plugin = self._load_plugin_module(plugin_name)
                if plugin:
                    plugin.initialize(self.config.config.get(plugin_name, {}))
                    self.memory.store(f"plugin_loaded:{plugin_name}", {
                        "name": plugin_name,
                        "loaded_at": datetime.now(),
                    })
            except Exception as e:
                print(f"插件 {plugin_name} 加载失败: {e}")
                
    async def _load_skills(self) -> None:
        """加载配置的技能"""
        for skill_name in self.skills:
            try:
                # 动态加载技能
                skill = self._load_skill_module(skill_name)
                if skill:
                    self.memory.store(f"skill_loaded:{skill_name}", {
                        "name": skill_name,
                        "loaded_at": datetime.now(),
                    })
            except Exception as e:
                print(f"技能 {skill_name} 加载失败: {e}")
                
    def _load_plugin_module(self, plugin_name: str) -> Optional[Any]:
        """动态加载插件模块"""
        # 这里应该实现动态导入
        return None
        
    def _load_skill_module(self, skill_name: str) -> Optional[Any]:
        """动态加载技能模块"""
        # 这里应该实现动态导入
        return None
        
    def register_handler(self, event_type: str, handler: Callable) -> None:
        """注册事件处理器
        
        Args:
            event_type: 事件类型（如'message', 'error'等）
            handler: 事件处理函数
        """
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)
        
    async def handle_message(self, context: Context, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """处理消息的核心方法
        
        Args:
            context: 对话上下文
            message: 原始消息数据
            
        Returns:
            处理后的响应消息，如果没有响应则返回None
        """
        start_time = datetime.now()
        
        try:
            # 预处理消息
            processed_message = await self.preprocess_message(context, message)
            
            # 触发消息事件
            await self.trigger_event("message", {
                "context": context,
                "message": processed_message,
                "timestamp": datetime.now(),
            })
            
            # 调用注册的消息处理器
            responses = []
            if "message" in self._handlers:
                for handler in self._handlers["message"]:
                    try:
                        result = await handler(context, processed_message)
                        if result:
                            responses.append(result)
                    except Exception as e:
                        await self.trigger_event("error", {
                            "context": context,
                            "error": e,
                            "handler": handler.__name__,
                        })
                        
            # 如果没有处理器响应，使用默认处理
            if not responses:
                response = await self._default_message_handler(context, processed_message)
                if response:
                    responses.append(response)
                    
            # 后处理响应
            final_response = None
            if responses:
                final_response = await self.postprocess_response(context, processed_message, responses[0])
                
            # 更新统计信息
            response_time = (datetime.now() - start_time).total_seconds()
            self.stats["messages_processed"] += 1
            if final_response:
                self.stats["responses_sent"] += 1
                # 更新平均响应时间（加权平均）
                old_avg = self.stats["avg_response_time"]
                count = self.stats["messages_processed"]
                self.stats["avg_response_time"] = (old_avg * (count - 1) + response_time) / count
                
            return final_response
            
        except Exception as e:
            self.stats["errors"] += 1
            await self.trigger_event("error", {
                "context": context,
                "error": e,
                "timestamp": datetime.now(),
            })
            raise
            
    async def preprocess_message(self, context: Context, message: Dict[str, Any]) -> Dict[str, Any]:
        """预处理消息
        
        Args:
            context: 对话上下文
            message: 原始消息
            
        Returns:
            处理后的消息
        """
        # 这里可以添加消息标准化、清理等逻辑
        return message
        
    async def postprocess_response(self, context: Context, message: Dict[str, Any], response: Dict[str, Any]) -> Dict[str, Any]:
        """后处理响应
        
        Args:
            context: 对话上下文
            message: 原始消息
            response: 生成的响应
            
        Returns:
            处理后的最终响应
        """
        # 这里可以添加响应格式化、日志记录等逻辑
        return response
        
    async def _default_message_handler(self, context: Context, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """默认消息处理器
        
        Args:
            context: 对话上下文
            message: 消息数据
            
        Returns:
            默认响应消息
        """
        # 这里可以设置默认的响应逻辑
        content = message.get("content", "")
        
        # 简单的问候语识别
        greetings = ["hello", "hi", "你好", "嗨", "您好", "嘿"]
        if content.lower() in greetings:
            return {
                "content": f"你好！我是{self.name}，有什么可以帮助你的吗？",
                "type": "text",
            }
            
        # 基础问答
        if content.endswith("?") or "是什么" in content or "怎么" in content:
            return {
                "content": f"这是一个很好的问题！作为{self.name}，我还在学习中，你可以尝试问我更具体的问题。",
                "type": "text",
            }
            
        return None
        
    async def _default_error_handler(self, context: Context, error_data: Dict[str, Any]) -> None:
        """默认错误处理器"""
        error = error_data.get("error")
        error_context = error_data.get("context", {})
        
        print(f"智能体错误 - 时间: {datetime.now()}")
        print(f"上下文: {error_context}")
        print(f"错误: {error}")
        
    async def trigger_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """触发事件
        
        Args:
            event_type: 事件类型
            data: 事件数据
        """
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                try:
                    # 检查是否是异步函数
                    if callable(handler):
                        await handler(data)
                except Exception as e:
                    print(f"事件处理器执行失败: {e}")
                    
    async def shutdown(self) -> None:
        """关闭智能体，清理资源"""
        await self.trigger_event("shutdown", {
            "agent": self.name,
            "timestamp": datetime.now(),
            "stats": self.stats,
        })
        
    def get_status(self) -> Dict[str, Any]:
        """获取智能体状态"""
        return {
            "name": self.name,
            "description": self.description,
            "status": "running",
            "uptime": (datetime.now() - self.created_at).total_seconds(),
            "stats": self.stats,
            "skills": self.skills,
            "plugins": self.plugins,
            "memory_usage": self.memory.get_usage(),
        }
        
    @abstractmethod
    async def train(self, training_data: List[Dict[str, Any]]) -> None:
        """训练智能体
        
        Args:
            training_data: 训练数据列表
        """
        pass
        
    @abstractmethod
    async def evaluate(self, test_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """评估智能体性能
        
        Args:
            test_data: 测试数据列表
            
        Returns:
            评估指标字典
        """
        pass