from .base import GameObject

class Stone(GameObject):
    """石头类"""
    
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.emoji = "🪨"
        self.type = "stone"
    
    def get_emoji(self) -> str:
        return self.emoji
    
    def get_type(self) -> str:
        return self.type
