import matplotlib.pyplot as plt


def print_cube_list(cube_list):
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(projection='3d')

    sequence_of_x_vals = []
    sequence_of_y_vals = []
    sequence_of_z_vals = []

    for cube in cube_list:
        sequence_of_x_vals.append(cube.x)
        sequence_of_y_vals.append(cube.y)
        sequence_of_z_vals.append(cube.z)

    ax.scatter(sequence_of_x_vals, sequence_of_y_vals, sequence_of_z_vals)
    plt.show()
