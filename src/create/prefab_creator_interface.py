from enum import Enum
import pygame
import esper
from src.create.prefab_creator import create_sprite
from src.ecs.components.c_levels import CLevels
from src.ecs.components.c_lives import CLives
from src.ecs.components.c_score import CScore

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.engine.service_locator import ServiceLocator

class TextAlignment(Enum):
    LEFT = 0,
    RIGHT = 1
    CENTER = 2

def create_text(world:esper.World, txt:str, size:int,
                color:pygame.Color, pos:pygame.Vector2, alignment:TextAlignment) -> int:
    font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", size)
    text_entity = world.create_entity()

    world.add_component(text_entity, CSurface.from_text(txt, font, color))
    txt_s = world.component_for_entity(text_entity, CSurface)

    # De acuerdo al alineamiento, determia el origine de la superficie
    origin = pygame.Vector2(0, 0)
    if alignment is TextAlignment.RIGHT:
        origin.x -= txt_s.area.right
    elif alignment is TextAlignment.CENTER:
        origin.x -= txt_s.area.centerx

    world.add_component(text_entity,
                        CTransform(pos + origin))
    return text_entity

def create_lives_gui(world:esper.World, lives:int) -> int:
    lives_cfg = ServiceLocator.config_service.get("assets/cfg/interface.json")["scene_texts"]["lives"]
    lives_gui_entity = world.create_entity()
    lives_list = list()
    for i in range(lives):
        surface = ServiceLocator.images_service.get(lives_cfg["image"])
        pos = pygame.Vector2(lives_cfg["pos"]["x"] + i*surface.get_rect().width, lives_cfg["pos"]["y"])
        vel = pygame.Vector2(0, 0)
        life_entity = create_sprite(world, pos, vel, surface)
        lives_list.append(life_entity)
    world.add_component(lives_gui_entity, CLives(lives_list))

    return lives_gui_entity

def create_interface(world:esper.World, lives:int):
    interface_cfg = ServiceLocator.config_service.get("assets/cfg/interface.json")
    create_text(world, "1UP", interface_cfg["scene_texts"]["start"]["size"],
                pygame.Color(interface_cfg["title_color"]["r"], interface_cfg["title_color"]["g"], interface_cfg["title_color"]["b"]),
                pygame.Vector2(32, 18), TextAlignment.LEFT)
    create_text(world, "HI-SCORE", interface_cfg["scene_texts"]["start"]["size"],
                pygame.Color(interface_cfg["title_color"]["r"], interface_cfg["title_color"]["g"], interface_cfg["title_color"]["b"]),
                pygame.Vector2(90, 18), TextAlignment.LEFT)

    score_values = create_text(world, "0", interface_cfg["scene_texts"]["start"]["size"],
                pygame.Color(interface_cfg["normal_color"]["r"], interface_cfg["normal_color"]["g"], interface_cfg["normal_color"]["b"]),
                pygame.Vector2(72, 28), TextAlignment.RIGHT)
    score_values = world.add_component(score_values, CScore())

    max_score_value = create_text(world, str(interface_cfg["high_score"]), interface_cfg["scene_texts"]["start"]["size"],
                pygame.Color(interface_cfg["high_score_color"]["r"], interface_cfg["high_score_color"]["g"], interface_cfg["high_score_color"]["b"]),
                pygame.Vector2(148, 28), TextAlignment.RIGHT)
    max_score_value = world.add_component(max_score_value, CScore(hiscore=True))
    create_lives_gui(world, lives)

def create_levels_gui(world:esper.World, levels:int) -> int:
    level_cfg = ServiceLocator.config_service.get("assets/cfg/interface.json")["scene_texts"]["levels"]
    level_gui_entity = world.create_entity()
    level_list = list()
    for i in range(levels):
        surface = ServiceLocator.images_service.get(level_cfg["image"])
        pos = pygame.Vector2(level_cfg["pos"]["x"] + i*surface.get_rect().width, level_cfg["pos"]["y"])
        vel = pygame.Vector2(0, 0)
        life_entity = create_sprite(world, pos, vel, surface)
        level_list.append(life_entity)
    world.add_component(level_gui_entity, CLevels(level_list,levels))
    print(levels)
    return level_gui_entity