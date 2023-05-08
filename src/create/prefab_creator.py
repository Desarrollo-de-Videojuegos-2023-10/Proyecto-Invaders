import pygame
import esper
import random
from src.ecs.components.c_blink_item import CBlinkItem

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_star import CTagStar
from src.engine.service_locator import ServiceLocator


def create_square(world: esper.World, size: pygame.Vector2, color: pygame.Color,
                  pos: pygame.Vector2, vel: pygame.Vector2) -> int:
    square_entity = world.create_entity()
    world.add_component(square_entity, CSurface(size, color))
    world.add_component(square_entity, CTransform(pos))
    if vel is not None:
        world.add_component(square_entity, CVelocity(vel))
    return square_entity


def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2,
                  surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CSurface.from_surface(surface))
    world.add_component(sprite_entity, CTransform(pos))
    if vel is not None:
        world.add_component(sprite_entity, CVelocity(vel))
    return sprite_entity


def create_starfield(world: esper.World):
    starfield_cfg = ServiceLocator.config_service.get(
        "assets/cfg/starfield.json")
    window_size = ServiceLocator.config_service.get(
        "assets/cfg/window.json")["size"]
    star_amount = starfield_cfg["number_of_stars"]
    star_colors = starfield_cfg["star_colors"]
    speed_cfg = starfield_cfg["vertical_speed"]
    blink_rate = starfield_cfg["blink_rate"]

    for _ in range(star_amount):
        entity = world.create_entity()
        size = pygame.Vector2(1, 1)
        selected_color = random.choice(star_colors)
        speed = random.randint(speed_cfg["min"], speed_cfg["max"])

        color = pygame.Color(
            selected_color["r"], selected_color["g"], selected_color["b"])
        pos = pygame.Vector2(random.randint(
            5, window_size["w"]), random.randint(5, window_size["h"]))
        vel = pygame.Vector2(0, speed)

        world.add_component(entity, CTagStar())
        world.add_component(entity, CSurface(size, color))
        world.add_component(entity, CTransform(pos))
        world.add_component(entity, CVelocity(vel))
        world.add_component(entity, CBlinkItem(
            random.uniform(blink_rate["min"], blink_rate["max"]),
            random.uniform(blink_rate["min"], blink_rate["max"]))
        )