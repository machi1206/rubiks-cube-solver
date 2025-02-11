import gym
from gym import spaces
import random
import numpy as np
from cube_simulation import create_cube, move, get_cube_state, draw_cube
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class RubiksCubeEnv(gym.Env):
    def __init__(self):
        super(RubiksCubeEnv, self).__init__()
        self.cube = create_cube()
        self.action_space = spaces.Discrete(12)  # 12 moves
        self.moves = ['U', "U'", 'D', "D'", 'F', "F'", 'B', "B'", 'L', "L'", 'R', "R'"]
        self.observation_space = spaces.Box(low=0, high=5, shape=(54,), dtype=np.int32)
        self.fig, self.ax = plt.subplots()  
        plt.ion()  
        self.fig.show()  
        self.fig.canvas.draw()  

    def _get_observation(self):
        # Map colors to integers
        color_to_int = {'W': 0, 'Y': 1, 'R': 2, 'O': 3, 'G': 4, 'B': 5}
        
        # Flatten the cube state into a 1D array of integers
        observation = []
        for face in ['U', 'D', 'F', 'B', 'L', 'R']:
            observation.extend([color_to_int[color] for color in self.cube[face].flatten()])
        
        return np.array(observation, dtype=np.int32)


    def reset(self):
        self.cube = create_cube()
        num_scrambles = np.random.randint(2, 5)  # Start with fewer moves
        for _ in range(num_scrambles):
            random_move = random.choice(self.moves)
            move(self.cube, random_move)  # Directly use the move function
        return self._get_observation()

    def step(self, action):
        move(self.cube, self.moves[action])
        reward = self.calculate_reward()
        done = self.is_solved()
        return self._get_observation(), reward, done, {}


    def is_solved(self):
        return all(np.all(face == face[0, 0]) for face in self.cube.values())

    def render(self):
        self.ax.clear()  # Clear previous cube state
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        # Draw cube faces
        positions = {'U': (3, 6), 'L': (0, 3), 'F': (3, 3), 'R': (6, 3), 'B': (9, 3), 'D': (3, 0)}
        color_map = {'W': 'white', 'Y': 'yellow', 'R': 'red', 'O': 'orange', 'G': 'green', 'B': 'blue'}

        for face, (x_offset, y_offset) in positions.items():
            for i in range(3):
                for j in range(3):
                    color = color_map[self.cube[face][i, j]]
                    rect = patches.Rectangle((x_offset + j, y_offset - i), 1, 1, facecolor=color, edgecolor='black')
                    self.ax.add_patch(rect)

        self.ax.set_xlim(-1, 13)
        self.ax.set_ylim(-3, 10)

        self.fig.canvas.draw()  # Draw updates on the same window
        plt.pause(0.2)          # Add delay to visualize each move

    def calculate_reward(self):
        solved_faces = sum(np.all(self.cube[face] == self.cube[face][1, 1]) for face in self.cube)
        reward = -0.25  # Penalty for each move
        reward += 10 * solved_faces  # Bonus for each solved face

        if self.is_solved():
            reward += 100  # Big reward for solving the cube
        return reward
