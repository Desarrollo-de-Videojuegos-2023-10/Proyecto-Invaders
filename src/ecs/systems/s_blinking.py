import esper
from src.ecs.components.c_blink_item import CBlinkItem
from src.ecs.components.c_surface import CSurface


def system_blinking(world: esper.World, delta_time: float):
    components = world.get_components(CSurface, CBlinkItem)
    for _, (c_s, c_b) in components:

        c_b.current_time += delta_time
        if c_b.current_time >= c_b.blink_rate:
            c_b.current_time = 0
            c_s.visible = not c_s.visible