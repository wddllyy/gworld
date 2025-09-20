from .base import GameObject

class Stone(GameObject):
    """石头类"""
    
    def __init__(self, x: int, y: int, obj_id: int = None):
        super().__init__(x, y, obj_id)
        self.emoji = "🪨"
        self.type = "stone"
    
    def get_emoji(self) -> str:
        return self.emoji
    
    def get_type(self) -> str:
        return self.type
