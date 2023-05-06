import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_temporary import CTagTemporary


def system_temporary_remove(world: esper.World):
    components = world.get_components(CAnimation, CTagTemporary)
    for temporary_entity,  (c_a, _) in components:
        if c_a.curr_frame == c_a.animations_list[c_a.curr_anim].end:
            world.delete_entity(temporary_entity)