import pygame
from src.create.prefab_creator import create_starfield
from src.ecs.components.c_blink_item import CBlinkItem
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_blinking import system_blinking
from src.ecs.systems.s_bullet_count import system_bullet_count
from src.ecs.systems.s_enemy_movement import system_enemy_movement
from src.ecs.systems.s_enemy_spawn import system_enemy_spawn
from src.ecs.systems.s_starfield_movement import system_starfield_movement
from src.ecs.systems.s_temporary_remove import system_temporary_remove

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_game import create_enemies, create_player_bullet, create_game_input, create_player
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_screen_bullet import system_screen_bullet
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_collision_ball_block import system_collision_enemy_bullet
# from src.ecs.systems.s_collision_player_ball import system_collision_player_ball
from src.ecs.systems.s_block_count import system_block_count
import src.engine.game_engine
from src.engine.service_locator import ServiceLocator


class PlayScene(Scene):
    def __init__(self, level_path: str, engine: 'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        self.level_cfg = ServiceLocator.config_service.get(level_path)
        self.player_cfg = ServiceLocator.config_service.get("assets/cfg/player.json")
        self.enemies_cfg = ServiceLocator.config_service.get("assets/cfg/enemy_data.json")
        self.interface_cfg = ServiceLocator.config_service.get("assets/cfg/interface.json")["scene_texts"]
        self.max_bullets = self.level_cfg["player_start"]["max_bullets"]
        self.current_bullets = {
            "bullet_count": 0
        }
        self._player_ent = -1
        self._paused = False

    def do_create(self):
        self._start = create_text(self.ecs_world, self.interface_cfg["start"]["text"],
                                         self.interface_cfg["start"]["size"],
                                         pygame.Color(self.interface_cfg["start"]["color"]["r"],
                                                      self.interface_cfg["start"]["color"]["g"],
                                                      self.interface_cfg["start"]["color"]["b"]),
                                         pygame.Vector2(self.interface_cfg["start"]["pos"]["x"],
                                                        self.interface_cfg["start"]["pos"]["y"]),
                                         TextAlignment.CENTER)
        ServiceLocator.sounds_service.play(self.interface_cfg["start"]["sound"])
        self._time = pygame.time.get_ticks()/ 1000.0
        self._starting = False
        create_starfield(self.ecs_world)
        self._enemy = False

        player_ent = create_player(self.ecs_world)
        self._p_v = self.ecs_world.component_for_entity(player_ent, CVelocity)
        self._p_t = self.ecs_world.component_for_entity(player_ent, CTransform)
        self._p_s = self.ecs_world.component_for_entity(player_ent, CSurface)

        self._paused = False
        create_game_input(self.ecs_world)

    def do_update(self, delta_time: float):
        system_screen_player(self.ecs_world, self.screen_rect)
        system_screen_bullet(self.ecs_world, self.screen_rect)
        system_starfield_movement(self.ecs_world, delta_time)
        system_blinking(self.ecs_world, delta_time)
        self._tick = pygame.time.get_ticks()/ 1000.0
        if ( self._tick  - self._time) >= 2 and self._starting == False:
            self.ecs_world.delete_entity(self._start)
            self._starting = True
        if not self._paused and self._starting == True:
            if self._enemy == False:
                system_enemy_spawn(self.ecs_world, self.level_cfg)
                self._enemy = True
            system_movement(self.ecs_world, delta_time)
            system_enemy_movement(self.ecs_world, self.level_cfg, delta_time)
            system_bullet_count(self.ecs_world, self.current_bullets)
            system_collision_enemy_bullet(self.ecs_world)
            system_animation(self.ecs_world, delta_time)
            system_temporary_remove(self.ecs_world)
            system_block_count(self.ecs_world, self)

    def do_clean(self):
        self._paused = False

    def do_action(self, action: CInputCommand):
        if action.name == "LEFT":
            if action.phase == CommandPhase.START:
                self._p_v.vel.x -= self.player_cfg["input_speed"]
            elif action.phase == CommandPhase.END:
                self._p_v.vel.x += self.player_cfg["input_speed"]
        elif action.name == "RIGHT":
            if action.phase == CommandPhase.START:
                self._p_v.vel.x += self.player_cfg["input_speed"]
            elif action.phase == CommandPhase.END:
                self._p_v.vel.x -= self.player_cfg["input_speed"]

        if action.name == "PLAYER_FIRE" and not self._paused and self.current_bullets["bullet_count"] < self.max_bullets:
            if action.phase == CommandPhase.START:
                create_player_bullet(self.ecs_world,
                                     pygame.Vector2(
                                         self._p_t.pos.x, self._p_t.pos.y),
                                     pygame.Vector2(self._p_s.area.width,
                                                    self._p_s.area.height))

        if action.name == "QUIT_TO_MENU" and action.phase == CommandPhase.START:
            self.switch_scene("MENU_SCENE")

        if action.name == "PAUSE":
            if self._paused == False and action.phase == CommandPhase.START:
                self._paused = True
                self._text = create_text(self.ecs_world, self.interface_cfg["paused"]["text"],
                                         self.interface_cfg["paused"]["size"],
                                         pygame.Color(self.interface_cfg["paused"]["color"]["r"],
                                                      self.interface_cfg["paused"]["color"]["g"],
                                                      self.interface_cfg["paused"]["color"]["b"]),
                                         pygame.Vector2(self.interface_cfg["paused"]["pos"]["x"],
                                                        self.interface_cfg["paused"]["pos"]["y"]),
                                         TextAlignment.CENTER)
                ServiceLocator.sounds_service.play(
                    self.interface_cfg["paused"]["sound"])
                self.ecs_world.add_component(self._text, CBlinkItem(self.interface_cfg["paused"]["blink_rate"],
                                                                    self.interface_cfg["paused"]["blink_rate"]))
            elif self._paused == True and action.phase == CommandPhase.START:
                self._paused = False
                self.ecs_world.delete_entity(self._text)
