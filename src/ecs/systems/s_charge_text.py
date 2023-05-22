import esper
import pygame

from src.ecs.components.c_changing_text import CChangingText
from src.ecs.components.c_player_ability import AbilityState

def system_charging_text(world: esper.World, ability_state: int):
    components = world.get_component(CChangingText)
    for _, (c_ct) in components:
        if ability_state == AbilityState.READY:
            c_ct.text = "CHARGED"
            c_ct.color = pygame.Color(255, 255, 255)
        elif ability_state == AbilityState.CHARGING:
            c_ct.text = "CHARGING"
            c_ct.color = pygame.Color(255, 158, 57)
        elif ability_state == AbilityState.SHOOTING:
            c_ct.text = "ACTIVATED"
            c_ct.color = pygame.Color(0, 255, 0)