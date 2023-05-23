import pygame
from src.create.prefab_creator import create_starfield
from src.create.prefab_creator_game import create_enemies
from src.ecs.components.c_blink_item import CBlinkItem
from src.ecs.systems.s_blinking import system_blinking
from src.ecs.systems.s_starfield_movement import system_starfield_movement

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_logo, create_menu, create_text
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.engine.service_locator import ServiceLocator

class MenuScene(Scene):

    def do_create(self,**kwargs):
        self._score = kwargs.get("score", 0)
        self._level_no = kwargs.get("level_no", 1)
        self.interface_cfg = ServiceLocator.config_service.get(
            "assets/cfg/interface.json")["scene_texts"]
        self._text = create_text(self.ecs_world, self.interface_cfg["press"]["text"],
                                         self.interface_cfg["press"]["size"],
                                         pygame.Color(self.interface_cfg["press"]["color"]["r"],
                                                      self.interface_cfg["press"]["color"]["g"],
                                                      self.interface_cfg["press"]["color"]["b"]),
                                         pygame.Vector2(self.interface_cfg["press"]["pos"]["x"],
                                                        self.interface_cfg["press"]["pos"]["y"]),
                                         TextAlignment.CENTER)
        self.ecs_world.add_component(self._text, CBlinkItem(self.interface_cfg["press"]["blink_rate"],
                                                                    self.interface_cfg["press"]["blink_rate"]))
        create_text(self.ecs_world, "Arrows to MOVE - P to PAUSE", 8,
                    pygame.Color(150, 150, 255), pygame.Vector2(130, 180), TextAlignment.CENTER)
        create_text(self.ecs_world, "F for special ability", 8,
                    pygame.Color(150, 150, 255), pygame.Vector2(130, 195), TextAlignment.CENTER)
        create_starfield(self.ecs_world)
        create_menu(self.ecs_world, score=self._score, level_no=self._level_no)
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))
        create_logo(self.ecs_world)
    

    def do_update(self, delta_time: float):
        system_starfield_movement(self.ecs_world, delta_time)
        system_blinking(self.ecs_world, delta_time)

    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME" and action.phase == CommandPhase.START:
            self.switch_scene("LEVEL_01")

