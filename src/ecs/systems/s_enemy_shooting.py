import esper
import random
from src.create.prefab_creator_game import create_enemy_bullet
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy

def system_enemy_shooting(world: esper.World):
    player_components = world.get_component(CPlayerState)
    enemy_components = world.get_components(CTagEnemy, CTransform, CSurface)

    c_pstate: CPlayerState
    for _, (c_pstate) in player_components:
        if c_pstate.state == PlayerState.IDLE:
            for _, (_, c_t, c_s) in enemy_components:
                chance = random.randint(0, 2000)
                if chance <= 1:
                    create_enemy_bullet(world, c_t.pos, c_s.area)