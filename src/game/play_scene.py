import json
import pygame
from src.create.prefab_creator import create_starfield
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_blinking import system_blinking
from src.ecs.systems.s_starfield_movement import system_starfield_movement
from src.ecs.systems.s_temporary_remove import system_temporary_remove

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_game import create_player_bullet, create_game_input, create_player, create_play_field
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_screen_bullet import system_screen_bullet
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_collision_ball_block import system_collision_enemy_bullet
#from src.ecs.systems.s_collision_player_ball import system_collision_player_ball
from src.ecs.systems.s_block_count import system_block_count
import src.engine.game_engine


class PlayScene(Scene):
    def __init__(self, level_path: str, engine: 'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        with open(level_path) as level_file:
            self.level_cfg = json.load(level_file)
        with open("assets/cfg/player.json") as player_file:
            self.player_cfg = json.load(player_file)
        with open("assets/cfg/blocks.json") as blocks_file:
            self.blocks_cfg = json.load(blocks_file)

        self._player_ent = -1
        self._paused = False

    def do_create(self):
        create_starfield(self.ecs_world)
        create_play_field(self.ecs_world,
                          self.level_cfg["blocks_field"],
                          self.blocks_cfg)

        player_ent = create_player(self.ecs_world)
        self._p_v = self.ecs_world.component_for_entity(player_ent, CVelocity)
        self._p_t = self.ecs_world.component_for_entity(player_ent, CTransform)
        self._p_s = self.ecs_world.component_for_entity(player_ent, CSurface)

        paused_text_ent = create_text(self.ecs_world, "PAUSED", 16,
                                      pygame.Color(255, 50, 50), pygame.Vector2(
                                          320, 180),
                                      TextAlignment.CENTER)
        self.p_txt_s = self.ecs_world.component_for_entity(
            paused_text_ent, CSurface)
        self.p_txt_s.visible = self._paused

        self._paused = False
        create_game_input(self.ecs_world)

    def do_update(self, delta_time: float):
        system_screen_player(self.ecs_world, self.screen_rect)
        system_screen_bullet(self.ecs_world, self.screen_rect)
        system_block_count(self.ecs_world, self)
        system_starfield_movement(self.ecs_world, delta_time)
        system_blinking(self.ecs_world, delta_time)

        if not self._paused:
            system_movement(self.ecs_world, delta_time)
            system_collision_enemy_bullet(self.ecs_world)
            system_animation(self.ecs_world, delta_time)
            system_temporary_remove(self.ecs_world)

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

        if action.name == "PLAYER_FIRE":
            if action.phase == CommandPhase.START:
                create_player_bullet(self.ecs_world,
                    pygame.Vector2(self._p_t.pos.x, self._p_t.pos.y),
                    pygame.Vector2(self._p_s.area.width,
                                   self._p_s.area.height))

        if action.name == "QUIT_TO_MENU" and action.phase == CommandPhase.START:
            self.switch_scene("MENU_SCENE")

        if action.name == "PAUSE" and action.phase == CommandPhase.START:
            self._paused = not self._paused
            self.p_txt_s.visible = self._paused

