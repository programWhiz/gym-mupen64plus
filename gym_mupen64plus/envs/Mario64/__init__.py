# Discrete Action Space:
from gym.envs import register
from gym_mupen64plus.envs.Mario64.mario64_env import Mario64_Env

register(
    id='Mario-64-World-1-Star-1-v0',
    entry_point='gym_mupen64plus.envs.Mario64:Mario64_Env',
    kwargs={'save_state' : 'mario64-1-1.st3'},
    tags={ 'mupen': True },
    nondeterministic=True,
)
