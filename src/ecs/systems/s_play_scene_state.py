import esper
from src.ecs.components.c_play_state import CPlayState, PlayState
from src.create.prefab_creator_game import create_enemies
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_play_state(world: esper.World, c_ps: CPlayState, level_cfg:dict, start_text_entity:dict, delta_time:float):
    if c_ps.state == PlayState.START:
        c_ps.time += delta_time
        if c_ps.time > 2.5:
            c_ps.time = 0
            world.delete_entity(start_text_entity)
            create_enemies(world, level_cfg)
            c_ps.state = PlayState.PLAYING
    elif c_ps.state == PlayState.PLAYING:
        if is_lvl_complete(world):
            c_ps.state = PlayState.WIN


def is_lvl_complete(world: esper.World):
    component_count = len(world.get_components(CTagEnemy))
    if component_count <= 0:
        return True
    return False