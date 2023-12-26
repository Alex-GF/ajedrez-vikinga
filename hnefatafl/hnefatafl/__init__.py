from gymnasium.envs.registration import register

register(
     id="hnefatafl/Hnefatafl-v0",
     entry_point="hnefatafl.envs:HnefataflEnv",
     max_episode_steps=300,
)