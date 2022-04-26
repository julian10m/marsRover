from abc import abstractstaticmethod, ABCMeta

class MarsRover():
    right_direction_update = {
                'N': 'E',
                'E': 'S',
                'S': 'W',
                'W': 'N',}


    left_direction_update = {
                'E': 'N',
                'S': 'E',
                'W': 'S',
                'N': 'W',}


    def __init__(self, x, y, direction):
        self.x =  x
        self.y = y
        self.direction = direction
        

    def set_x(self, x):
        self.x = x
    

    def set_y(self, y):
        self.y = y


    def rotate_left(self):
        self.direction = self.left_direction_update[self.direction]


    def rotate_right(self):
        self.direction = self.right_direction_update[self.direction]


    def get_next_coord(self, current_coord, delta, side_length):
        next_coord = current_coord + delta
        if next_coord < 0:
            return side_length - 1
        elif next_coord == side_length:
            return 0
        return next_coord


    def get_next_x_coord(self, delta, side_length):
        return self.get_next_coord(self.x, delta, side_length)


    def get_next_y_coord(self, delta, side_length):
        return self.get_next_coord(self.y, delta, side_length)        


    def update_position(self, grid):
        if self.direction == 'N' or self.direction == 'S':
            if self.direction == 'N':
                new_y = self.get_next_y_coord(1, len(grid[0]))
            else:
                new_y = self.get_next_y_coord(-1, len(grid[0]))
            if grid[self.x][new_y] == 'O':
                return True
            self.set_y(new_y)
        else:
            if self.direction == 'E':
                new_x = self.get_next_x_coord(1, len(grid))
            else: # direction = 'W'
                new_x = self.get_next_x_coord(-1, len(grid))
            if grid[new_x][self.y] == 'O':
                return True
            self.set_x(new_x)
        return None


class ICommand(metaclass=ABCMeta):
    def __init__(self, mars_rover):
       self._mars_rover = mars_rover


    @abstractstaticmethod
    def execute():
        '''Defines what each command does.'''


class RotateLeft(ICommand):
    def execute(self):
        self._mars_rover.rotate_left()


class RotateRight(ICommand):

    def execute(self):
        self._mars_rover.rotate_right()


class Move(ICommand):

    def __init__(self, mars_rover, grid):
       super().__init__(mars_rover)
       self._grid = grid


    def execute(self):
        return self._mars_rover.update_position(self._grid)


class MarsRoverAPI():

    def __init__(self, mars_rover, grid):
        self.mars_rover = mars_rover
        self.grid = grid
        self.commands = self.register_commands()


    def register_commands(self):
        return {'L': RotateLeft(self.mars_rover),
                'R': RotateRight(self.mars_rover),
                'M': Move(self.mars_rover, self.grid),}


    def coords_string(self):
        return ':'.join([str(self.mars_rover.x), str(self.mars_rover.y)])


    def coords_output(self):
        return ':'.join([self.coords_string(), self.mars_rover.direction])


    def obstacle_output(self):
        return f'O:{self.coords_output()}'


    def execute(self, commands):
        for c in commands:
            output = self.commands[c].execute()
            if output is True:
                return self.obstacle_output()
        return self.coords_output()
