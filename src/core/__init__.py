"""
ClawHub核心框架模块

提供智能体框架的基础组件，包括：
- 智能体基类
- 插件管理器
- 上下文管理
- 记忆存储
"""

from .agent import BaseAgent, AgentConfig
from .plugin import PluginInterface, PluginManager
from .context import Context, Session, User
from .memory import Memory, ShortTermMemory, LongTermMemory

__all__ = [
    'BaseAgent',
    'AgentConfig',
    'PluginInterface',
    'PluginManager',
    'Context',
    'Session',
    'User',
    'Memory',
    'ShortTermMemory',
    'LongTermMemory',
]