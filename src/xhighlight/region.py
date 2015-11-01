import enum


class Shape (enum.Enum):

    rectangular = 1
    ellipsoid = 2


class Region:

    def __init__(self, shape, x, y, width, height):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.shape = shape
