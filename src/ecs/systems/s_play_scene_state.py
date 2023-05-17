import esper
import pygame
from src.create.prefab_creator_interface import TextAlignment, create_lives_gui, create_text
from src.ecs.components.c_play_state import CPlayState, PlayState
from src.create.prefab_creator_game import create_enemies
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator


def system_play_state(world: esper.World, c_ps: CPlayState, level_cfg: dict, start_text_entity: dict, interface_cfg: dict, player_cfg:dict, delta_time: float):
    player_state_components = world.get_component(CPlayerState)
    if c_ps.state == PlayState.START:
        c_ps.time += delta_time
        if c_ps.time > 2.5:
            c_ps.time = 0
            world.delete_entity(start_text_entity)
            create_lives_gui(world, player_cfg["lives"])
            create_enemies(world, level_cfg)
            c_ps.state = PlayState.PLAYING
    elif c_ps.state == PlayState.PLAYING:
        for player_entity, (c_pstate) in player_state_components:
            if c_pstate.lives < 0:
                c_ps.state = PlayState.GAME_OVER
                c_ps.time = 0
                world.delete_entity(player_entity)
        if is_lvl_complete(world):
            c_ps.state = PlayState.WIN
    elif c_ps.state == PlayState.GAME_OVER:
        c_ps.time += delta_time
        if c_ps.time > 4.5:
            c_ps.state = PlayState.END
            ServiceLocator.sounds_service.play(level_cfg["game_over_sfx"])
            create_text(world, interface_cfg["game_over"]["text"],
                        interface_cfg["game_over"]["size"],
                        pygame.Color(interface_cfg["game_over"]["color"]["r"],
                                    interface_cfg["game_over"]["color"]["g"],
                                    interface_cfg["game_over"]["color"]["b"]),
                        pygame.Vector2(interface_cfg["game_over"]["pos"]["x"],
                                    interface_cfg["game_over"]["pos"]["y"]),
                        TextAlignment.CENTER)


def is_lvl_complete(world: esper.World):
    component_count = len(world.get_components(CTagEnemy))
    if component_count <= 0:
        return True
    return False
