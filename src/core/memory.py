"""
记忆存储系统

为智能体提供短期和长期记忆存储能力。
"""

from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import heapq
import json


class MemoryEntry:
    """记忆条目"""
    
    def __init__(self, key: str, value: Any, importance: float = 1.0):
        """
        初始化记忆条目
        
        Args:
            key: 记忆键
            value: 记忆值
            importance: 重要性评分（0-10）
        """
        self.key = key
        self.value = value
        self.importance = max(0.0, min(10.0, importance))  # 限制在0-10之间
        self.created_at = datetime.now()
        self.accessed_at = datetime.now()
        self.access_count = 1
        
    def access(self) -> None:
        """访问记忆，更新访问信息"""
        self.accessed_at = datetime.now()
        self.access_count += 1
        
    def update_importance(self, new_importance: float) -> None:
        """更新重要性评分
        
        Args:
            new_importance: 新的重要性评分
        """
        self.importance = max(0.0, min(10.0, new_importance))
        
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "key": self.key,
            "value": self.value,
            "importance": self.importance,
            "created_at": self.created_at.isoformat(),
            "accessed_at": self.accessed_at.isoformat(),
            "access_count": self.access_count,
            "age_days": (datetime.now() - self.created_at).days,
        }
        
    def __lt__(self, other: 'MemoryEntry') -> bool:
        """小于运算符，用于优先级队列"""
        # 按重要性降序排列（重要性高的优先）
        return self.importance > other.importance


class Memory(ABC):
    """记忆基类
    
    定义记忆存储的基本接口。
    """
    
    @abstractmethod
    def store(self, key: str, value: Any, importance: float = 1.0) -> bool:
        """存储记忆
        
        Args:
            key: 记忆键
            value: 记忆值
            importance: 重要性评分
            
        Returns:
            存储是否成功
        """
        pass
        
    @abstractmethod
    def retrieve(self, key: str) -> Optional[Any]:
        """检索记忆
        
        Args:
            key: 记忆键
            
        Returns:
            记忆值
        """
        pass
        
    @abstractmethod
    def delete(self, key: str) -> bool:
        """删除记忆
        
        Args:
            key: 记忆键
            
        Returns:
            删除是否成功
        """
        pass
        
    @abstractmethod
    def search(self, pattern: str) -> List[Tuple[str, Any]]:
        """搜索记忆
        
        Args:
            pattern: 搜索模式
            
        Returns:
            匹配的记忆键值对列表
        """
        pass
        
    @abstractmethod
    def get_usage(self) -> Dict[str, Any]:
        """获取使用统计
        
        Returns:
            使用统计信息
        """
        pass


class ShortTermMemory(Memory):
    """短期记忆
    
    基于内存的短期记忆存储，有容量限制。
    """
    
    def __init__(self, capacity: int = 100):
        """
        初始化短期记忆
        
        Args:
            capacity: 记忆容量
        """
        self.capacity = capacity
        self.memories: Dict[str, MemoryEntry] = {}
        self.priority_queue: List[MemoryEntry] = []
        self.stats = {
            "stored": 0,
            "retrieved": 0,
            "deleted": 0,
            "evicted": 0,
        }
        
    def store(self, key: str, value: Any, importance: float = 1.0) -> bool:
        """存储记忆
        
        Args:
            key: 记忆键
            value: 记忆值
            importance: 重要性评分
            
        Returns:
            存储是否成功
        """
        # 如果已存在，更新记忆
        if key in self.memories:
            entry = self.memories[key]
            entry.value = value
            entry.update_importance(importance)
            entry.access()
            
            # 更新优先级队列
            self._rebuild_priority_queue()
            return True
            
        # 创建新记忆条目
        entry = MemoryEntry(key, value, importance)
        
        # 如果达到容量限制，需要淘汰最不重要的记忆
        if len(self.memories) >= self.capacity:
            if not self._evict_least_important():
                return False  # 无法淘汰任何记忆
                
        # 存储记忆
        self.memories[key] = entry
        heapq.heappush(self.priority_queue, entry)
        self.stats["stored"] += 1
        
        return True
        
    def _evict_least_important(self) -> bool:
        """淘汰最不重要的记忆
        
        Returns:
            是否成功淘汰
        """
        if not self.priority_queue:
            return False
            
        # 获取最不重要的记忆（堆顶元素）
        while self.priority_queue:
            entry = heapq.heappop(self.priority_queue)
            if entry.key in self.memories:
                # 删除记忆
                del self.memories[entry.key]
                self.stats["evicted"] += 1
                return True
                
        return False
        
    def _rebuild_priority_queue(self) -> None:
        """重建优先级队列"""
        self.priority_queue = list(self.memories.values())
        heapq.heapify(self.priority_queue)
        
    def retrieve(self, key: str) -> Optional[Any]:
        """检索记忆
        
        Args:
            key: 记忆键
            
        Returns:
            记忆值
        """
        if key not in self.memories:
            return None
            
        entry = self.memories[key]
        entry.access()
        self.stats["retrieved"] += 1
        
        return entry.value
        
    def delete(self, key: str) -> bool:
        """删除记忆
        
        Args:
            key: 记忆键
            
        Returns:
            删除是否成功
        """
        if key not in self.memories:
            return False
            
        # 从字典中删除
        del self.memories[key]
        self.stats["deleted"] += 1
        
        # 重建优先级队列（更高效的做法是惰性删除）
        self._rebuild_priority_queue()
        
        return True
        
    def search(self, pattern: str) -> List[Tuple[str, Any]]:
        """搜索记忆
        
        Args:
            pattern: 搜索模式
            
        Returns:
            匹配的记忆键值对列表
        """
        results = []
        
        for key, entry in self.memories.items():
            if pattern.lower() in key.lower():
                results.append((key, entry.value))
            elif isinstance(entry.value, str) and pattern.lower() in entry.value.lower():
                results.append((key, entry.value))
                
        return results
        
    def get_important_memories(self, count: int = 10) -> List[Dict[str, Any]]:
        """获取最重要的记忆
        
        Args:
            count: 数量
            
        Returns:
            记忆信息列表
        """
        # 按重要性排序
        sorted_entries = sorted(
            self.memories.values(),
            key=lambda x: x.importance,
            reverse=True
        )
        
        return [entry.to_dict() for entry in sorted_entries[:count]]
        
    def get_recent_memories(self, count: int = 10) -> List[Dict[str, Any]]:
        """获取最近的记忆
        
        Args:
            count: 数量
            
        Returns:
            记忆信息列表
        """
        # 按最近访问时间排序
        sorted_entries = sorted(
            self.memories.values(),
            key=lambda x: x.accessed_at,
            reverse=True
        )
        
        return [entry.to_dict() for entry in sorted_entries[:count]]
        
    def get_usage(self) -> Dict[str, Any]:
        """获取使用统计
        
        Returns:
            使用统计信息
        """
        total_importance = sum(entry.importance for entry in self.memories.values())
        avg_importance = total_importance / len(self.memories) if self.memories else 0
        
        return {
            "capacity": self.capacity,
            "used": len(self.memories),
            "usage_percentage": (len(self.memories) / self.capacity) * 100 if self.capacity > 0 else 0,
            "average_importance": avg_importance,
            "stats": self.stats,
            "oldest_memory_days": (
                min((datetime.now() - entry.created_at).days for entry in self.memories.values())
                if self.memories else 0
            ),
        }
        
    def clear(self) -> None:
        """清空所有记忆"""
        self.memories.clear()
        self.priority_queue.clear()
        self.stats = {"stored": 0, "retrieved": 0, "deleted": 0, "evicted": 0}


class LongTermMemory(Memory):
    """长期记忆
    
    基于文件的长期记忆存储，无容量限制但可能有性能考虑。
    """
    
    def __init__(self, storage_path: str = "memory_storage.json"):
        """
        初始化长期记忆
        
        Args:
            storage_path: 存储文件路径
        """
        self.storage_path = storage_path
        self.memories: Dict[str, MemoryEntry] = {}
        self.stats = {
            "loaded": 0,
            "stored": 0,
            "retrieved": 0,
            "deleted": 0,
        }
        
        # 加载现有记忆
        self._load_memories()
        
    def _load_memories(self) -> None:
        """从文件加载记忆"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            for key, entry_data in data.items():
                entry = MemoryEntry(
                    key=key,
                    value=entry_data["value"],
                    importance=entry_data["importance"],
                )
                entry.created_at = datetime.fromisoformat(entry_data["created_at"])
                entry.accessed_at = datetime.fromisoformat(entry_data["accessed_at"])
                entry.access_count = entry_data["access_count"]
                
                self.memories[key] = entry
                
            self.stats["loaded"] = len(self.memories)
            
        except FileNotFoundError:
            # 文件不存在，创建空存储
            pass
        except Exception as e:
            print(f"加载长期记忆失败: {e}")
            
    def _save_memories(self) -> bool:
        """保存记忆到文件
        
        Returns:
            保存是否成功
        """
        try:
            data = {}
            for key, entry in self.memories.items():
                data[key] = {
                    "value": entry.value,
                    "importance": entry.importance,
                    "created_at": entry.created_at.isoformat(),
                    "accessed_at": entry.accessed_at.isoformat(),
                    "access_count": entry.access_count,
                }
                
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            return True
            
        except Exception as e:
            print(f"保存长期记忆失败: {e}")
            return False
            
    def store(self, key: str, value: Any, importance: float = 1.0) -> bool:
        """存储记忆
        
        Args:
            key: 记忆键
            value: 记忆值
            importance: 重要性评分
            
        Returns:
            存储是否成功
        """
        # 如果已存在，更新记忆
        if key in self.memories:
            entry = self.memories[key]
            entry.value = value
            entry.update_importance(importance)
            entry.access()
        else:
            # 创建新记忆条目
            entry = MemoryEntry(key, value, importance)
            self.memories[key] = entry
            
        self.stats["stored"] += 1
        
        # 保存到文件
        return self._save_memories()
        
    def retrieve(self, key: str) -> Optional[Any]:
        """检索记忆
        
        Args:
            key: 记忆键
            
        Returns:
            记忆值
        """
        if key not in self.memories:
            return None
            
        entry = self.memories[key]
        entry.access()
        self.stats["retrieved"] += 1
        
        # 更新文件
        self._save_memories()
        
        return entry.value
        
    def delete(self, key: str) -> bool:
        """删除记忆
        
        Args:
            key: 记忆键
            
        Returns:
            删除是否成功
        """
        if key not in self.memories:
            return False
            
        # 从字典中删除
        del self.memories[key]
        self.stats["deleted"] += 1
        
        # 更新文件
        return self._save_memories()
        
    def search(self, pattern: str) -> List[Tuple[str, Any]]:
        """搜索记忆
        
        Args:
            pattern: 搜索模式
            
        Returns:
            匹配的记忆键值对列表
        """
        results = []
        
        for key, entry in self.memories.items():
            if pattern.lower() in key.lower():
                results.append((key, entry.value))
            elif isinstance(entry.value, str) and pattern.lower() in entry.value.lower():
                results.append((key, entry.value))
                
        return results
        
    def cleanup_old_memories(self, max_age_days: int = 365) -> List[str]:
        """清理旧记忆
        
        Args:
            max_age_days: 最大保留天数
            
        Returns:
            被清理的记忆键列表
        """
        cleanup_time = datetime.now()
        cleaned_keys = []
        
        for key, entry in list(self.memories.items()):
            age_days = (cleanup_time - entry.created_at).days
            
            if age_days > max_age_days and entry.importance < 5.0:
                del self.memories[key]
                cleaned_keys.append(key)
                
        # 保存更新
        if cleaned_keys:
            self._save_memories()
            
        return cleaned_keys
        
    def get_usage(self) -> Dict[str, Any]:
        """获取使用统计
        
        Returns:
            使用统计信息
        """
        if not self.memories:
            return {
                "total_memories": 0,
                "storage_path": self.storage_path,
                "stats": self.stats,
            }
            
        total_importance = sum(entry.importance for entry in self.memories.values())
        avg_importance = total_importance / len(self.memories)
        
        # 计算年龄分布
        now = datetime.now()
        age_distribution = {
            "less_than_7_days": 0,
            "7_to_30_days": 0,
            "30_to_90_days": 0,
            "more_than_90_days": 0,
        }
        
        for entry in self.memories.values():
            age_days = (now - entry.created_at).days
            
            if age_days < 7:
                age_distribution["less_than_7_days"] += 1
            elif age_days < 30:
                age_distribution["7_to_30_days"] += 1
            elif age_days < 90:
                age_distribution["30_to_90_days"] += 1
            else:
                age_distribution["more_than_90_days"] += 1
                
        return {
            "total_memories": len(self.memories),
            "storage_path": self.storage_path,
            "average_importance": avg_importance,
            "age_distribution": age_distribution,
            "most_accessed": max(
                self.memories.values(),
                key=lambda x: x.access_count
            ).key if self.memories else None,
            "oldest_memory_days": min(
                (now - entry.created_at).days for entry in self.memories.values()
            ) if self.memories else 0,
            "stats": self.stats,
        }


class HybridMemory(Memory):
    """混合记忆系统
    
    结合短期和长期记忆，提供分层的记忆管理。
    """
    
    def __init__(self, short_term_capacity: int = 100, long_term_path: str = "memory_storage.json"):
        """
        初始化混合记忆
        
        Args:
            short_term_capacity: 短期记忆容量
            long_term_path: 长期记忆存储路径
        """
        self.short_term = ShortTermMemory(short_term_capacity)
        self.long_term = LongTermMemory(long_term_path)
        self.promotion_threshold = 5  # 访问次数达到此阈值时晋升到长期记忆
        
    def store(self, key: str, value: Any, importance: float = 1.0) -> bool:
        """存储记忆
        
        Args:
            key: 记忆键
            value: 记忆值
            importance: 重要性评分
            
        Returns:
            存储是否成功
        """
        # 如果重要性高，直接存储到长期记忆
        if importance >= 8.0:
            return self.long_term.store(key, value, importance)
            
        # 否则先存储到短期记忆
        return self.short_term.store(key, value, importance)
        
    def retrieve(self, key: str) -> Optional[Any]:
        """检索记忆
        
        Args:
            key: 记忆键
            
        Returns:
            记忆值
        """
        # 先在短期记忆中查找
        value = self.short_term.retrieve(key)
        if value is not None:
            # 检查是否需要晋升到长期记忆
            entry = self.short_term.memories.get(key)
            if entry and entry.access_count >= self.promotion_threshold:
                # 晋升到长期记忆
                self.long_term.store(key, value, entry.importance)
                # 从短期记忆中删除
                self.short_term.delete(key)
            return value
            
        # 在长期记忆中查找
        return self.long_term.retrieve(key)
        
    def delete(self, key: str) -> bool:
        """删除记忆
        
        Args:
            key: 记忆键
            
        Returns:
            删除是否成功
        """
        # 尝试从两个存储中删除
        short_term_result = self.short_term.delete(key)
        long_term_result = self.long_term.delete(key)
        
        return short_term_result or long_term_result
        
    def search(self, pattern: str) -> List[Tuple[str, Any]]:
        """搜索记忆
        
        Args:
            pattern: 搜索模式
            
        Returns:
            匹配的记忆键值对列表
        """
        # 搜索两个存储
        short_term_results = self.short_term.search(pattern)
        long_term_results = self.long_term.search(pattern)
        
        # 合并结果，去除重复
        all_results = {}
        for key, value in short_term_results:
            all_results[key] = value
        for key, value in long_term_results:
            if key not in all_results:
                all_results[key] = value
                
        return list(all_results.items())
        
    def promote_to_long_term(self, key: str) -> bool:
        """将记忆从短期晋升到长期
        
        Args:
            key: 记忆键
            
        Returns:
            晋升是否成功
        """
        # 检查记忆是否存在
        if key not in self.short_term.memories:
            return False
            
        entry = self.short_term.memories[key]
        
        # 存储到长期记忆
        success = self.long_term.store(key, entry.value, entry.importance)
        
        # 如果成功，从短期记忆中删除
        if success:
            self.short_term.delete(key)
            
        return success
        
    def demote_to_short_term(self, key: str) -> bool:
        """将记忆从长期降级到短期
        
        Args:
            key: 记忆键
            
        Returns:
            降级是否成功
        """
        # 检查记忆是否存在
        value = self.long_term.retrieve(key)
        if value is None:
            return False
            
        # 从长期记忆中删除
        self.long_term.delete(key)
        
        # 存储到短期记忆
        return self.short_term.store(key, value, importance=1.0)
        
    def get_usage(self) -> Dict[str, Any]:
        """获取使用统计
        
        Returns:
            使用统计信息
        """
        short_term_usage = self.short_term.get_usage()
        long_term_usage = self.long_term.get_usage()
        
        return {
            "short_term": short_term_usage,
            "long_term": long_term_usage,
            "total_memories": short_term_usage.get("used", 0) + long_term_usage.get("total_memories", 0),
            "promotion_threshold": self.promotion_threshold,
        }