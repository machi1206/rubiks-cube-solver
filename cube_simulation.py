import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Define cube colors
color_map = {'W': 'white', 'Y': 'yellow', 'R': 'red', 'O': 'orange', 'G': 'green', 'B': 'blue'}

# Create initial cube
def create_cube():
    colors = ['W', 'R', 'Y', 'O', 'G', 'B']
    faces = ['F', 'D', 'B', 'U', 'L', 'R']
    return {face: np.full((3, 3), color) for face, color in zip(faces, colors)}

# Rotate a face
def rotate_face(face, clockwise=True):
    return np.rot90(face, -1 if clockwise else 1)

# Move function
def move(cube, operation):
    face = operation[0]
    clockwise = not (len(operation) == 2 and operation[1] == "'")
    cube[face] = rotate_face(cube[face], clockwise)

    adjacent_faces = {
        'U': [('B', 0, 'row'), ('R', 0, 'row'), ('F', 0, 'row'), ('L', 0, 'row')],
        'D': [('F', 2, 'row'), ('R', 2, 'row'), ('B', 2, 'row'), ('L', 2, 'row')],
        'F': [('U', 2, 'row'), ('R', 0, 'col'), ('D', 0, 'row'), ('L', 2, 'col')],
        'B': [('U', 0, 'row'), ('L', 0, 'col'), ('D', 2, 'row'), ('R', 2, 'col')],
        'L': [('U', 0, 'col'), ('F', 0, 'col'), ('D', 0, 'col'), ('B', 2, 'col')],
        'R': [('U', 2, 'col'), ('B', 0, 'col'), ('D', 2, 'col'), ('F', 2, 'col')]
    }

    if face in adjacent_faces:
        edges = []
        for f, idx, typ in adjacent_faces[face]:
            edges.append(np.copy(cube[f][idx] if typ == 'row' else cube[f][:, idx]))

        if clockwise:
            edges = [edges[-1]] + edges[:-1]
        else:
            edges = edges[1:] + [edges[0]]

        for (f, idx, typ), new_edge in zip(adjacent_faces[face], edges):
            if typ == 'row':
                cube[f][idx] = new_edge
            else:
                cube[f][:, idx] = new_edge

# Draw cube
def draw_cube(cube, ax):
    ax.clear()
    ax.set_aspect('equal')
    ax.axis('off')

    positions = {
        'U': (3, 6), 'L': (0, 3), 'F': (3, 3), 'R': (6, 3), 'B': (9, 3), 'D': (3, 0)
    }

    for face, (x_offset, y_offset) in positions.items():
        for i in range(3):
            for j in range(3):
                color = color_map[cube[face][i, j]]
                rect = patches.Rectangle((x_offset + j, y_offset - i), 1, 1, facecolor=color, edgecolor='black')
                ax.add_patch(rect)

    ax.set_xlim(-1, 13)
    ax.set_ylim(-3, 10)
    plt.draw()

# Convert cube state to a numeric format
def get_cube_state(cube):
    color_to_num = {'W': 0, 'Y': 1, 'R': 2, 'O': 3, 'G': 4, 'B': 5}
    return np.array([color_to_num[cube[face][i, j]] for face in cube for i in range(3) for j in range(3)])
