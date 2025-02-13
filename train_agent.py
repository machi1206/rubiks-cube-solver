from stable_baselines3 import PPO
from rubiks_env import RubiksCubeEnv

env = RubiksCubeEnv()
model = PPO('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=10000)

# Save the trained model
model.save("rubiks_cube_solver")
