import esper
from src.create.prefab_creator_game import create_explosion
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.service_locator import ServiceLocator


def system_player_state(world: esper.World, delta_time: float):
    player_components = world.get_components(
        CSurface, CTransform, CPlayerState)

    c_s: CSurface
    c_t: CTransform
    c_pstate: CPlayerState
    for _, (c_s, c_t, c_pstate) in player_components:
        if c_pstate.state == PlayerState.DEAD:
            c_pstate.respawn_time += delta_time
            if c_pstate.respawn_time > 3 and c_pstate.lives > 0:
                player_cfg = ServiceLocator.config_service.get(
                    "assets/cfg/player.json")
                c_pstate.state = PlayerState.ALIVE
                c_pstate.respawn_time = 0
                c_t.pos.x = player_cfg["spawn_point"]["x"]
                c_s.visible = True


def kill_player(world: esper.World, c_t: CTransform, c_s: CSurface, c_pstate: CPlayerState):
    explosion_info = ServiceLocator.config_service.get(
        "assets/cfg/explosion.json")
    ServiceLocator.sounds_service.play(explosion_info["player"]["sound"])
    c_pstate.lives -= 1
    c_pstate.state = PlayerState.DEAD
    create_explosion(world, c_t.pos, explosion_info["player"])
    c_s.visible = False
