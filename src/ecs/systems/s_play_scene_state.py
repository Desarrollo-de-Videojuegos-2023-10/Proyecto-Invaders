import esper
import pygame
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_levels import CLevels
from src.ecs.components.c_play_state import CPlayState, PlayState
from src.create.prefab_creator_game import create_enemies, create_game_over_input
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_score import CScore
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator


def system_play_state(world: esper.World, c_ps: CPlayState, level_cfg: dict, start_text_entity: dict, interface_cfg: dict, delta_time: float, scene):
    player_state_components = world.get_component(CPlayerState)
    if c_ps.state == PlayState.START:
        c_ps.time += delta_time
        if c_ps.time > 2.5:
            c_ps.time = 0
            world.delete_entity(start_text_entity)
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

    elif c_ps.state == PlayState.END:
        if not c_ps.already_saved:
            create_game_over_input(world)
            save_scores(world, c_ps)
    elif c_ps.state == PlayState.WIN:
        if not c_ps.already_saved:
            switch_level(world, c_ps, scene, player_state_components)

def is_lvl_complete(world: esper.World):
    component_count = len(world.get_components(CTagEnemy))
    if component_count <= 0:
        return True
    return False

def switch_level(world: esper.World, c_ps: CPlayState, scene, player_state_components:list):
    current_score = save_scores(world, c_ps)
    components = world.get_component(CLevels)
    level = 1
    for _, (c_level) in components:
        c_level.level +=1
        level = c_level.level

    lives = 3
    for _, (c_pstate) in player_state_components:
        lives = c_pstate.lives
    scene.switch_scene("LEVEL_01", score=current_score, level_no=level, player_lives=lives)

def save_scores(world, c_ps: CPlayState):
    config = ServiceLocator.config_service.get("assets/cfg/interface.json")
    components = world.get_component(CScore)
    current_score = 0
    for _, (c_score) in components:
        if c_score.hiscore and c_score.score > config["high_score"]:
            config["high_score"] = c_score.score
            ServiceLocator.config_service.save("assets/cfg/interface.json", config)
        elif not c_score.hiscore:
            current_score = c_score.score
    c_ps.already_saved = True
    return current_score