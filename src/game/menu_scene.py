import pygame
from src.create.prefab_creator import create_starfield
from src.create.prefab_creator_game import create_enemies
from src.ecs.components.c_blink_item import CBlinkItem
from src.ecs.systems.s_blinking import system_blinking
from src.ecs.systems.s_starfield_movement import system_starfield_movement

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import create_menu
from src.ecs.components.c_input_command import CInputCommand, CommandPhase

class MenuScene(Scene):

    def do_create(self,**kwargs):
        create_starfield(self.ecs_world)
        create_menu(self.ecs_world)
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))


    def do_update(self, delta_time: float):
        system_starfield_movement(self.ecs_world, delta_time)
        system_blinking(self.ecs_world, delta_time)

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME" and action.phase == CommandPhase.START:
            self.switch_scene("LEVEL_01")

