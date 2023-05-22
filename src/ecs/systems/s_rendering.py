import esper
import pygame

from src.ecs.components.c_changing_text import CChangingText
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface

def system_rendering(world:esper.World, screen:pygame.Surface):
    components = world.get_components(CTransform, CSurface)
    for ent, (c_t, c_s) in components:
        if not c_s.visible:
            continue

        # CASO ESPECIAL CUANDO EL TEXTO CAMBIA
        # SE DEBE VOLVER A CREAR LA SUPERFICIE
        if world.has_component(ent, CChangingText):
            c_txt = world.component_for_entity(ent, CChangingText)
            c_s.surf = c_txt.font.render(c_txt.text, True, c_txt.color)
            c_s.area = c_s.surf.get_rect()
        screen.blit(c_s.surf, c_t.pos, area=c_s.area)