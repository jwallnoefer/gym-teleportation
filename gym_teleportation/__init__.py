from gym.envs.registration import register

register(
    id='teleportation-v0',
    entry_point="gym_teleportation.envs.teleportation:TeleportationEnv",
    nondeterministic=True
)
