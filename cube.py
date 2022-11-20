# from space import Orientation


class Cube:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        # self.aligned_cube_group = []
        # self.orientation = Orientation.unknown

    # def set_align_with(self, cube_list):
    #     self.aligned_cube_group = cube_list

    # def set_orientation(self, orientation):
    #     self.orientation = orientation

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_z(self, z):
        self.z = z

    def update_coordinates(self, x, y, z):
        self.set_x(x)
        self.set_y(y)
        self.set_z(z)
