import esper
from src.ecs.components.tags.c_tag_bullet import CTagBullet

def system_bullet_count(world: esper.World, runtime_bullets:dict):
    runtime_bullets["bullet_count"] = len(world.get_component(CTagBullet))