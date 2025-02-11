from stable_baselines3 import PPO
from rubiks_env import RubiksCubeEnv
import matplotlib.pyplot as plt
import matplotlib.patches as patches

env = RubiksCubeEnv()
model = PPO.load("rubiks solver PPO/rubiks_cube_solver.zip")

obs = env.reset()

for _ in range(1000):
    action, _ = model.predict(obs)
    obs, reward, done, _ = env.step(action)
    env.render()  # This will now update dynamically in one window

    if done:
        print("Cube Solved!")
        break

plt.ioff()   # Turn off interactive mode when done
plt.show()   # Keep the window open after solving
