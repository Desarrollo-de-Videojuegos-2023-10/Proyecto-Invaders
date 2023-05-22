import pygame
import esper
from src.ecs.components.c_changing_text import CChangingText
from src.ecs.components.c_player_ability import CPlayerAbility, AbilityState
from src.engine.service_locator import ServiceLocator

def system_ability_state(world: esper.World, delta_time: float, max_bullets:dict):
    components = world.get_component(CPlayerAbility)
    for _, (c_pa) in components:
        if c_pa.state == AbilityState.READY:
            _do_ability_ready(c_pa)
        elif c_pa.state == AbilityState.CHARGING:
            _do_ability_charging(c_pa, delta_time)
        elif c_pa.state == AbilityState.SHOOTING:
            _do_ability_shooting(c_pa, delta_time, max_bullets)


def _do_ability_ready(c_pa: CPlayerAbility):
    pass

def _do_ability_charging(c_pa: CPlayerAbility, delta_time:float):
    c_pa.current_charge_time += delta_time
    if c_pa.current_charge_time > c_pa.cooldown_time:
        c_pa.state = AbilityState.READY
        c_pa.current_ability_time = 0

def _do_ability_shooting(c_pa: CPlayerAbility, delta_time:float, max_bullets:dict):
    c_pa.current_ability_time += delta_time
    if c_pa.current_ability_time > c_pa.ability_duration:
        level_cfg = ServiceLocator.config_service.get("assets/cfg/level_01.json")
        c_pa.state = AbilityState.CHARGING
        c_pa.current_charge_time = 0
        max_bullets["bullet_count"] = level_cfg["player_start"]["max_bullets"]