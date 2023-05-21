import esper
import pygame
from src.ecs.components.c_score import CScore
from src.ecs.components.c_surface import CSurface
from src.engine.service_locator import ServiceLocator

def system_score_rendering(world: esper.World):
    interface_cfg = ServiceLocator.config_service.get("assets/cfg/interface.json")
    components = world.get_components(CScore, CSurface)

    for _, (c_score, c_s) in components:
        font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 8)
        hiscore = interface_cfg["high_score"]
        if not c_score.hiscore:
            c_s.surf = font.render(str(c_score.score), True, pygame.Color(interface_cfg["normal_color"]["r"], interface_cfg["normal_color"]["g"], interface_cfg["normal_color"]["b"]))
            c_s.area = c_s.surf.get_rect()
        elif c_score.score > hiscore and c_score.hiscore:
            c_s.surf = font.render(str(c_score.score), True, pygame.Color(interface_cfg["high_score_color"]["r"], interface_cfg["high_score_color"]["g"], interface_cfg["high_score_color"]["b"]))
            c_s.area = c_s.surf.get_rect()
