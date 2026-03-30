"""
飞书智能体

专门用于飞书平台集成的智能体实现。
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import json

from .base_agent import BaseAgent, AgentConfig
from ..core.context import Context
from ..feishu.client import FeishuClient, FeishuConfig
from ..feishu.webhook import WebhookHandler, WebhookEvent


class FeishuAgent(BaseAgent):
    """飞书智能体
    
    专门用于飞书平台，集成飞书API和Webhook处理。
    """
    
    def __init__(
        self,
        config: AgentConfig,
        feishu_config: FeishuConfig,
    ):
        """
        初始化飞书智能体
        
        Args:
            config: 智能体配置
            feishu_config: 飞书配置
        """
        # 确保智能体名称包含飞书标识
        if not config.name.endswith("(飞书)"):
            config.name = f"{config.name} (飞书)"
            
        super().__init__(config)
        
        # 飞书相关组件
        self.feishu_config = feishu_config
        self.feishu_client = FeishuClient(feishu_config)
        self.webhook_handler = WebhookHandler(self.feishu_client)
        
        # 飞书特定状态
        self.feishu_stats = {
            "messages_received": 0,
            "messages_sent": 0,
            "webhook_events": 0,
            "api_calls": 0,
            "errors": 0,
        }
        
        # 注册飞书特定的事件处理器
        self.register_handler("feishu_message", self._handle_feishu_message)
        self.register_handler("feishu_event", self._handle_feishu_event)
        
    async def initialize(self) -> None:
        """初始化飞书智能体"""
        await super().initialize()
        
        # 初始化飞书客户端
        try:
            # 获取访问令牌
            await self.feishu_client.get_access_token()
            print(f"飞书智能体 {self.name} 初始化成功")
        except Exception as e:
            print(f"飞书智能体初始化失败: {e}")
            
    async def handle_feishu_webhook(
        self,
        signature: str,
        timestamp: str,
        nonce: str,
        encrypted_message: str,
    ) -> Dict[str, Any]:
        """处理飞书Webhook请求
        
        Args:
            signature: 签名
            timestamp: 时间戳
            nonce: 随机数
            encrypted_message: 加密消息
            
        Returns:
            Webhook响应
        """
        self.feishu_stats["webhook_events"] += 1
        
        try:
            # 解密和验证消息
            decrypted_message = await self.feishu_client.receive_webhook(
                signature=signature,
                timestamp=timestamp,
                nonce=nonce,
                encrypted_message=encrypted_message,
            )
            
            # 解析Webhook事件
            event = WebhookEvent(**decrypted_message)
            
            # 触发飞书事件
            await self.trigger_event("feishu_event", {
                "event": event,
                "timestamp": datetime.now(),
            })
            
            # 处理不同类型的事件
            response = None
            
            if event.type == "url_verification":
                # URL验证事件
                response = {"challenge": event.challenge}
                
            elif event.type == "event_callback":
                # 事件回调
                if event.event.get("type") == "message":
                    # 消息事件
                    response = await self._handle_message_event(event)
                    
            return response or {}
            
        except Exception as e:
            self.feishu_stats["errors"] += 1
            await self.trigger_event("error", {
                "context": {"source": "feishu_webhook"},
                "error": e,
                "timestamp": datetime.now(),
            })
            raise
            
    async def _handle_message_event(self, event: WebhookEvent) -> Dict[str, Any]:
        """处理消息事件
        
        Args:
            event: Webhook事件
            
        Returns:
            处理结果
        """
        event_data = event.event
        sender = event_data.get("sender", {})
        message = event_data.get("message", {})
        
        # 创建上下文
        context = self.create_context(
            user_id=sender.get("sender_id", {}).get("user_id", "unknown"),
            channel="feishu",
            request_data={
                "event": event.dict(),
                "message_id": message.get("message_id"),
                "chat_id": message.get("chat_id"),
                "root_id": message.get("root_id"),
                "parent_id": message.get("parent_id"),
            },
            user_info={
                "user_id": sender.get("sender_id", {}).get("user_id"),
                "username": sender.get("sender_id", {}).get("open_id"),
                "nickname": sender.get("sender", {}).get("name"),
            },
        )
        
        # 提取消息内容
        message_content = self._extract_message_content(message)
        
        # 触发飞书消息事件
        await self.trigger_event("feishu_message", {
            "context": context,
            "message": message_content,
            "event": event,
            "timestamp": datetime.now(),
        })
        
        # 处理消息
        response = await self.process_message_with_context(context, message_content)
        
        # 如果生成了响应，发送回飞书
        if response:
            await self.send_feishu_response(
                receive_id=message.get("chat_id") or sender.get("sender_id", {}).get("open_id"),
                response=response,
                message_id=message.get("message_id"),
            )
            
        return {}
        
    def _extract_message_content(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """从飞书消息中提取内容
        
        Args:
            message: 飞书消息
            
        Returns:
            标准化的消息内容
        """
        message_type = message.get("message_type", "text")
        content_str = message.get("content", "{}")
        
        try:
            content_data = json.loads(content_str)
        except json.JSONDecodeError:
            content_data = {"text": content_str}
            
        # 标准化消息格式
        standardized_message = {
            "type": message_type,
            "content": content_data.get("text", ""),
            "raw_content": content_data,
            "message_id": message.get("message_id"),
            "timestamp": message.get("create_time"),
        }
        
        # 处理富文本消息
        if message_type == "post":
            # 解析飞书富文本
            standardized_message["content"] = self._parse_post_content(content_data)
            
        return standardized_message
        
    def _parse_post_content(self, post_data: Dict[str, Any]) -> str:
        """解析飞书富文本内容
        
        Args:
            post_data: 富文本数据
            
        Returns:
            提取的文本内容
        """
        # 简化解析，提取所有文本内容
        text_parts = []
        
        # 尝试从富文本中提取文字
        content = post_data.get("content", [])
        for item in content:
            if isinstance(item, dict):
                # 提取文本元素
                text = item.get("text", "")
                if text:
                    text_parts.append(text.strip())
                    
        return " ".join(text_parts) if text_parts else "[富文本消息]"
        
    async def send_feishu_response(
        self,
        receive_id: str,
        response: Dict[str, Any],
        message_id: Optional[str] = None,
    ) -> bool:
        """发送响应到飞书
        
        Args:
            receive_id: 接收者ID（用户open_id或群聊chat_id）
            response: 响应消息
            message_id: 原消息ID（用于回复）
            
        Returns:
            发送是否成功
        """
        try:
            # 准备飞书消息格式
            feishu_message = self._prepare_feishu_message(response, message_id)
            
            # 发送消息
            result = await self.feishu_client.send_message(
                receive_id=receive_id,
                msg_type=feishu_message["msg_type"],
                content=feishu_message["content"],
            )
            
            if result and result.get("code") == 0:
                self.feishu_stats["messages_sent"] += 1
                self.feishu_stats["api_calls"] += 1
                return True
            else:
                self.feishu_stats["errors"] += 1
                print(f"发送飞书消息失败: {result}")
                return False
                
        except Exception as e:
            self.feishu_stats["errors"] += 1
            print(f"发送飞书消息异常: {e}")
            return False
            
    def _prepare_feishu_message(
        self,
        response: Dict[str, Any],
        message_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """准备飞书消息格式
        
        Args:
            response: 标准响应消息
            message_id: 原消息ID
            
        Returns:
            飞书API格式的消息
        """
        msg_type = response.get("type", "text")
        content = response.get("content", "")
        
        # 构建飞书消息内容
        if msg_type == "text":
            feishu_content = {"text": str(content)}
        elif msg_type == "card":
            # 卡片消息
            feishu_content = content if isinstance(content, dict) else {"config": {}, "elements": []}
            msg_type = "interactive"
        else:
            # 默认文本消息
            feishu_content = {"text": str(content)}
            msg_type = "text"
            
        # 添加回复信息
        if message_id:
            if msg_type == "text":
                feishu_content["text"] = f"{feishu_content['text']}"
            # 飞书API需要额外参数来回复消息
            
        return {
            "msg_type": msg_type,
            "content": json.dumps(feishu_content, ensure_ascii=False),
        }
        
    async def _handle_feishu_message(
        self,
        context: Context,
        message: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """飞书消息处理器
        
        Args:
            context: 对话上下文
            message: 消息数据
            
        Returns:
            响应消息
        """
        # 飞书特定的消息处理逻辑
        content = message.get("content", "").lower()
        
        # 飞书特定的命令处理
        if content.startswith("/"):
            command = content[1:].split()[0] if content[1:] else ""
            
            if command == "help":
                return {
                    "content": (
                        f"我是{self.name}，支持以下命令：\n"
                        "• /help - 显示帮助信息\n"
                        "• /status - 查看智能体状态\n"
                        "• /history - 查看对话历史\n"
                        "• /clear - 清空当前对话\n"
                        "• /feedback - 提供反馈"
                    ),
                    "type": "text",
                }
                
            elif command == "status":
                status = self.get_detailed_status()
                status_text = (
                    f"智能体状态：\n"
                    f"名称：{status['name']}\n"
                    f"运行时间：{status['uptime']:.1f}秒\n"
                    f"消息处理：{status['stats']['messages_processed']}条\n"
                    f"飞书消息：接收{self.feishu_stats['messages_received']}/发送{self.feishu_stats['messages_sent']}\n"
                    f"插件数量：{status['plugin_info']['enabled_plugins']}个"
                )
                return {"content": status_text, "type": "text"}
                
            elif command == "history":
                history = await self.get_session_history(
                    context.session.session_id,
                    limit=5,
                )
                
                if history:
                    history_text = "最近5条对话：\n"
                    for msg in history[-5:]:
                        role = "用户" if msg.get("role") == "user" else "助手"
                        preview = str(msg.get("content", ""))[:30]
                        history_text += f"• {role}: {preview}...\n"
                else:
                    history_text = "暂无对话历史"
                    
                return {"content": history_text, "type": "text"}
                
            elif command == "clear":
                context.session.clear_history()
                return {"content": "对话历史已清空", "type": "text"}
                
            elif command == "feedback":
                return {
                    "content": "感谢您的反馈！您可以通过以下方式联系我们：\n• 发送邮件到 feedback@clawhub.ai\n• 在GitHub提交Issue",
                    "type": "text",
                }
                
        # 默认处理逻辑
        return None
        
    async def _handle_feishu_event(self, event_data: Dict[str, Any]) -> None:
        """飞书事件处理器
        
        Args:
            event_data: 事件数据
        """
        event = event_data.get("event")
        if not event:
            return
            
        event_type = event.type
        print(f"处理飞书事件: {event_type}")
        
        # 记录事件到记忆
        self.memory.store(
            key=f"feishu_event_{event_type}_{datetime.now().timestamp()}",
            value=event.dict(),
            importance=1.0,
        )
        
    def get_feishu_status(self) -> Dict[str, Any]:
        """获取飞书相关状态
        
        Returns:
            飞书状态信息
        """
        return {
            **self.feishu_stats,
            "app_id": self.feishu_config.app_id,
            "base_url": self.feishu_config.base_url,
            "has_token": bool(self.feishu_client.access_token),
        }
        
    async def send_test_message(self, receive_id: str, message: str = "测试消息") -> bool:
        """发送测试消息
        
        Args:
            receive_id: 接收者ID
            message: 测试消息
            
        Returns:
            发送是否成功
        """
        test_response = {
            "content": f"{message} - 来自 {self.name}",
            "type": "text",
        }
        
        return await self.send_feishu_response(receive_id, test_response)
        
    async def broadcast_message(
        self,
        department_ids: List[str],
        message: Dict[str, Any],
    ) -> Dict[str, Any]:
        """广播消息到部门
        
        Args:
            department_ids: 部门ID列表
            message: 消息内容
            
        Returns:
            发送结果
        """
        results = {}
        
        for dept_id in department_ids:
            try:
                # 这里应该调用飞书的部门消息API
                # 暂时使用简化实现
                success = await self.send_feishu_response(
                    receive_id=dept_id,
                    response=message,
                )
                results[dept_id] = {
                    "success": success,
                    "timestamp": datetime.now().isoformat(),
                }
            except Exception as e:
                results[dept_id] = {
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
                
        return results