import pygame
import esper

from src.create.prefab_creator import create_sprite
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_enemy_state import CEnemyState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.tags.c_tag_temporary import CTagTemporary
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagplayer
from src.engine.service_locator import ServiceLocator
from src.create.prefab_creator import create_square


def create_player(world: esper.World):
    player_cfg = ServiceLocator.config_service.get("assets/cfg/player.json")

    surf = ServiceLocator.images_service.get(player_cfg["image"])
    pos = pygame.Vector2(player_cfg["spawn_point"]
                         ["x"], player_cfg["spawn_point"]["y"])
    vel = pygame.Vector2(0, 0)
    player_ent = create_sprite(world, pos, vel, surf)
    world.add_component(player_ent, CTagplayer(player_cfg["lives"]))
    return player_ent


def create_player_bullet(world: esper.World,
                         player_pos: pygame.Vector2,
                         player_size: pygame.Vector2):
    bullet_cfg = ServiceLocator.config_service.get(
        "assets/cfg/bullet.json")["player"]
    bullet_size = pygame.Vector2(
        bullet_cfg["size"]["x"], bullet_cfg["size"]["y"])
    color = pygame.Color(
        bullet_cfg["color"]["r"], bullet_cfg["color"]["g"], bullet_cfg["color"]["b"])
    pos = pygame.Vector2(player_pos.x + (player_size[0] / 2) - (bullet_size[0] / 2),
                         player_pos.y + (player_size[1] / 2) - (bullet_size[1] / 2))
    vel = pygame.Vector2(0, -bullet_cfg["speed"])

    bullet_entity = create_square(world, bullet_size, color, pos, vel)
    world.add_component(bullet_entity, CTagBullet())
    ServiceLocator.sounds_service.play(bullet_cfg["sound"])


def create_explosion(world: esper.World, pos: pygame.Vector2, explosion_info: dict):
    explosion_surface = ServiceLocator.images_service.get(
        explosion_info["image"])
    vel = pygame.Vector2(0, 0)

    explosion_entity = create_sprite(world, pos, vel, explosion_surface)
    world.add_component(explosion_entity, CTagTemporary())
    world.add_component(explosion_entity,
                        CAnimation(explosion_info["animations"]))
    ServiceLocator.sounds_service.play(explosion_info["sound"])
    return explosion_entity


def create_game_input(world: esper.World):
    quit_to_menu_action = world.create_entity()
    world.add_component(quit_to_menu_action,
                        CInputCommand("QUIT_TO_MENU",
                                      pygame.K_ESCAPE))
    left_action = world.create_entity()
    world.add_component(left_action,
                        CInputCommand("LEFT",
                                      pygame.K_LEFT))
    right_action = world.create_entity()
    world.add_component(right_action,
                        CInputCommand("RIGHT",
                                      pygame.K_RIGHT))

    pause_action = world.create_entity()
    world.add_component(pause_action,
                        CInputCommand("PAUSE",
                                      pygame.K_p))

    fire_action = world.create_entity()
    world.add_component(fire_action,
                        CInputCommand("PLAYER_FIRE", pygame.K_z))


def create_enemies(world: esper.World, level_cfg:dict):
    enemy_cfg = ServiceLocator.config_service.get("assets/cfg/enemy_data.json")

    for enemy_type_spawn in level_cfg["enemy_starting_points"]:
        pixel_offset_y = enemy_type_spawn["offset_y"]
        pixel_offset_x = enemy_type_spawn["offset_x"]
        enemy_type = enemy_type_spawn["type"]
        enemy_surf = ServiceLocator.images_service.get(enemy_cfg[enemy_type]["image"])
        for row in range(enemy_type_spawn["rows"]):
            for column in range(enemy_type_spawn["columns"]):
                enemy_pos = pygame.Vector2(enemy_type_spawn["pos"]["x"] + (column * pixel_offset_x),
                                           enemy_type_spawn["pos"]["y"] + (row * pixel_offset_y))
                enemy_vel = pygame.Vector2(0, 0)

                enemy_entity = create_sprite(world, enemy_pos, enemy_vel, enemy_surf)
                world.add_component(enemy_entity, CTagEnemy())
                world.add_component(enemy_entity, CEnemyState())
                world.add_component(enemy_entity, CAnimation(enemy_cfg[enemy_type]["animations"]))
