from enum import Enum

class BulletType(Enum):
    PLAYER = 1
    ENEMY = 2

class CTagBullet:
    def __init__(self, bullet_type: BulletType):
        self.type = bullet_type
