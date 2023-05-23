from enum import Enum
import pygame
import esper
from src.create.prefab_creator import create_sprite
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_changing_text import CChangingText
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

def create_logo(world:esper.World):
    logo_cfg= ServiceLocator.config_service.get("assets/cfg/interface.json")["logo"]
    surface = ServiceLocator.images_service.get(logo_cfg["image"])
    pos = pygame.Vector2(logo_cfg["pos"]["x"]/2 , logo_cfg["pos"]["y"])
    vel = pygame.Vector2(0, 0)
    create_sprite(world, pos, vel, surface)
    

def create_menu(world:esper.World, score: int =0, level_no:int=1):
    interface_cfg = ServiceLocator.config_service.get("assets/cfg/interface.json")
    create_text(world, "1UP", interface_cfg["scene_texts"]["start"]["size"],
                pygame.Color(interface_cfg["title_color"]["r"], interface_cfg["title_color"]["g"], interface_cfg["title_color"]["b"]),
                pygame.Vector2(32, 18), TextAlignment.LEFT)
    create_text(world, "HI-SCORE", interface_cfg["scene_texts"]["start"]["size"],
                pygame.Color(interface_cfg["title_color"]["r"], interface_cfg["title_color"]["g"], interface_cfg["title_color"]["b"]),
                pygame.Vector2(90, 18), TextAlignment.LEFT)
    score_values = create_text(world, "00" if score == 0 else str(score), interface_cfg["scene_texts"]["start"]["size"],
                pygame.Color(interface_cfg["normal_color"]["r"], interface_cfg["normal_color"]["g"], interface_cfg["normal_color"]["b"]),
                pygame.Vector2(72, 28), TextAlignment.RIGHT)
    score_values = world.add_component(score_values, CScore(score=score))
    max_score_value = create_text(world, str(interface_cfg["high_score"]), interface_cfg["scene_texts"]["start"]["size"],
                pygame.Color(interface_cfg["high_score_color"]["r"], interface_cfg["high_score_color"]["g"], interface_cfg["high_score_color"]["b"]),
                pygame.Vector2(148, 28), TextAlignment.RIGHT)
    world.add_component(max_score_value, CScore(hiscore=True, score=score))    


def create_interface(world:esper.World, lives:int, score:int = 0, level_no:int = 1):
    interface_cfg = ServiceLocator.config_service.get("assets/cfg/interface.json")
    create_text(world, "1UP", interface_cfg["scene_texts"]["start"]["size"],
                pygame.Color(interface_cfg["title_color"]["r"], interface_cfg["title_color"]["g"], interface_cfg["title_color"]["b"]),
                pygame.Vector2(32, 18), TextAlignment.LEFT)
    create_text(world, "HI-SCORE", interface_cfg["scene_texts"]["start"]["size"],
                pygame.Color(interface_cfg["title_color"]["r"], interface_cfg["title_color"]["g"], interface_cfg["title_color"]["b"]),
                pygame.Vector2(90, 18), TextAlignment.LEFT)

    score_values = create_text(world, "00" if score == 0 else str(score), interface_cfg["scene_texts"]["start"]["size"],
                pygame.Color(interface_cfg["normal_color"]["r"], interface_cfg["normal_color"]["g"], interface_cfg["normal_color"]["b"]),
                pygame.Vector2(72, 28), TextAlignment.RIGHT)
    score_values = world.add_component(score_values, CScore(score=score))

    max_score_value = create_text(world, str(interface_cfg["high_score"]), interface_cfg["scene_texts"]["start"]["size"],
                pygame.Color(interface_cfg["high_score_color"]["r"], interface_cfg["high_score_color"]["g"], interface_cfg["high_score_color"]["b"]),
                pygame.Vector2(148, 28), TextAlignment.RIGHT)
    world.add_component(max_score_value, CScore(hiscore=True, score=score))
    create_lives_gui(world, lives)

    if level_no < 6:
        create_levels_gui(world, level_no, level_no)
    else:
        create_levels_gui(world, 1, level_no)
        create_text(world, "0"+ str(level_no) if level_no < 10 else str(level_no), 8, pygame.Color(255,255,255), pygame.Vector2(220,26),TextAlignment.CENTER)

    ability_text = create_text(world, "CHARGED", 8, pygame.Color(255,255,255), pygame.Vector2(13, 235), TextAlignment.LEFT)
    world.add_component(ability_text, CChangingText("CHARGED", ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 8), pygame.Color(255,255,255)))

def create_levels_gui(world:esper.World, flag_no:int, level_no:int) -> int:
    level_cfg = ServiceLocator.config_service.get("assets/cfg/interface.json")["scene_texts"]["levels"]
    level_gui_entity = world.create_entity()
    level_list = list()
    for i in range(flag_no):
        surface = ServiceLocator.images_service.get(level_cfg["image"])
        pos = pygame.Vector2(level_cfg["pos"]["x"] + i*surface.get_rect().width, level_cfg["pos"]["y"])
        vel = pygame.Vector2(0, 0)
        life_entity = create_sprite(world, pos, vel, surface)
        level_list.append(life_entity)
    world.add_component(level_gui_entity, CLevels(level_list, level_no))
    return level_gui_entity