"""飞书Webhook处理器"""
from typing import Dict, Any, Optional
import hashlib
import json
import logging
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class WebhookEvent(BaseModel):
    """Webhook事件模型"""
    challenge: Optional[str] = None
    token: str
    type: str
    event: Dict[str, Any]

class MessageEvent(BaseModel):
    """消息事件模型"""
    sender: Dict[str, Any]
    message: Dict[str, Any]
    chat_type: str = Field(alias="chat_type")
    chat_id: str = Field(alias="chat_id")

class WebhookHandler:
    """Webhook处理器"""
    
    def __init__(self, verification_token: str, encrypt_key: Optional[str] = None):
        self.verification_token = verification_token
        self.encrypt_key = encrypt_key
    
    def verify_signature(self, 
                        signature: str,
                        timestamp: str,
                        nonce: str,
                        body: str) -> bool:
        """验证飞书签名"""
        if not self.verification_token:
            logger.warning("未配置验证令牌，跳过签名验证")
            return True
        
        # 构造签名字符串
        sign_string = f"{timestamp}\n{nonce}\n{body}"
        
        # 计算签名
        import base64
        import hmac
        
        key = self.verification_token.encode('utf-8')
        message = sign_string.encode('utf-8')
        
        sign = base64.b64encode(
            hmac.new(key, message, digestmod=hashlib.sha256).digest()
        ).decode('utf-8')
        
        return signature == sign
    
    def decrypt_event(self, encrypted_data: str) -> Dict[str, Any]:
        """解密事件数据"""
        if not self.encrypt_key:
            return json.loads(encrypted_data)
        
        # 这里需要实现飞书的事件解密逻辑
        # 实际实现需要使用飞书的加密算法
        logger.warning("事件解密功能未实现，返回原始数据")
        return json.loads(encrypted_data)
    
    async def handle_url_verification(self, event: WebhookEvent) -> Dict[str, Any]:
        """处理URL验证事件"""
        if event.challenge:
            logger.info("处理URL验证请求")
            return {"challenge": event.challenge}
        return {"error": "无效的验证请求"}
    
    async def handle_message_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """处理消息事件"""
        try:
            message_event = MessageEvent(**event)
            logger.info(f"收到消息事件: {message_event.chat_type} chat, sender: {message_event.sender.get('sender_id', {}).get('open_id')}")
            
            # 提取消息内容
            message = message_event.message
            message_type = message.get("message_type", "")
            content = message.get("content", "")
            
            # 解析消息内容
            if message_type == "text":
                try:
                    content_dict = json.loads(content)
                    text_content = content_dict.get("text", "")
                    logger.info(f"文本消息内容: {text_content}")
                    return {
                        "type": "message",
                        "chat_type": message_event.chat_type,
                        "chat_id": message_event.chat_id,
                        "user_id": message_event.sender.get("sender_id", {}).get("open_id"),
                        "content": text_content,
                        "message_id": message.get("message_id")
                    }
                except json.JSONDecodeError:
                    logger.error(f"解析消息内容失败: {content}")
            
            return {"type": "message", "status": "processed"}
            
        except Exception as e:
            logger.error(f"处理消息事件失败: {e}")
            return {"error": str(e)}
    
    async def handle_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理Webhook事件"""
        try:
            event = WebhookEvent(**event_data)
            
            if event.type == "url_verification":
                return await self.handle_url_verification(event)
            
            elif event.type == "event_callback":
                event_type = event.event.get("type", "")
                
                if event_type == "im.message.receive_v1":
                    return await self.handle_message_event(event.event)
                
                else:
                    logger.info(f"收到未知事件类型: {event_type}")
                    return {"type": event_type, "status": "ignored"}
            
            else:
                logger.warning(f"未知的事件类型: {event.type}")
                return {"error": f"未知的事件类型: {event.type}"}
                
        except Exception as e:
            logger.error(f"处理Webhook事件失败: {e}")
            return {"error": str(e)}