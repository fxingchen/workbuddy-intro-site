"""
上下文管理系统

管理对话上下文，包括会话、用户信息和对话历史。
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class User:
    """用户信息"""
    user_id: str
    username: Optional[str] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)
    
    def update_last_seen(self) -> None:
        """更新最后访问时间"""
        self.last_seen = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "nickname": self.nickname,
            "avatar": self.avatar,
            "email": self.email,
            "phone": self.phone,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "last_seen": self.last_seen.isoformat(),
        }


@dataclass
class Session:
    """会话信息"""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    channel: str = ""  # 渠道，如：feishu, wechat, web
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    message_history: List[Dict[str, Any]] = field(default_factory=list)
    max_history_length: int = 50
    
    def add_message(self, message: Dict[str, Any]) -> None:
        """添加消息到历史
        
        Args:
            message: 消息数据
        """
        message_with_timestamp = {
            **message,
            "timestamp": datetime.now().isoformat(),
        }
        
        self.message_history.append(message_with_timestamp)
        self.updated_at = datetime.now()
        
        # 保持历史长度限制
        if len(self.message_history) > self.max_history_length:
            self.message_history = self.message_history[-self.max_history_length:]
            
    def get_recent_messages(self, count: int = 10) -> List[Dict[str, Any]]:
        """获取最近的几条消息
        
        Args:
            count: 消息数量
            
        Returns:
            消息列表
        """
        return self.message_history[-count:] if self.message_history else []
        
    def clear_history(self) -> None:
        """清空消息历史"""
        self.message_history.clear()
        self.updated_at = datetime.now()
        
    def deactivate(self) -> None:
        """停用会话"""
        self.active = False
        self.updated_at = datetime.now()
        
    def reactivate(self) -> None:
        """重新激活会话"""
        self.active = True
        self.updated_at = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "channel": self.channel,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "active": self.active,
            "metadata": self.metadata,
            "message_count": len(self.message_history),
            "message_history": self.message_history,
        }


class Context:
    """对话上下文
    
    封装对话的上下文信息，为智能体提供完整的对话环境。
    """
    
    def __init__(
        self,
        session: Session,
        user: Optional[User] = None,
        request_data: Optional[Dict[str, Any]] = None,
    ):
        """
        初始化上下文
        
        Args:
            session: 会话信息
            user: 用户信息（可选）
            request_data: 原始请求数据（可选）
        """
        self.session = session
        self.user = user
        self.request_data = request_data or {}
        self.context_data: Dict[str, Any] = {}
        self.created_at = datetime.now()
        
        # 默认上下文数据
        self.context_data["timestamp"] = self.created_at.isoformat()
        self.context_data["session_id"] = session.session_id
        if user:
            self.context_data["user_id"] = user.user_id
            
    def set_data(self, key: str, value: Any) -> None:
        """设置上下文数据
        
        Args:
            key: 数据键
            value: 数据值
        """
        self.context_data[key] = value
        
    def get_data(self, key: str, default: Any = None) -> Any:
        """获取上下文数据
        
        Args:
            key: 数据键
            default: 默认值
            
        Returns:
            数据值
        """
        return self.context_data.get(key, default)
        
    def remove_data(self, key: str) -> None:
        """移除上下文数据
        
        Args:
            key: 数据键
        """
        if key in self.context_data:
            del self.context_data[key]
            
    def add_message_to_history(self, message: Dict[str, Any]) -> None:
        """添加消息到会话历史
        
        Args:
            message: 消息数据
        """
        self.session.add_message(message)
        
    def get_conversation_history(self, count: int = 10) -> List[Dict[str, Any]]:
        """获取对话历史
        
        Args:
            count: 消息数量
            
        Returns:
            消息历史列表
        """
        return self.session.get_recent_messages(count)
        
    def update_user_info(self, user_info: Dict[str, Any]) -> None:
        """更新用户信息
        
        Args:
            user_info: 用户信息字典
        """
        if self.user:
            for key, value in user_info.items():
                if hasattr(self.user, key):
                    setattr(self.user, key, value)
                    
    def merge_context(self, other_context: Dict[str, Any]) -> None:
        """合并其他上下文数据
        
        Args:
            other_context: 其他上下文数据
        """
        self.context_data.update(other_context)
        
    def get_context_summary(self) -> Dict[str, Any]:
        """获取上下文摘要
        
        Returns:
            上下文摘要信息
        """
        summary = {
            "context_id": id(self),
            "session": {
                "id": self.session.session_id,
                "channel": self.session.channel,
                "active": self.session.active,
                "message_count": len(self.session.message_history),
            },
            "user": self.user.to_dict() if self.user else None,
            "created_at": self.created_at.isoformat(),
            "data_keys": list(self.context_data.keys()),
        }
        
        # 添加最近的消息摘要
        recent_messages = self.get_conversation_history(3)
        summary["recent_messages"] = [
            {
                "type": msg.get("type", "unknown"),
                "timestamp": msg.get("timestamp"),
                "content_preview": str(msg.get("content", ""))[:50] + "..." 
                if len(str(msg.get("content", ""))) > 50 
                else msg.get("content", "")
            }
            for msg in recent_messages
        ]
        
        return summary
        
    def create_child_context(self, extra_data: Dict[str, Any] = None) -> 'Context':
        """创建子上下文
        
        Args:
            extra_data: 额外的上下文数据
            
        Returns:
            新的上下文实例
        """
        child_context = Context(
            session=self.session,
            user=self.user,
            request_data=self.request_data.copy(),
        )
        
        # 复制当前上下文数据
        child_context.context_data = self.context_data.copy()
        
        # 添加额外的数据
        if extra_data:
            child_context.context_data.update(extra_data)
            
        return child_context
        
    def __str__(self) -> str:
        """字符串表示"""
        user_str = f"User({self.user.user_id})" if self.user else "Anonymous"
        return f"Context(session={self.session.session_id}, user={user_str}, data={len(self.context_data)} items)"


class ContextManager:
    """上下文管理器
    
    管理上下文的创建、存储和检索。
    """
    
    def __init__(self):
        self.contexts: Dict[str, Context] = {}
        self.sessions: Dict[str, Session] = {}
        self.users: Dict[str, User] = {}
        
    def create_session(
        self,
        user_id: str,
        channel: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Session:
        """创建新会话
        
        Args:
            user_id: 用户ID
            channel: 渠道标识
            metadata: 会话元数据
            
        Returns:
            新创建的会话
        """
        session = Session(
            user_id=user_id,
            channel=channel,
            metadata=metadata or {},
        )
        
        self.sessions[session.session_id] = session
        return session
        
    def get_or_create_user(self, user_id: str, **kwargs) -> User:
        """获取或创建用户
        
        Args:
            user_id: 用户ID
            **kwargs: 用户属性
            
        Returns:
            用户对象
        """
        if user_id in self.users:
            user = self.users[user_id]
            # 更新用户信息
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            user.update_last_seen()
            return user
            
        # 创建新用户
        user = User(user_id=user_id, **kwargs)
        self.users[user_id] = user
        return user
        
    def create_context(
        self,
        session_id: str,
        user_id: str,
        channel: str,
        request_data: Optional[Dict[str, Any]] = None,
        user_info: Optional[Dict[str, Any]] = None,
    ) -> Context:
        """创建新上下文
        
        Args:
            session_id: 会话ID（如果为None则创建新会话）
            user_id: 用户ID
            channel: 渠道标识
            request_data: 请求数据
            user_info: 用户信息
            
        Returns:
            新创建的上下文
        """
        # 获取或创建会话
        if session_id and session_id in self.sessions:
            session = self.sessions[session_id]
            session.reactivate()
        else:
            session = self.create_session(user_id, channel)
            
        # 获取或创建用户
        user = self.get_or_create_user(user_id, **(user_info or {}))
        
        # 创建上下文
        context = Context(session, user, request_data)
        context_key = f"{session.session_id}_{datetime.now().timestamp()}"
        self.contexts[context_key] = context
        
        return context
        
    def get_context(self, context_key: str) -> Optional[Context]:
        """根据键获取上下文
        
        Args:
            context_key: 上下文键
            
        Returns:
            上下文对象
        """
        return self.contexts.get(context_key)
        
    def get_session(self, session_id: str) -> Optional[Session]:
        """获取会话
        
        Args:
            session_id: 会话ID
            
        Returns:
            会话对象
        """
        return self.sessions.get(session_id)
        
    def get_user(self, user_id: str) -> Optional[User]:
        """获取用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户对象
        """
        return self.users.get(user_id)
        
    def cleanup_inactive_sessions(self, max_age_hours: int = 24) -> List[str]:
        """清理不活跃的会话
        
        Args:
            max_age_hours: 最大不活跃时间（小时）
            
        Returns:
            被清理的会话ID列表
        """
        cleanup_time = datetime.now()
        cleaned_sessions = []
        
        for session_id, session in list(self.sessions.items()):
            # 检查会话是否不活跃
            age_hours = (cleanup_time - session.updated_at).total_seconds() / 3600
            
            if age_hours > max_age_hours and session.active:
                session.deactivate()
                cleaned_sessions.append(session_id)
                
        return cleaned_sessions
        
    def get_statistics(self) -> Dict[str, Any]:
        """获取管理器统计信息
        
        Returns:
            统计信息字典
        """
        active_sessions = sum(1 for s in self.sessions.values() if s.active)
        
        return {
            "total_contexts": len(self.contexts),
            "total_sessions": len(self.sessions),
            "active_sessions": active_sessions,
            "total_users": len(self.users),
            "average_messages_per_session": (
                sum(len(s.message_history) for s in self.sessions.values()) / len(self.sessions)
                if self.sessions else 0
            ),
        }