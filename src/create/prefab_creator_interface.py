from enum import Enum
import pygame
import esper
from src.create.prefab_creator import create_sprite
from src.ecs.components.c_lives import CLives

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