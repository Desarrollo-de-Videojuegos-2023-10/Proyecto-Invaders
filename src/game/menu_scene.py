import pygame
from src.create.prefab_creator import create_starfield
from src.ecs.systems.s_blinking import system_blinking
from src.ecs.systems.s_starfield_movement import system_starfield_movement

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_text
from src.ecs.components.c_input_command import CInputCommand

class MenuScene(Scene):

    def do_create(self):
        create_text(self.ecs_world, "MAIN MENU", 16,
                    pygame.Color(50, 255, 50), pygame.Vector2(128, 130), TextAlignment.CENTER)
        create_text(self.ecs_world, "PRESS Z TO START GAME", 11,
                    pygame.Color(255, 255, 0), pygame.Vector2(128, 160), TextAlignment.CENTER)
        create_text(self.ecs_world, "Arrows to MOVE - P to PAUSE", 8,
                    pygame.Color(150, 150, 255), pygame.Vector2(320, 250), TextAlignment.CENTER)
        create_starfield(self.ecs_world)

        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))

    def do_update(self, delta_time: float):
        system_starfield_movement(self.ecs_world, delta_time)
        system_blinking(self.ecs_world, delta_time)

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            self.switch_scene("LEVEL_01")

