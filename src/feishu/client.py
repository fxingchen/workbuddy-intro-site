"""飞书API客户端封装"""
from typing import Dict, Any, Optional
from dataclasses import dataclass
import httpx
import json
import time
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@dataclass
class FeishuConfig:
    """飞书配置"""
    app_id: str
    app_secret: str
    verification_token: str
    encrypt_key: Optional[str] = None
    base_url: str = "https://open.feishu.cn"

class FeishuClient:
    """飞书API客户端"""
    
    def __init__(self, config: FeishuConfig):
        self.config = config
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def get_access_token(self) -> str:
        """获取访问令牌"""
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at - timedelta(minutes=5):
                return self.access_token
        
        url = f"{self.config.base_url}/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.config.app_id,
            "app_secret": self.config.app_secret
        }
        
        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                self.access_token = data["tenant_access_token"]
                expire_time = data.get("expire", 7200)
                self.token_expires_at = datetime.now() + timedelta(seconds=expire_time)
                logger.info("成功获取飞书访问令牌")
                return self.access_token
            else:
                raise Exception(f"获取令牌失败: {data.get('msg')}")
                
        except Exception as e:
            logger.error(f"获取飞书访问令牌失败: {e}")
            raise
    
    async def send_message(self, 
                          receive_id: str,
                          msg_type: str,
                          content: Dict[str, Any]) -> Dict[str, Any]:
        """发送消息到飞书"""
        token = await self.get_access_token()
        
        url = f"{self.config.base_url}/open-apis/im/v1/messages"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": json.dumps(content, ensure_ascii=False)
        }
        
        try:
            response = await self.client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                logger.info(f"消息发送成功: {receive_id}")
                return data
            else:
                raise Exception(f"消息发送失败: {data.get('msg')}")
                
        except Exception as e:
            logger.error(f"发送飞书消息失败: {e}")
            raise
    
    async def send_text_message(self, receive_id: str, text: str) -> Dict[str, Any]:
        """发送文本消息"""
        content = {"text": text}
        return await self.send_message(receive_id, "text", content)
    
    async def send_card_message(self, receive_id: str, card_config: Dict[str, Any]) -> Dict[str, Any]:
        """发送卡片消息"""
        return await self.send_message(receive_id, "interactive", card_config)
    
    async def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """获取用户信息"""
        token = await self.get_access_token()
        
        url = f"{self.config.base_url}/open-apis/contact/v3/users/{user_id}"
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = await self.client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") == 0:
                return data.get("data", {}).get("user", {})
            else:
                raise Exception(f"获取用户信息失败: {data.get('msg')}")
                
        except Exception as e:
            logger.error(f"获取飞书用户信息失败: {e}")
            raise
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()