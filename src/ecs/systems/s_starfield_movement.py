import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_star import CTagStar
from src.engine.service_locator import ServiceLocator


def system_starfield_movement(world: esper.World, delta_time: float):
    components = world.get_components(CTransform, CVelocity, CTagStar)
    window_size = ServiceLocator.config_service.get("assets/cfg/window.json")["size"]
    for _, (c_t, c_v, _) in components:
        c_t.pos += c_v.vel * delta_time
        if (c_t.pos.y > window_size["h"]):
            c_t.pos.y = 0