import json
import esper
from src.create.prefab_creator_game import create_explosion
from src.ecs.components.c_lives import CLives
from src.ecs.components.c_levels import CLevels
from src.ecs.components.c_play_state import CPlayState
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.service_locator import ServiceLocator


def system_player_state(world: esper.World, delta_time: float, player: dict):
    player_components = world.get_components(
        CSurface, CTransform, CPlayerState)
    play_state_components = world.get_component(CPlayState)
    lives_gui_components = world.get_component(CLives)
    level_gui_components = world.get_component(CLevels)

    c_s: CSurface
    c_t: CTransform
    c_pstate: CPlayerState
    for _, (c_s, c_t, c_pstate) in player_components:
        if c_pstate.state == PlayerState.DEAD:
            config = ServiceLocator.config_service.get("assets/cfg/interface.json")
            config["scene_texts"]["level"] = 1
            ServiceLocator.config_service.save("assets/cfg/interface.json", config)
            c_pstate.respawn_time += delta_time
            if c_pstate.respawn_time > 3 and c_pstate.lives > -1:
                player_cfg = ServiceLocator.config_service.get(
                    "assets/cfg/player.json")
                c_pstate.state = PlayerState.ALIVE
                c_pstate.respawn_time = 0
                c_t.pos.x = player_cfg["spawn_point"]["x"]
                c_s.visible = True
                for _, c_lives in lives_gui_components:
                    entity_to_remove = c_lives.live_entities.pop()
                    world.delete_entity(entity_to_remove)


def kill_player(world: esper.World, c_t: CTransform, c_s: CSurface, c_pstate: CPlayerState):
    explosion_info = ServiceLocator.config_service.get(
        "assets/cfg/explosion.json")
    ServiceLocator.sounds_service.play(explosion_info["player"]["sound"])
    c_pstate.lives -= 1
    c_pstate.state = PlayerState.DEAD
    create_explosion(world, c_t.pos, explosion_info["player"])
    c_s.visible = False
