"""
插件模块

提供各种扩展插件，增强智能体功能。
"""

from .message_processor import MessageProcessorPlugin
from .workflow_engine import WorkflowEnginePlugin
from .skill_library import SkillLibraryPlugin

__all__ = [
    'MessageProcessorPlugin',
    'WorkflowEnginePlugin',
    'SkillLibraryPlugin',
]