import json
import esper
from src.create.prefab_creator_interface import create_levels_gui
from src.ecs.components.c_player_state import CPlayerState

from src.ecs.components.tags.c_tag_enemy import CTagEnemy

from src.engine.scenes.scene import Scene

def system_enemies_count(world: esper.World, scene:Scene, c_pstate: CPlayerState, levels: dict):
    print(len(world.get_components(CTagEnemy)))
    component_count = len(world.get_components(CTagEnemy))
    if component_count <= 0:
        c_pstate.levels += 1
        levels["level"] =  c_pstate.levels
        with open("assets/cfg/player.json", 'w') as archivo_nuevo:
            json.dump(levels, archivo_nuevo, indent=4)
        scene.switch_scene("LEVEL_01")