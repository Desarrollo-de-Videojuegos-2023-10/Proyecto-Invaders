import esper
from src.ecs.components.tags.c_tag_bullet import BulletType, CTagBullet

def system_bullet_count(world: esper.World, runtime_bullets:dict):

    runtime_bullets["bullet_count"] = len([bullet for _, bullet in world.get_component(CTagBullet) if bullet.type == BulletType.PLAYER])