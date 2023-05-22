import esper
from src.ecs.components.c_score import CScore
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_bullet import BulletType, CTagBullet
from src.create.prefab_creator_game import create_explosion
from src.engine.service_locator import ServiceLocator


def system_collision_enemy_bullet(world: esper.World):
    explosion_info = ServiceLocator.config_service.get("assets/cfg/explosion.json")
    components_enemy = world.get_components(CSurface, CTransform, CTagEnemy)
    components_bullet = world.get_components(CSurface, CTransform, CTagBullet)
    components_score = world.get_component(CScore)

    for enemy_entity, (c_s, c_t, c_tag_enemy) in components_enemy:
        ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        for bullet_entity, (c_b_s, c_b_t, c_tag_bullet) in components_bullet:
            bull_rect = CSurface.get_area_relative(c_b_s.area, c_b_t.pos)
            if ene_rect.colliderect(bull_rect) and c_tag_bullet.type == BulletType.PLAYER:
                world.delete_entity(enemy_entity)
                world.delete_entity(bullet_entity)
                create_explosion(world, c_t.pos, explosion_info["enemy"])
                for _, (c_score) in components_score:
                    c_score.score += c_tag_enemy.score_value