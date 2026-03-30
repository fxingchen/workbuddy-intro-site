"""
基础智能体实现

提供通用的智能体实现，为具体智能体提供基础功能。
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from ..core.agent import BaseAgent, AgentConfig
from ..core.context import Context, ContextManager
from ..core.plugin import PluginManager
from ..core.memory import HybridMemory


class BaseAgent(BaseAgent):
    """基础智能体
    
    提供通用的智能体实现，包括上下文管理、插件系统和记忆存储。
    """
    
    def __init__(self, config: AgentConfig):
        """
        初始化基础智能体
        
        Args:
            config: 智能体配置
        """
        super().__init__(config)
        
        # 扩展配置
        self.context_manager = ContextManager()
        self.plugin_manager = PluginManager()
        
        # 使用混合记忆
        self.memory = HybridMemory(
            short_term_capacity=config.memory_size,
            long_term_path=f"data/memory_{self.name.lower().replace(' ', '_')}.json",
        )
        
        # 初始化状态
        self.session_count = 0
        
    async def initialize(self) -> None:
        """初始化智能体"""
        await super().initialize()
        
        # 加载配置的插件
        for plugin_name in self.plugins:
            try:
                # 这里应该根据插件名加载实际的插件模块
                # 暂时使用占位符
                self._load_plugin(plugin_name)
            except Exception as e:
                print(f"加载插件 {plugin_name} 失败: {e}")
                
    def _load_plugin(self, plugin_name: str) -> None:
        """加载插件（简化实现）"""
        # 这里应该实现动态加载插件
        # 暂时打印日志
        print(f"加载插件: {plugin_name}")
        
    def create_context(
        self,
        user_id: str,
        channel: str = "unknown",
        request_data: Optional[Dict[str, Any]] = None,
        user_info: Optional[Dict[str, Any]] = None,
    ) -> Context:
        """创建对话上下文
        
        Args:
            user_id: 用户ID
            channel: 渠道标识
            request_data: 请求数据
            user_info: 用户信息
            
        Returns:
            创建的上下文
        """
        context = self.context_manager.create_context(
            session_id=None,  # 自动创建新会话
            user_id=user_id,
            channel=channel,
            request_data=request_data,
            user_info=user_info,
        )
        
        self.session_count += 1
        
        # 存储到记忆
        self.memory.store(
            key=f"session_{context.session.session_id}",
            value={
                "user_id": user_id,
                "channel": channel,
                "created_at": datetime.now().isoformat(),
            },
            importance=2.0,
        )
        
        return context
        
    async def process_message_with_context(
        self,
        context: Context,
        message: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """使用上下文处理消息
        
        Args:
            context: 对话上下文
            message: 消息数据
            
        Returns:
            响应消息
        """
        # 添加消息到上下文历史
        context.add_message_to_history({
            "role": "user",
            "content": message.get("content", ""),
            "type": message.get("type", "text"),
            "timestamp": datetime.now().isoformat(),
        })
        
        # 通过插件管道处理消息
        plugin_response = await self.plugin_manager.process_message(context, message)
        
        # 如果没有插件响应，使用智能体默认处理
        if not plugin_response:
            plugin_response = await self.handle_message(context, message)
            
        # 如果生成了响应，添加到历史
        if plugin_response:
            context.add_message_to_history({
                "role": "assistant",
                "content": plugin_response.get("content", ""),
                "type": plugin_response.get("type", "text"),
                "timestamp": datetime.now().isoformat(),
            })
            
            # 存储到记忆
            self._store_conversation_memory(context, message, plugin_response)
            
        return plugin_response
        
    def _store_conversation_memory(
        self,
        context: Context,
        user_message: Dict[str, Any],
        assistant_response: Dict[str, Any],
    ) -> None:
        """存储对话到记忆"""
        memory_key = f"conversation_{context.session.session_id}_{datetime.now().timestamp()}"
        
        # 计算重要性（基于对话长度、响应质量等）
        importance = 3.0  # 基础重要性
        
        # 对话越长越重要
        conversation_length = len(context.session.message_history)
        if conversation_length > 10:
            importance += 1.0
        if conversation_length > 20:
            importance += 1.0
            
        # 存储记忆
        self.memory.store(
            key=memory_key,
            value={
                "user_message": user_message,
                "assistant_response": assistant_response,
                "context_summary": context.get_context_summary(),
                "timestamp": datetime.now().isoformat(),
            },
            importance=importance,
        )
        
    async def get_session_history(
        self,
        session_id: str,
        limit: int = 20,
    ) -> Optional[List[Dict[str, Any]]]:
        """获取会话历史
        
        Args:
            session_id: 会话ID
            limit: 限制数量
            
        Returns:
            会话历史
        """
        session = self.context_manager.get_session(session_id)
        if not session:
            return None
            
        return session.get_recent_messages(limit)
        
    async def search_conversations(
        self,
        query: str,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """搜索对话记录
        
        Args:
            query: 搜索查询
            limit: 限制数量
            
        Returns:
            搜索结果
        """
        # 在记忆中搜索
        search_results = self.memory.search(query)
        
        results = []
        for key, value in search_results[:limit]:
            if isinstance(value, dict) and "conversation" in key:
                results.append({
                    "key": key,
                    "summary": {
                        "user_message_preview": str(value.get("user_message", {}).get("content", ""))[:100],
                        "assistant_response_preview": str(value.get("assistant_response", {}).get("content", ""))[:100],
                        "timestamp": value.get("timestamp", ""),
                    },
                    "importance": self._get_memory_importance(key),
                })
                
        return results
        
    def _get_memory_importance(self, key: str) -> float:
        """获取记忆的重要性"""
        # 这里应该查询实际的记忆条目
        # 暂时返回默认值
        return 3.0
        
    async def train(self, training_data: List[Dict[str, Any]]) -> None:
        """训练智能体
        
        Args:
            training_data: 训练数据
        """
        print(f"开始训练智能体 {self.name}，数据量: {len(training_data)}")
        
        # 将训练数据存储到记忆
        for i, data in enumerate(training_data):
            memory_key = f"training_{i}_{datetime.now().timestamp()}"
            self.memory.store(
                key=memory_key,
                value=data,
                importance=8.0,  # 训练数据重要性较高
            )
            
        print(f"训练数据已存储到记忆")
        
    async def evaluate(self, test_data: List[Dict[str, Any]]) -> Dict[str, float]:
        """评估智能体性能
        
        Args:
            test_data: 测试数据
            
        Returns:
            评估指标
        """
        print(f"开始评估智能体 {self.name}，测试数据量: {len(test_data)}")
        
        # 简化评估逻辑
        correct_count = 0
        total_time = 0
        
        for test_item in test_data:
            start_time = datetime.now()
            
            # 创建测试上下文
            context = self.create_context(
                user_id="test_user",
                channel="test",
                request_data=test_item,
            )
            
            # 处理测试消息
            try:
                response = await self.process_message_with_context(
                    context,
                    test_item.get("message", {}),
                )
                
                # 检查响应是否正确（简化逻辑）
                if response and "content" in response:
                    correct_count += 1
                    
            except Exception as e:
                print(f"测试处理失败: {e}")
                
            end_time = datetime.now()
            total_time += (end_time - start_time).total_seconds()
            
        # 计算指标
        accuracy = correct_count / len(test_data) if test_data else 0
        avg_response_time = total_time / len(test_data) if test_data else 0
        
        return {
            "accuracy": accuracy,
            "avg_response_time": avg_response_time,
            "test_count": len(test_data),
            "correct_count": correct_count,
        }
        
    def get_detailed_status(self) -> Dict[str, Any]:
        """获取详细状态"""
        base_status = super().get_status()
        
        # 添加上下文管理器统计
        context_stats = self.context_manager.get_statistics()
        
        # 添加插件信息
        plugin_info = {
            "total_plugins": len(self.plugin_manager.plugins),
            "enabled_plugins": len(self.plugin_manager.message_pipeline),
            "plugin_list": self.plugin_manager.list_plugins(),
        }
        
        # 添加记忆使用情况
        memory_usage = self.memory.get_usage()
        
        return {
            **base_status,
            "context_stats": context_stats,
            "plugin_info": plugin_info,
            "memory_usage": memory_usage,
            "session_count": self.session_count,
        }