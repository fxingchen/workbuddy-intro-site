"""
插件系统

提供插件管理器和插件接口，支持动态加载和卸载插件。
"""

from typing import Dict, Any, Optional, List, Type, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
import importlib
import inspect


@dataclass
class PluginConfig:
    """插件配置"""
    name: str
    enabled: bool = True
    priority: int = 50
    config: Dict[str, Any] = field(default_factory=dict)


class PluginInterface(ABC):
    """插件接口
    
    所有插件必须实现此接口。
    """
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """初始化插件
        
        Args:
            config: 插件配置
        """
        pass
        
    @abstractmethod
    async def handle_message(self, context: Any, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """处理消息
        
        Args:
            context: 对话上下文
            message: 消息数据
            
        Returns:
            处理后的响应消息，如果不处理则返回None
        """
        pass
        
    @abstractmethod
    async def shutdown(self) -> None:
        """关闭插件，清理资源"""
        pass


class PluginManager:
    """插件管理器
    
    负责插件的加载、管理和消息处理路由。
    """
    
    def __init__(self):
        self.plugins: Dict[str, PluginInterface] = {}
        self.plugin_configs: Dict[str, PluginConfig] = {}
        self.message_pipeline: List[PluginInterface] = []
        self.loaded_at = datetime.now()
        
    def register_plugin(self, plugin: PluginInterface, config: PluginConfig) -> None:
        """注册插件
        
        Args:
            plugin: 插件实例
            config: 插件配置
        """
        plugin_name = config.name
        
        if plugin_name in self.plugins:
            print(f"警告: 插件 {plugin_name} 已注册，将被覆盖")
            
        # 初始化插件
        try:
            plugin.initialize(config.config)
            self.plugins[plugin_name] = plugin
            self.plugin_configs[plugin_name] = config
            
            # 按优先级排序插入到处理管道
            self._update_message_pipeline()
            
            print(f"插件 {plugin_name} 注册成功 (优先级: {config.priority})")
            
        except Exception as e:
            print(f"插件 {plugin_name} 初始化失败: {e}")
            
    def _update_message_pipeline(self) -> None:
        """更新消息处理管道，按优先级排序"""
        # 过滤启用的插件
        enabled_plugins = [
            (name, plugin, config)
            for name, plugin in self.plugins.items()
            if self.plugin_configs[name].enabled
        ]
        
        # 按优先级降序排序（优先级高的先处理）
        enabled_plugins.sort(key=lambda x: x[2].priority, reverse=True)
        
        # 更新管道
        self.message_pipeline = [plugin for _, plugin, _ in enabled_plugins]
        
    def load_plugin_from_module(self, module_path: str, config: PluginConfig) -> bool:
        """从模块路径加载插件
        
        Args:
            module_path: 模块路径，如 'plugins.message_processor'
            config: 插件配置
            
        Returns:
            加载是否成功
        """
        try:
            # 导入模块
            module = importlib.import_module(module_path)
            
            # 查找实现了PluginInterface的类
            plugin_class = None
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    issubclass(obj, PluginInterface) and 
                    obj != PluginInterface):
                    plugin_class = obj
                    break
                    
            if not plugin_class:
                print(f"模块 {module_path} 中没有找到有效的插件类")
                return False
                
            # 创建插件实例
            plugin_instance = plugin_class()
            
            # 注册插件
            self.register_plugin(plugin_instance, config)
            return True
            
        except Exception as e:
            print(f"从模块 {module_path} 加载插件失败: {e}")
            return False
            
    def enable_plugin(self, plugin_name: str) -> bool:
        """启用插件
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            操作是否成功
        """
        if plugin_name not in self.plugin_configs:
            print(f"插件 {plugin_name} 不存在")
            return False
            
        self.plugin_configs[plugin_name].enabled = True
        self._update_message_pipeline()
        print(f"插件 {plugin_name} 已启用")
        return True
        
    def disable_plugin(self, plugin_name: str) -> bool:
        """禁用插件
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            操作是否成功
        """
        if plugin_name not in self.plugin_configs:
            print(f"插件 {plugin_name} 不存在")
            return False
            
        self.plugin_configs[plugin_name].enabled = False
        self._update_message_pipeline()
        print(f"插件 {plugin_name} 已禁用")
        return True
        
    def set_plugin_priority(self, plugin_name: str, priority: int) -> bool:
        """设置插件优先级
        
        Args:
            plugin_name: 插件名称
            priority: 新的优先级（越大越先处理）
            
        Returns:
            操作是否成功
        """
        if plugin_name not in self.plugin_configs:
            print(f"插件 {plugin_name} 不存在")
            return False
            
        self.plugin_configs[plugin_name].priority = priority
        self._update_message_pipeline()
        print(f"插件 {plugin_name} 优先级已设置为 {priority}")
        return True
        
    async def process_message(self, context: Any, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """通过插件管道处理消息
        
        Args:
            context: 对话上下文
            message: 消息数据
            
        Returns:
            处理后的响应消息
        """
        for plugin in self.message_pipeline:
            try:
                response = await plugin.handle_message(context, message)
                if response:
                    return response
            except Exception as e:
                print(f"插件 {plugin.__class__.__name__} 处理消息时出错: {e}")
                
        return None
        
    async def shutdown_all(self) -> None:
        """关闭所有插件"""
        print(f"正在关闭 {len(self.plugins)} 个插件...")
        
        for plugin_name, plugin in self.plugins.items():
            try:
                await plugin.shutdown()
                print(f"插件 {plugin_name} 已关闭")
            except Exception as e:
                print(f"关闭插件 {plugin_name} 时出错: {e}")
                
    def get_plugin_status(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """获取插件状态
        
        Args:
            plugin_name: 插件名称
            
        Returns:
            插件状态信息
        """
        if plugin_name not in self.plugins:
            return None
            
        config = self.plugin_configs[plugin_name]
        return {
            "name": plugin_name,
            "enabled": config.enabled,
            "priority": config.priority,
            "config": config.config,
            "class": self.plugins[plugin_name].__class__.__name__,
        }
        
    def list_plugins(self) -> List[Dict[str, Any]]:
        """列出所有插件"""
        plugins = []
        for plugin_name, plugin in self.plugins.items():
            config = self.plugin_configs[plugin_name]
            plugins.append({
                "name": plugin_name,
                "enabled": config.enabled,
                "priority": config.priority,
                "class": plugin.__class__.__name__,
            })
            
        return plugins
        
    def get_pipeline_order(self) -> List[str]:
        """获取消息处理管道的顺序"""
        return [plugin.__class__.__name__ for plugin in self.message_pipeline]


class BasePlugin(PluginInterface):
    """基础插件
    
    为插件开发提供便利的基础类。
    """
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.config: Dict[str, Any] = {}
        self.initialized = False
        
    def initialize(self, config: Dict[str, Any]) -> None:
        """初始化插件
        
        Args:
            config: 插件配置
        """
        self.config = config
        self.initialized = True
        print(f"插件 {self.name} 初始化完成")
        
    async def handle_message(self, context: Any, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """处理消息（子类应该重写此方法）
        
        Args:
            context: 对话上下文
            message: 消息数据
            
        Returns:
            处理后的响应消息
        """
        # 基类不做任何处理
        return None
        
    async def shutdown(self) -> None:
        """关闭插件"""
        print(f"插件 {self.name} 正在关闭...")
        
    def log(self, level: str, message: str, **kwargs) -> None:
        """记录日志
        
        Args:
            level: 日志级别（info, warning, error）
            message: 日志消息
            **kwargs: 额外参数
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level.upper()}] {self.name}: {message}"
        
        if kwargs:
            log_message += f" {kwargs}"
            
        print(log_message)