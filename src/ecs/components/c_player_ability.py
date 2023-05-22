from enum import Enum

class AbilityState(Enum):
    READY = 0
    CHARGING = 1
    SHOOTING = 2

class CPlayerAbility:
    def __init__(self, cooldown_time:int, ability_duration:int) -> None:
        self.cooldown_time = cooldown_time
        self.current_charge_time = cooldown_time
        self.ability_duration = ability_duration
        self.current_ability_time = 0
        self.state = AbilityState.READY