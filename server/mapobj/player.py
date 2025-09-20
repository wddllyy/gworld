from .base import GameObject

class Player(GameObject):
    """玩家类"""
    
    def __init__(self, x: int, y: int, obj_id: int = None):
        super().__init__(x, y, obj_id)
        self.emoji = "🧍🏻‍♂️"
        self.type = "player"
    
    def get_emoji(self) -> str:
        return self.emoji
    
    def get_type(self) -> str:
        return self.type
