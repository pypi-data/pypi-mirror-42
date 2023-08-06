
from gym.envs.registration import register

register(
    id='custom-env-v0',
    entry_point='custom_gym_envs.envs:CustomEnv',
)
