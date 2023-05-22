import esper
from src.ecs.components.c_enemy_state import CEnemyState, MovementDirection
from src.ecs.components.c_transform import CTransform
from src.engine.service_locator import ServiceLocator

def system_enemy_movement(world: esper.World, lvl_cfg:dict, delta_time: float):
    components = world.get_components(CEnemyState, CTransform)
    enemy_limits = ServiceLocator.config_service.get("assets/cfg/enemy_data.json")
    max_pos_left = None
    max_pos_right = None

    for _, (c_es, c_t) in components:
        if  max_pos_left is None or c_t.pos.x < max_pos_left:
            max_pos_left = c_t.pos.x
        elif max_pos_right is None or c_t.pos.x > max_pos_right:
            max_pos_right = c_t.pos.x
        if c_es.movement_direction == MovementDirection.LEFT:
            c_t.pos.x -= lvl_cfg["enemy_speed"] * delta_time
        elif c_es.movement_direction == MovementDirection.RIGHT:
            c_t.pos.x += lvl_cfg["enemy_speed"] * delta_time


    if max_pos_left and max_pos_left < enemy_limits["movement_limit_left"]:
        for _, (c_es, _) in components:
            c_es.movement_direction = MovementDirection.RIGHT
    elif max_pos_right and max_pos_right > enemy_limits["movement_limit_right"]:
        for _, (c_es, _) in components:
            c_es.movement_direction = MovementDirection.LEFT