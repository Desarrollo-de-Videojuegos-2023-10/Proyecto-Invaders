import esper
from src.create.prefab_creator_game import create_enemies


def system_enemy_spawn(world: esper.World, enemy: dict):
    create_enemies(world, enemy)