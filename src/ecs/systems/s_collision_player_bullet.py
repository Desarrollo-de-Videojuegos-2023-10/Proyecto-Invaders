import esper
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import BulletType, CTagBullet
from src.ecs.systems.s_player_state import kill_player


def system_collision_player_bullet(world: esper.World):
    player_components = world.get_components(CSurface, CTransform, CPlayerState)
    components_bullet = world.get_components(CSurface, CTransform, CTagBullet)

    for _, (c_s, c_t, c_pstate) in player_components:
        player_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        for bullet_entity, (c_b_s, c_b_t, c_tag_bullet) in components_bullet:
            bull_rect = CSurface.get_area_relative(c_b_s.area, c_b_t.pos)
            if player_rect.colliderect(bull_rect) and c_tag_bullet.type == BulletType.ENEMY and c_pstate.state == PlayerState.IDLE:
                world.delete_entity(bullet_entity)
                kill_player(world, c_t, c_s, c_pstate)
