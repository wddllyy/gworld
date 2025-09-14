from .base import GameObject

class Tree(GameObject):
    """树类"""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.emoji = "🌳"
        self.type = "tree"
    
    def get_emoji(self) -> str:
        return self.emoji
    
    def get_type(self) -> str:
        return self.type
