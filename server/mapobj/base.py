from abc import ABC, abstractmethod
from typing import List, Tuple
import uuid

class GameObject(ABC):
    """游戏对象基类"""
    
    def __init__(self, x: int, y: int, obj_id: int = None):
        self.x = x
        self.y = y
        self.emoji = ""
        self.type = ""
        self.id = obj_id if obj_id is not None else -1
    
    @abstractmethod
    def get_emoji(self) -> str:
        """获取对象的emoji表示"""
        pass
    
    @abstractmethod
    def get_type(self) -> str:
        """获取对象类型"""
        pass
    
    def get_position(self) -> Tuple[int, int]:
        """获取对象位置"""
        return (self.x, self.y)
    
    def set_position(self, x: int, y: int):
        """设置对象位置"""
        self.x = x
        self.y = y
    
    def to_dict(self) -> dict:
        """转换为字典格式，用于发送给客户端"""
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'emoji': self.get_emoji(),
            'type': self.get_type()
        }
